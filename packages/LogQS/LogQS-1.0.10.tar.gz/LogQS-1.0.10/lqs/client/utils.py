import io
import os
import re
import base64
import time
import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Iterable, List, Optional, Callable, Any
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

import requests
from lqs.interface.base.models import UploadState

try:
    # TODO: better way to handle this?
    # doesn't seem like it should be a hard dependency
    from PIL import Image as PILImage
except ImportError:
    PILImage = None

from lqs.transcode import Transcode
from lqs.common.utils import (
    get_relative_object_path,
    decompress_chunk_bytes,
)
from lqs.common.exceptions import ConflictException, NotFoundException
from lqs.interface.core.models import (
    Ingestion,
    Object,
    ObjectPart,
    Record,
    Topic,
    ProcessState,
)
from lqs.interface.pjm.models import JSONLLog

if TYPE_CHECKING:
    from lqs.client import RESTClient

DEFAULT_LOG_FILE_REGEXES = [
    r"/(?P<log_name>[^/]*?)\.bag$",
    r"/(?P<log_name>[^/]*?)\.log$",
    r"/(?P<log_name>[^/]*?)\.jsonl$",
    r"/(?P<log_name>[^/]*)\.log/log0$",
    r"/(?P<log_name>[^/]*)/log0$",
    r"/(?P<log_name>[^/]*)/manifests\/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
]


class Utils:
    def __init__(self, app: "RESTClient"):
        self.app = app

    def get_info(self, print_config=False, log_config=False):
        self.app.info("Logging info message.")
        self.app.debug("Logging debug message.")
        self.app.warn("Logging warn message.")
        self.app.error("Logging error message.")

        if print_config:
            print(self.app.config)

        if log_config:
            self.app.info(self.app.config)

    def fetch_by_name_or_create(
        self,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        resource_name: Optional[str] = None,
        list_params: dict = {},
        create_if_missing: bool = True,
        create_params: dict = {},
        create_func: Optional[Callable] = None,
        list_func: Optional[Callable] = None,
        fetch_func: Optional[Callable] = None,
    ) -> Any:
        """
        Fetch or create a resource by name.

        This function fetches a resource by id if provided, or by name if provided, or creates the resource if it doesn't exist and create_if_missing is True.
        If no resource id or name is provided, the function returns None.

        Args:
            resource_type (str): The type of the resource.
            resource_id (str, optional): The id of the resource. Defaults to None.
            resource_name (str, optional): The name of the resource. Defaults to None.
            list_params (dict, optional): Additional parameters to use when listing the resource. Defaults to {}.
            create_if_missing (bool, optional): Whether to create the resource if it doesn't exist. Defaults to True.
            create_params (dict, optional): Additional parameters to use when creating the resource. Defaults to {}.
            create_func (Callable, optional): The function to use when creating the resource. Defaults to None.
            list_func (Callable, optional): The function to use when listing the resource. Defaults to None.
            fetch_func (Callable, optional): The function to use when fetching the resource. Defaults to None.

        Raises:
            NotFoundException: If no resource is found and create_if_missing is False.

        Returns:
            Any: The fetched or created resource, or None if no resource is found or created.
        """
        resource = None
        if resource_id is None and resource_name is not None:
            # if no resource id is provided, we try to find the resource by name
            resources = list_func(name=resource_name, **list_params).data
            if len(resources) == 0:
                # we didn't find the resource by name
                if create_if_missing:
                    # if we're allowed to create the resource, we create it using the provided parameters
                    resource = create_func(name=resource_name, **create_params).data
                else:
                    raise NotFoundException(
                        f"No {resource_type} found with name {resource_name}"
                    )
            else:
                # we use the found resource
                resource = resources[0]
        elif resource_id is not None and resource_name is None:
            # if no resource name is provided, we try to find the resource by id
            resource = fetch_func(resource_id).data

        return resource

    def calculate_etag(self, file_path: str, part_size: int = 100 * 1024 * 1024) -> str:
        """
        Calculate the ETag of a file.

        This function calculates the ETag of a file assuming it is uploaded as a multipart upload.

        Args:
            file_path (str): The path to the file to calculate the ETag for.
            part_size (int, optional): The size of each chunk to read from the file. Defaults to 100 * 1024 * 1024.

        Returns:
            str: The calculated ETag.
        """
        part_md5s = []
        with open(file_path, "rb") as f:
            for part in iter(lambda: f.read(part_size), b""):
                part_md5s.append(hashlib.md5(part).digest())
        return hashlib.md5(b"".join(part_md5s)).hexdigest() + f"-{len(part_md5s)}"

    def verify_integrity(
        self, file_path: str, etag: str, part_size: int = 100 * 1024 * 1024
    ) -> bool:
        """
        Verify the integrity of a file given an ETag.

        This function verifies the integrity of a file assuming it is uploaded as a multipart upload.

        Args:
            file_path (str): The path to the file to verify the integrity of.
            etag (str): The ETag of the file.
            part_size (int, optional): The size of each chunk to read from the file. Defaults to 100 * 1024 * 1024.

        Returns:
            bool: Whether the file is intact.
        """
        calculated_etag = self.calculate_etag(file_path, part_size)
        self.app.debug(f"Calculated ETag for file {file_path}: {calculated_etag}")
        return calculated_etag == etag

    def verify_object_integrity(
        self, file_path: str, object: Object, part_size: int = 100 * 1024 * 1024
    ) -> bool:
        """
        Verify the integrity of a file given an object.

        This function verifies the integrity of a file assuming it is uploaded as a multipart upload.

        Args:
            file_path (str): The path to the file to verify the integrity of.
            object (Object): The object to verify the integrity of.
            part_size (int, optional): The size of each chunk to read from the file. Defaults to 100 * 1024 * 1024.

        Returns:
            bool: Whether the file is intact.
        """
        return self.verify_integrity(file_path, object.etag, part_size)

    # Uploading

    def upload_log_object_part(
        self,
        log_id: str,
        object_key: str,
        part_number: int,
        file_path: str,
        offset: int,
        size: int,
        max_attempts: int = 3,
        backoff_factor: float = 5.0,
        connect_timeout: int = 60,
        read_timeout: int = 600,
    ):
        """
        Upload a part of a file to a log object.

        Args:
            log_id (str): The log id to upload the object part to.
            object_key (str): The key of the object to upload the part to.
            part_number (int): The part number of the object part.
            file_path (str): The path to the file to upload.
            offset (int): The offset in the file to start reading from.
            size (int): The size of the part to upload.
            max_attempts (int, optional): The maximum number of attempts to upload the part. Defaults to 3.
            backoff_factor (float, optional): The backoff factor for retrying the upload. Defaults to 5.0.
            connect_timeout (int, optional): The connection timeout for the upload. Defaults to 60.
            read_timeout (int, optional): The read timeout for the upload. Defaults to 600.

        Raises:
            Exception: If the upload fails.

        Returns:
            ObjectPart: The uploaded object part.
        """
        log_id = str(log_id)
        object_part = self.app.create.log_object_part(
            log_id=log_id,
            object_key=object_key,
            size=size,
            part_number=part_number,
        ).data
        upload_object_data_url = object_part.presigned_url

        with open(file_path, "rb") as f:
            f.seek(offset)
            data = f.read(size)
            attempt_count = 0
            response = None
            for attempt_count in range(1, max_attempts + 1):
                if attempt_count > 1:
                    self.app.debug(
                        f"Retrying upload of part {part_number} of object {object_key} in log {log_id} (attempt {attempt_count}/{max_attempts})."
                    )
                try:
                    response = requests.put(
                        upload_object_data_url,
                        data=data,
                        timeout=(connect_timeout, read_timeout),
                    )
                    break
                except Exception as e:
                    self.app.debug(
                        f"Error while uploading part {part_number} of object {object_key} in log {log_id} (attempt {attempt_count}/{max_attempts}): {e}"
                    )
                    time.sleep(backoff_factor * (2 ** (attempt_count - 1)))
                    continue

        if response is None:
            raise Exception(
                f"Failed to upload part {part_number} of object {object_key} in log {log_id} after {max_attempts} attempts."
            )

        if response.status_code != 200:
            raise Exception(f"Error while uploading object part: {response.text}")

        return self.app.fetch.log_object_part(
            log_id=log_id,
            object_key=object_key,
            part_number=part_number,
        ).data

    def upload_log_object(
        self,
        log_id: str,
        file_path: str,
        object_key: str = None,
        key_replacement: tuple[str, str] = None,
        key_prefix: str = None,
        part_size: int = 100 * 1024 * 1024,
        max_workers: int | None = 8,
        skip_if_exists: bool = False,
        continue_upload: bool = True,
        skip_if_complete: bool = False,
        overwrite: bool = False,
        verify_integrity: bool = True,
    ) -> tuple["Object", list["ObjectPart"]]:
        """
        Upload a file to a log.

        The file is uploaded as a log object, meaning it is associated with a single log given by log_id.
        The file is split into parts of size part_size, which are uploaded in parallel using a maximum of max_workers workers.
        Note that larger values for part_size and max_workers will generally result in faster uploads, but may also result in higher memory usage.

        If skip_if_exists is set to True, the upload will be skipped if the object already exists.
        If continue_upload is set to True, any existing parts of the object will be skipped and the upload will continue from where it left off.
        If continue_upload is set to True and skip_if_complete is set to True, the upload will be skipped if the object is already complete.
        If overwrite is set to True, any existing object with the same key will be deleted before the upload.

        Args:
            log_id (str): The log id to upload the object to.
            file_path (str): The path to the file to upload.
            object_key (str, optional): The key to use for the object. Defaults to None.
            key_replacement (tuple[str, str], optional): A tuple of strings to replace in the object key. Defaults to None.
            key_prefix (str, optional): A prefix to add to the object key. Defaults to None.
            part_size (int, optional): The size of each part to upload. Defaults to 100 * 1024 * 1024.
            max_workers (int, optional): The maximum number of workers to use for parallel uploads. Defaults to 8.
            skip_if_exists (bool, optional): Whether to skip the upload if the object already exists. Defaults to False.
            continue_upload (bool, optional): Whether to continue an existing upload. Defaults to True.
            skip_if_complete (bool, optional): Whether to skip the continued upload if the object is already complete. Defaults to False.
            overwrite (bool, optional): Whether to overwrite the object if it already exists. Defaults to False.
            verify_integrity (bool, optional): Whether to verify the integrity of the uploaded object. Defaults to True.

        Raises:
            ConflictException: If existing resources conflict with the upload.

        Returns:
            tuple["Object", list["ObjectPart"]]: The uploaded object and its parts.
        """

        # First, create/re-create/fetch/etc. the log object
        if continue_upload and overwrite:
            raise Exception("Only one one of continue_upload, overwrite can be set to true")
        
        log_id = str(log_id)
        if object_key is None:
            object_key = file_path.split("/")[-1]
        if key_replacement is not None:
            object_key = object_key.replace(*key_replacement)
        if key_prefix is not None:
            object_key = os.path.join(key_prefix, object_key)
        if object_key.startswith("/"):
            object_key = object_key[1:]

        try:
            log_object = self.app.create.log_object(
                log_id=log_id,
                key=object_key,
            ).data
        except ConflictException as e:
            if skip_if_exists:
                self.app.debug(
                    f"Skipping upload of object {object_key} in log {log_id}."
                )
                log_object = self.app.fetch.log_object(
                    log_id=log_id, object_key=object_key
                ).data
                return log_object, []

            if continue_upload:
                self.app.debug(
                    f"Continuing upload of object {object_key} in log {log_id}."
                )
                log_object = self.app.fetch.log_object(
                    log_id=log_id, object_key=object_key
                ).data
                if log_object.upload_state == UploadState.complete:
                    if skip_if_complete:
                        self.app.debug(
                            f"Skipping complete upload of object {object_key} in log {log_id}."
                        )
                        return log_object, []
                    else:
                        raise ConflictException(
                            f"Can't continue upload: Upload of Object {object_key} in log {log_id} is already complete."
                        )
            elif overwrite:
                self.app.debug(f"Overwriting object {object_key} in log {log_id}.")
                self.app.delete.log_object(log_id=log_id, object_key=object_key)
                log_object = self.app.create.log_object(
                    log_id=log_id,
                    key=object_key,
                ).data
            else:
                raise e

        # Then, figure out which parts we need to upload
        object_size = os.path.getsize(file_path)
        number_of_parts = object_size // part_size + 1
        log_object_parts: List[ObjectPart] = []

        parts_res = self.app.list.log_object_part(log_id=log_id, object_key=object_key)
        log_object_parts += parts_res.data
        while parts_res.is_truncated:
            parts_res = self.app.list.log_object_part(
                log_id=log_id,
                object_key=object_key,
                part_number_marker=parts_res.next_part_number_marker,
            )
            log_object_parts += parts_res.data
        self.app.debug(
            f"Found {len(log_object_parts)} existing parts for object {object_key} in log {log_id}."
        )
        if continue_upload is False:
            if len(log_object_parts) > 0:
                raise ConflictException(
                    f"Object {object_key} in log {log_id} already has {len(log_object_parts)} parts."
                    "Set continue_upload to True to continue the upload or overwrite to start over."
                )
        else:
            self.app.debug(
                f"Found {len(log_object_parts)} existing parts for object {object_key} in log {log_id}."
            )
        log_object_parts.sort(key=lambda part: part.part_number)

        # Validate existing parts sizes
        for idx, part in enumerate(log_object_parts):
            if part.part_number == number_of_parts:
                # the last part is allowed to be smaller than part_size
                continue
            if part.size == 0:
                # the part exists, but it has no data, so we'll overwrite it anyways
                continue
            if part.size != part_size:
                raise ConflictException(
                    f"Part {part.part_number} of object {object_key} in log {log_id} has an unexpected size {part.size}."
                    f"All parts except for the last part need to be the same size as the given part_size {part_size}."
                    f"Either overwrite the object to start over or change the part_size to match existing parts."
                )

        def should_skip_part(part_number):
            existing_part = next(
                (part for part in log_object_parts if part.part_number == part_number),
                None,
            )
            if existing_part is not None:
                if existing_part.size == 0:
                    self.app.debug(
                        f"Overwriting empty part {part_number} of object {object_key} in log {log_id}."
                    )
                else:
                    self.app.debug(
                        f"Skipping existing part {part_number} of object {object_key} in log {log_id}."
                    )
                    return True
            return False

        # Upload the parts (in parallel if max_workers is set)
        if max_workers is not None:
            futures = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for idx in range(0, number_of_parts):
                    offset = idx * part_size
                    size = min(part_size, object_size - offset)
                    part_number = idx + 1
                    if should_skip_part(part_number):
                        continue
                    futures.append(
                        executor.submit(
                            self.upload_log_object_part,
                            log_id=log_id,
                            object_key=object_key,
                            part_number=part_number,
                            file_path=file_path,
                            offset=offset,
                            size=size,
                        )
                    )

                for future in futures:
                    log_object_parts.append(future.result())
        else:
            for idx in range(0, number_of_parts):
                offset = idx * part_size
                size = min(part_size, object_size - offset)
                part_number = idx + 1
                if should_skip_part(part_number):
                    continue
                log_object_parts.append(
                    self.upload_log_object_part(
                        log_id=log_id,
                        object_key=object_key,
                        part_number=part_number,
                        file_path=file_path,
                        offset=offset,
                        size=size,
                    )
                )

        # Finally, mark the object as complete to finish the upload
        log_object = self.app.update.log_object(
            log_id=log_id, object_key=object_key, data={"upload_state": UploadState.complete}
        ).data

        if verify_integrity:
            self.app.debug(
                f"Verifying integrity of object {object_key} in log {log_id}."
            )
            if not self.verify_object_integrity(file_path, log_object, part_size):
                raise Exception(
                    f"Integrity check failed for object {object_key} in log {log_id}."
                )

        return log_object, log_object_parts

    def upload_log_object_part_from_memory(
        self,
        log_id: str,
        object_key: str,
        part_number: int,
        part_data: bytes | str,
        size: int,
        max_attempts: int = 3,
        backoff_factor: float = 5.0,
        connect_timeout: int = 60,
        read_timeout: int = 600,
    ):
        """
        Upload a part of a file to a log object.

        Args:
            log_id (str): The log id to upload the object part to.
            object_key (str): The key of the object to upload the part to.
            part_number (int): The part number of the object part.
            part_data (bytes | str): The data to upload.
            size (int): The size of the part to upload.
            max_attempts (int, optional): The maximum number of attempts to upload the part. Defaults to 3.
            backoff_factor (float, optional): The backoff factor for retrying the upload. Defaults to 5.0.
            connect_timeout (int, optional): The connection timeout for the upload. Defaults to 60.
            read_timeout (int, optional): The read timeout for the upload. Defaults to 600.

        Raises:
            Exception: If the upload fails.

        Returns:
            ObjectPart: The uploaded object part.
        """
        log_id = str(log_id)
        object_part = self.app.create.log_object_part(
            log_id=log_id,
            object_key=object_key,
            size=size,
            part_number=part_number,
        ).data
        upload_object_data_url = object_part.presigned_url

        attempt_count = 0
        response = None
        for attempt_count in range(1, max_attempts + 1):
            if attempt_count > 1:
                self.app.debug(
                    f"Retrying upload of part {part_number} of object {object_key} in log {log_id} (attempt {attempt_count}/{max_attempts})."
                )
            try:
                response = requests.put(
                    upload_object_data_url,
                    data=part_data,
                    timeout=(connect_timeout, read_timeout),
                )
                break
            except Exception as e:
                self.app.debug(
                    f"Error while uploading part {part_number} of object {object_key} in log {log_id} (attempt {attempt_count}/{max_attempts}): {e}"
                )
                time.sleep(backoff_factor * (2 ** (attempt_count - 1)))
                continue

        if response is None:
            raise Exception(
                f"Failed to upload part {part_number} of object {object_key} in log {log_id} after {max_attempts} attempts."
            )

        if response.status_code != 200:
            raise Exception(f"Error while uploading object part: {response.text}")

        return self.app.fetch.log_object_part(
            log_id=log_id,
            object_key=object_key,
            part_number=part_number,
        ).data

    def upload_log_object_from_memory(
        self,
        log_id: str,
        file_like: io.BytesIO | io.StringIO,
        object_key: str,
        key_replacement: tuple[str, str] = None,
        key_prefix: str = None,
        part_size: int = 100 * 1024 * 1024,
        max_workers: int | None = 8,
        skip_if_exists: bool = False,
        continue_upload: bool = True,
        skip_if_complete: bool = False,
        overwrite: bool = False,
    ) -> tuple["Object", list["ObjectPart"]]:
        """
        Upload a file-like object to a log.

        The file is uploaded as a log object, meaning it is associated with a single log given by log_id.
        The file is split into parts of size part_size, which are uploaded in parallel using a maximum of max_workers workers.
        Note that larger values for part_size and max_workers will generally result in faster uploads, but may also result in higher memory usage.

        If skip_if_exists is set to True, the upload will be skipped if the object already exists.
        If continue_upload is set to True, any existing parts of the object will be skipped and the upload will continue from where it left off.
        If continue_upload is set to True and skip_if_complete is set to True, the upload will be skipped if the object is already complete.
        If overwrite is set to True, any existing object with the same key will be deleted before the upload.

        Args:
            log_id (str): The log id to upload the object to.
            file_like (io.BytesIO | io.StringIO): The file-like object to upload.
            object_key (str): The key to use for the object.
            key_replacement (tuple[str, str], optional): A tuple of strings to replace in the object key. Defaults to None.
            key_prefix (str, optional): A prefix to add to the object key. Defaults to None.
            part_size (int, optional): The size of each part to upload. Defaults to 100 * 1024 * 1024.
            max_workers (int, optional): The maximum number of workers to use for parallel uploads. Defaults to 8.
            skip_if_exists (bool, optional): Whether to skip the upload if the object already exists. Defaults to False.
            continue_upload (bool, optional): Whether to continue an existing upload. Defaults to True.
            skip_if_complete (bool, optional): Whether to skip the continued upload if the object is already complete. Defaults to False.
            overwrite (bool, optional): Whether to overwrite the object if it already exists. Defaults to False.

        Raises:
            ConflictException: If existing resources conflict with the upload.

        Returns:
            tuple["Object", list["ObjectPart"]]: The uploaded object and its parts.
        """

        # First, create/re-create/fetch/etc. the log object
        log_id = str(log_id)
        if key_replacement is not None:
            object_key = object_key.replace(*key_replacement)
        if key_prefix is not None:
            object_key = os.path.join(key_prefix, object_key)
        if object_key.startswith("/"):
            object_key = object_key[1:]

        try:
            log_object = self.app.create.log_object(
                log_id=log_id,
                key=object_key,
            ).data
        except ConflictException as e:
            if skip_if_exists:
                self.app.debug(
                    f"Skipping upload of object {object_key} in log {log_id}."
                )
                log_object = self.app.fetch.log_object(
                    log_id=log_id, object_key=object_key
                ).data
                return log_object, []

            if continue_upload:
                self.app.debug(
                    f"Continuing upload of object {object_key} in log {log_id}."
                )
                log_object = self.app.fetch.log_object(
                    log_id=log_id, object_key=object_key
                ).data
                if log_object.upload_state == UploadState.complete:
                    if skip_if_complete:
                        self.app.debug(
                            f"Skipping complete upload of object {object_key} in log {log_id}."
                        )
                        return log_object, []
                    else:
                        raise ConflictException(
                            f"Can't continue upload: Upload of Object {object_key} in log {log_id} is already complete."
                        )
            elif overwrite:
                self.app.debug(f"Overwriting object {object_key} in log {log_id}.")
                self.app.delete.log_object(log_id=log_id, object_key=object_key)
                log_object = self.app.create.log_object(
                    log_id=log_id,
                    key=object_key,
                ).data
            else:
                raise e

        # Then, figure out which parts we need to upload
        if isinstance(file_like, io.StringIO):
            object_size = len(file_like.getvalue())
        elif isinstance(file_like, io.BytesIO):
            object_size = file_like.getbuffer().nbytes
        else:
            raise TypeError(
                "file_like must be an instance of io.BytesIO or io.StringIO"
            )
        number_of_parts = object_size // part_size + 1
        log_object_parts: List[ObjectPart] = []

        parts_res = self.app.list.log_object_part(log_id=log_id, object_key=object_key)
        log_object_parts += parts_res.data
        while parts_res.is_truncated:
            parts_res = self.app.list.log_object_part(
                log_id=log_id,
                object_key=object_key,
                part_number_marker=parts_res.next_part_number_marker,
            )
            log_object_parts += parts_res.data
        self.app.debug(
            f"Found {len(log_object_parts)} existing parts for object {object_key} in log {log_id}."
        )
        if continue_upload is False:
            if len(log_object_parts) > 0:
                raise ConflictException(
                    f"Object {object_key} in log {log_id} already has {len(log_object_parts)} parts."
                    "Set continue_upload to True to continue the upload or overwrite to start over."
                )
        else:
            self.app.debug(
                f"Found {len(log_object_parts)} existing parts for object {object_key} in log {log_id}."
            )
        log_object_parts.sort(key=lambda part: part.part_number)

        # Validate existing parts sizes
        for idx, part in enumerate(log_object_parts):
            if part.part_number == number_of_parts:
                # the last part is allowed to be smaller than part_size
                continue
            if part.size == 0:
                # the part exists, but it has no data, so we'll overwrite it anyways
                continue
            if part.size != part_size:
                raise ConflictException(
                    f"Part {part.part_number} of object {object_key} in log {log_id} has an unexpected size {part.size}."
                    f"All parts except for the last part need to be the same size as the given part_size {part_size}."
                    f"Either overwrite the object to start over or change the part_size to match existing parts."
                )

        def should_skip_part(part_number):
            existing_part = next(
                (part for part in log_object_parts if part.part_number == part_number),
                None,
            )
            if existing_part is not None:
                if existing_part.size == 0:
                    self.app.debug(
                        f"Overwriting empty part {part_number} of object {object_key} in log {log_id}."
                    )
                else:
                    self.app.debug(
                        f"Skipping existing part {part_number} of object {object_key} in log {log_id}."
                    )
                    return True
            return False

        # Upload the parts (in parallel if max_workers is set)
        if max_workers is not None:
            futures = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for idx in range(0, number_of_parts):
                    offset = idx * part_size
                    file_like.seek(offset)
                    size = min(part_size, object_size - offset)
                    part_number = idx + 1
                    if should_skip_part(part_number):
                        continue
                    futures.append(
                        executor.submit(
                            self.upload_log_object_part_from_memory,
                            log_id=log_id,
                            object_key=object_key,
                            part_number=part_number,
                            part_data=file_like.read(size),
                            size=size,
                        )
                    )

                for future in futures:
                    log_object_parts.append(future.result())
        else:
            for idx in range(0, number_of_parts):
                offset = idx * part_size
                file_like.seek(offset)
                size = min(part_size, object_size - offset)
                part_number = idx + 1
                if should_skip_part(part_number):
                    continue
                log_object_parts.append(
                    self.upload_log_object_part_from_memory(
                        log_id=log_id,
                        object_key=object_key,
                        part_number=part_number,
                        part_data=file_like.read(size),
                        size=size,
                    )
                )

        # Finally, mark the object as complete to finish the upload
        log_object = self.app.update.log_object(
            log_id=log_id, object_key=object_key, data={"upload_state": UploadState.complete}
        ).data

        return log_object, log_object_parts

    def upload_log_objects(
        self,
        log_id: str,
        file_dir: str,
        fail_if_empty: bool = True,
        key_replacement: tuple[str, str] = None,
        key_prefix: str = None,
        part_size: int = 100 * 1024 * 1024,
        max_workers: int | None = 8,
        skip_if_exists: bool = False,
        continue_upload: bool = True,
        skip_if_complete: bool = False,
        overwrite: bool = False,
        verify_integrity: bool = True,
    ) -> List[tuple["Object", list["ObjectPart"]]]:
        """
        Upload a directory of files to a log.

        The files are uploaded as log objects, meaning they are associated with a single log given by log_id.
        The files are split into parts of size part_size, which are uploaded in parallel using a maximum of max_workers workers.
        Note that larger values for part_size and max_workers will generally result in faster uploads, but may also result in higher memory usage.

        If skip_if_exists is set to True, the upload will be skipped if the object already exists.
        If continue_upload is set to True, any existing parts of the object will be skipped and the upload will continue from where it left off.
        If continue_upload is set to True and skip_if_complete is set to True, the upload will be skipped if the object is already complete.
        If overwrite is set to True, any existing object with the same key will be deleted before the upload.

        Args:
            log_id (str): The log id to upload the objects to.
            file_dir (str): The path to the directory to upload.
            fail_if_empty (bool, optional): Whether to raise an exception if no files are found in the directory. Defaults to True.
            key_replacement (tuple[str, str], optional): A tuple of strings to replace in the object keys. Defaults to None.
            key_prefix (str, optional): A prefix to add to the object keys. Defaults to None.
            part_size (int, optional): The size of each part to upload. Defaults to 100 * 1024 * 1024.
            max_workers (int, optional): The maximum number of workers to use for parallel uploads. Defaults to 8.
            skip_if_exists (bool, optional): Whether to skip the upload if the object already exists. Defaults to False.
            continue_upload (bool, optional): Whether to continue an existing upload. Defaults to True.
            skip_if_complete (bool, optional): Whether to skip the continued upload if the object is already complete. Defaults to False.
            overwrite (bool, optional): Whether to overwrite the object if it already exists. Defaults to False.
            verify_integrity (bool, optional): Whether to verify the integrity of the uploaded objects. Defaults to True.

        Raises:
            Exception: If no files are found in the directory and fail_if_empty is True.

        Returns:
            list[tuple["Object", list["ObjectPart"]]]: A list of tuples of uploaded objects and their parts.
        """
        log_id = str(log_id)
        upload_result_sets = []
        for file_path in Path(file_dir).rglob("*"):
            if os.path.isfile(file_path):
                object_key = str(file_path)
                if key_replacement is not None:
                    object_key = object_key.replace(*key_replacement)
                if key_prefix is not None:
                    object_key = os.path.join(key_prefix, object_key)
                if object_key.startswith("/"):
                    object_key = object_key[1:]
                upload_result = self.upload_log_object(
                    log_id=log_id,
                    file_path=file_path,
                    object_key=object_key,
                    part_size=part_size,
                    max_workers=max_workers,
                    skip_if_exists=skip_if_exists,
                    continue_upload=continue_upload,
                    skip_if_complete=skip_if_complete,
                    overwrite=overwrite,
                    verify_integrity=verify_integrity,
                )
                upload_result_sets.append(upload_result)
        if fail_if_empty and len(upload_result_sets) == 0:
            raise Exception(f"No files found in {file_dir}")
        return upload_result_sets

    def find_local_logs(
        self,
        root_dir: str,
        log_file_regexes: List[str] = DEFAULT_LOG_FILE_REGEXES,
        max_depth: Optional[int] = None,
    ) -> List[dict]:
        """
        Generate a list of log parameters from a directory of log files.

        This function searches the root directory for log files using the given regular expressions. The log parameters include the log_path, log_directory, log_name, and group_name.
        The log_name and group_name are extracted from the corresponding named capture groups of the regular expression.
        If the log_name captured group is followed by a slash, the log directory is also extracted, otherwise it is set to None.

        Args:
            root_dir (str): The directory to search for log files.
            log_file_regexes (List[str], optional): A list of regular expressions to match log files. Defaults to DEFAULT_LOG_FILE_REGEXES.
            max_depth (int, optional): The maximum depth to search for log files. Defaults to None.

        Returns:
            List[dict]: A list of log parameters.
        """
        log_param_sets = []
        for dir_path, dir_names, file_names in os.walk(root_dir):
            if (
                max_depth is not None
                and dir_path.count("/") - root_dir.count("/") > max_depth
            ):
                continue
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                for log_file_regex in log_file_regexes:
                    re_match = re.search(log_file_regex, file_path)
                    if re_match:
                        re_params = re_match.groupdict()
                        log_name = re_params.get("log_name")
                        group_name = re_params.get("group_name")
                        log_dir = None

                        r_index = re_match.end(1)
                        slash_index = file_path.find("/", r_index)
                        if slash_index != -1:
                            log_dir = file_path[: slash_index + 1]

                        log_params = {
                            "log_path": file_path,
                            "log_dir": log_dir,
                            "log_name": log_name,
                            "group_name": group_name,
                        }
                        log_param_sets.append(log_params)
                        break
        return log_param_sets

    def sync_log_objects(
        self,
        root_dir: str,
        log_file_regexes: List[str] = DEFAULT_LOG_FILE_REGEXES,
        max_depth: Optional[int] = None,
        group_id: Optional[str] = None,
        group_name: Optional[str] = None,
        create_group_if_missing: bool = True,
        group_note: Optional[str] = None,
        group_context: Optional[dict] = None,
        log_id: Optional[str] = None,
        log_name: Optional[str] = None,
        create_log_if_missing: bool = True,
        log_note: Optional[str] = None,
        log_context: Optional[dict] = None,
        key_prefix: str = None,
        part_size: int = 100 * 1024 * 1024,
        max_workers: int | None = 8,
        skip_if_exists: bool = False,
        continue_upload: bool = True,
        skip_if_complete: bool = False,
        overwrite: bool = False,
        verify_integrity: bool = True,
        create_ingestions: bool = True,
        skip_existing_ingestions: bool = True,
        ingestion_state: ProcessState = ProcessState.queued,
        ingestion_note: Optional[str] = None,
        ingestion_context: Optional[dict] = None,
        ingestion_workflow_id: Optional[str] = None,
        ingestion_workflow_context: Optional[dict] = None,
        verbosity: Optional[str] = "info",
    ) -> int:
        """
        Sync log files from a local directory to LogQS.

        This function searches the root directory for log files using the given regular expressions. It then uploads the log files to LogQS and, optionally, creates ingestions for them.
        The name used for the LogQS log resource of a found log file is extracted from the first capture group of the regular expression. If the captured group is followed by a slash,
        the log directory is also extracted. If the log with the extracted name does not exist in the group, it is created. If the group does not exist, it is created if create_group_if_missing is True.
        If log_id or log_name is provided, the logs are uploaded to the specified log instead of the log given by the name captured when finding the log files.
        If the log_id is not provided, the log_name is used to find or create the log to upload the logs to. If the group_id is not provided, the group_name is used to find or create the group to upload the logs to.
        If the group_name is not found and create_group_if_missing is True, a new group is created.
        If create_ingestions is True, ingestions are created for the logs. If skip_existing_ingestions is True, ingestions are only created for logs that don't already have corresponding ingestions.

        Args:
            root_dir (str): The directory to search for log files.
            log_file_regexes (List[str], optional): A list of regular expressions to match log files. Defaults to DEFAULT_LOG_FILE_REGEXES.
            max_depth (int, optional): The maximum depth to search for log files. Defaults to None.

            group_id (Optional[str], optional): The group id to upload the logs to. Defaults to None.
            group_name (Optional[str], optional): The group name to upload the logs to. Defaults to None.
            create_group_if_missing (bool, optional): Whether to create the group if it doesn't exist. Defaults to True.
            group_note (Optional[str], optional): A note to use when creating the group. Defaults to None.
            group_context (Optional[dict], optional): A context to use when creating the group. Defaults to None.

            log_id (Optional[str], optional): The log id to upload the logs to. Defaults to None.
            log_name (Optional[str], optional): The log name to upload the logs to. Defaults to None.
            create_log_if_missing (bool, optional): Whether to create the log if it doesn't exist. Defaults to True.
            log_note (Optional[str], optional): A note to use when creating the log. Defaults to None.
            log_context (Optional[dict], optional): A context to use when creating the log. Defaults to None.

            key_prefix (str, optional): A prefix to add to the object keys. Defaults to None.
            part_size (int, optional): The size of each part to upload. Defaults to 100 * 1024 * 1024.
            max_workers (int, optional): The maximum number of workers to use for parallel uploads. Defaults to 8.
            skip_if_exists (bool, optional): Whether to skip the upload if the object already exists. Defaults to False.
            continue_upload (bool, optional): Whether to continue an existing upload. Defaults to True.
            skip_if_complete (bool, optional): Whether to skip the continued upload if the object is already complete. Defaults to False.
            overwrite (bool, optional): Whether to overwrite the object if it already exists. Defaults to False.
            verify_integrity (bool, optional): Whether to verify the integrity of the uploaded objects. Defaults to True.

            create_ingestions (bool, optional): Whether to create ingestions for the logs. Defaults to True.
            skip_existing_ingestions (bool, optional): Whether to skip creating ingestions for logs that already have ingestions. Defaults to True.
            ingestion_state (str, optional): The state to set for the ingestions. Defaults to "queued".
            ingestion_note (Optional[str], optional): A note to add to the ingestions. Defaults to None.
            ingestion_context (Optional[dict], optional): A context to add to the ingestions. Defaults to None.
            ingestion_workflow_id (Optional[str], optional): The workflow id to use when creating the ingestions. Defaults to None.
            ingestion_workflow_context (Optional[dict], optional): The workflow context to use when creating the ingestions. Defaults to None.

            verbosity (Optional[str], optional): The verbosity level to use. One of "debug", "info", or "error". Defaults to "info".

        Returns:
            int: The number of uploaded log files.
        """

        def logger(msg):
            if verbosity is not None:
                getattr(self.app, verbosity.lower())(msg)

        # First, figure out which group/log we're working with
        group = None
        if group_id is not None or group_name is not None:
            group = self.fetch_by_name_or_create(
                resource_type="group",
                resource_id=group_id,
                resource_name=group_name,
                list_params={},
                create_if_missing=create_group_if_missing,
                create_params={"note": group_note, "context": group_context},
                create_func=self.app.create.group,
                list_func=self.app.list.group,
                fetch_func=self.app.fetch.group,
            )
        if group is None:
            logger(
                "No group ID or name provided; will create groups based on found log parameters."
            )

        log = None
        if group is not None:
            if log_id is not None or log_name is not None:
                log = self.fetch_by_name_or_create(
                    resource_type="log",
                    resource_id=log_id,
                    resource_name=log_name,
                    list_params={"group_id": group.id},
                    create_if_missing=create_log_if_missing,
                    create_params={
                        "group_id": group.id,
                        "note": log_note,
                        "context": log_context,
                    },
                    create_func=self.app.create.log,
                    list_func=self.app.list.log,
                    fetch_func=self.app.fetch.log,
                )
            if log is None:
                logger(
                    "No log ID or name provided; will create logs based on found log parameters."
                )

        # Next, we find all the log files in the root directory
        log_param_sets = self.find_local_logs(
            root_dir=root_dir,
            log_file_regexes=log_file_regexes,
            max_depth=max_depth,
        )
        logger(f"Found {len(log_param_sets)} logs in {root_dir}")

        # for each log, we check if the log already exists in the group
        uploaded_file_count = 0
        for params in log_param_sets:
            sync_group = None
            sync_log = None

            log_name_param = params.get("log_name")
            group_name_param = params.get("group_name")
            log_dir_param = params.get("log_dir")
            log_path_param = params.get("log_path")

            if log_path_param.endswith(".jsonl"):
                # if the log_path_param points to a JSONL file, we attempt to parse it as a JSONLLog
                jsonl_log = JSONLLog()
                jsonl_log.load_jsonl_file(log_path_param)
                if jsonl_log.header:
                    header_log_name = jsonl_log.header.log_name
                    header_group_name = jsonl_log.header.group_name
                    jsonl_group = self.fetch_by_name_or_create(
                        resource_type="group",
                        resource_name=header_group_name,
                        create_if_missing=create_group_if_missing,
                        create_params={
                            "note": jsonl_log.header.group_note,
                            "context": jsonl_log.header.group_context,
                        },
                        create_func=self.app.create.group,
                        list_func=self.app.list.group,
                        fetch_func=self.app.fetch.group,
                    )
                    sync_log = self.fetch_by_name_or_create(
                        resource_type="log",
                        resource_name=header_log_name,
                        list_params={"group_id": jsonl_group.id},
                        create_if_missing=create_log_if_missing,
                        create_params={
                            "group_id": jsonl_group.id,
                            "note": jsonl_log.header.log_note,
                            "context": jsonl_log.header.log_context,
                        },
                        create_func=self.app.create.log,
                        list_func=self.app.list.log,
                        fetch_func=self.app.fetch.log,
                    )
                    logger(
                        f"Using JSONL header defined log {sync_log.name} ({sync_log.id}) in group {jsonl_group.name} ({jsonl_group.id})"
                    )

            if sync_group is None and group is None:
                groups = self.app.list.group(name=group_name_param).data
                if len(groups) == 0:
                    logger(f"Creating group {group_name_param}")
                    sync_group = self.app.create.group(
                        name=group_name_param,
                        note=group_note,
                        context=group_context,
                    ).data
                else:
                    sync_group = groups[0]
            elif sync_group is None and group is not None:
                sync_group = group

            if sync_log is None and log is None:
                logs = self.app.list.log(
                    group_id=sync_group.id, name=log_name_param
                ).data
                if len(logs) == 0:
                    logger(
                        f"Creating log {log_name_param} in group {sync_group.name} ({sync_group.id})"
                    )
                    sync_log = self.app.create.log(
                        group_id=sync_group.id,
                        name=log_name_param,
                        note=log_note,
                        context=log_context,
                    ).data
                else:
                    sync_log = logs[0]
            elif sync_log is None and log is not None:
                sync_log = log

            # for each log, we upload the log files
            logger(f"Uploading log files for log {sync_log.name} ({sync_log.id})")
            log_object_key = None
            if log_dir_param is not None:
                key_replacement = (log_dir_param, "")
                log_object_sets = self.upload_log_objects(
                    log_id=sync_log.id,
                    file_dir=log_dir_param,
                    key_replacement=key_replacement,
                    key_prefix=key_prefix,
                    part_size=part_size,
                    max_workers=max_workers,
                    skip_if_exists=skip_if_exists,
                    continue_upload=continue_upload,
                    skip_if_complete=skip_if_complete,
                    overwrite=overwrite,
                    verify_integrity=verify_integrity,
                )
                uploaded_file_count += len(log_object_sets)
                log_file_name = log_path_param.split("/")[-1]
                for log_object, _ in log_object_sets:
                    if log_file_name in log_object.key:
                        log_object_key = log_object.key
                        break
                if log_object_key is None:
                    raise Exception(
                        f"Log file {log_file_name} not found in uploaded objects."
                    )
            else:
                log_object, _ = self.upload_log_object(
                    log_id=sync_log.id,
                    file_path=log_path_param,
                    part_size=part_size,
                    max_workers=max_workers,
                    skip_if_exists=skip_if_exists,
                    continue_upload=continue_upload,
                    skip_if_complete=skip_if_complete,
                    overwrite=overwrite,
                    verify_integrity=verify_integrity,
                )
                uploaded_file_count += 1
                log_object_key = log_object.key
            logger(
                f"Log object key {log_object_key} uploaded for log {sync_log.name} ({sync_log.id})"
            )

            # for each log, we create an ingestion
            if create_ingestions:
                ingestions = self.app.list.ingestion(
                    log_id=sync_log.id, object_key_like=log_object_key
                ).data
                if len(ingestions) == 0 or not skip_existing_ingestions:
                    ingestion = self.app.create.ingestion(
                        log_id=sync_log.id,
                        object_key=log_object_key,
                        name=sync_log.name,
                        note=ingestion_note,
                        state=ingestion_state,
                        context=ingestion_context,
                        workflow_id=ingestion_workflow_id,
                        workflow_context=ingestion_workflow_context,
                    ).data
                    logger(
                        f"Ingestion {ingestion.id} created for log {sync_log.name} ({sync_log.id}) for {log_object_key}"
                    )

        logger(f"Uploaded {uploaded_file_count} log files")
        return uploaded_file_count

    # Downloading

    def load_auxiliary_data_image(self, source: Record | dict):
        if isinstance(source, Record):
            auxiliary_data = source.get_auxiliary_data()
        else:
            auxiliary_data = source

        if auxiliary_data is None:
            return None
        if "image" not in auxiliary_data:
            return None
        if PILImage is None:
            raise Exception("PIL is not installed")
        encoded_webp_data = auxiliary_data["image"]
        decoded_webp_data = base64.b64decode(encoded_webp_data)
        image = PILImage.open(io.BytesIO(decoded_webp_data))
        return image

    def get_deserialized_record_data(
        self,
        record: Record,
        topic: Topic | None = None,
        ingestion: Ingestion | None = None,
        transcoder: Transcode | None = None,
    ) -> dict:
        if transcoder is None:
            transcoder = Transcode()

        if topic is None:
            topic = self.app.fetch.topic(record.topic_id).data

        message_bytes = self.fetch_record_bytes(record=record, ingestion=ingestion)

        return transcoder.deserialize(
            type_encoding=topic.type_encoding,
            type_name=topic.type_name,
            type_data=topic.type_data,
            message_bytes=message_bytes,
        )

    def fetch_record_bytes(
        self,
        record: Record,
        ingestion: Ingestion | None = None,
        decompress_chunk: bool = True,
        return_full_chunk: bool = False,
    ) -> bytes:

        if ingestion is None:
            ingestion = self.app.fetch.ingestion(record.ingestion_id).data

        object_store_id = (
            str(ingestion.object_store_id)
            if ingestion.object_store_id is not None
            else None
        )
        object_key = str(ingestion.object_key)

        if record.source is not None:
            # if the record has a source, we need to get the relative path from the object_key
            object_key = get_relative_object_path(
                object_key=object_key, source=record.source
            )

        if object_store_id is None:
            # the data is coming from a log object
            message_bytes: bytes = self.app.fetch.log_object(
                object_key=object_key,
                log_id=record.log_id,
                redirect=True,
                offset=record.data_offset,
                length=record.data_length,
            )
        else:
            # the data is coming from an object store
            message_bytes: bytes = self.app.fetch.object(
                object_key=object_key,
                object_store_id=object_store_id,
                redirect=True,
                offset=record.data_offset,
                length=record.data_length,
            )

        if record.chunk_compression is not None:
            if decompress_chunk:
                # if the record is compressed, we need to decompress it
                message_bytes = decompress_chunk_bytes(
                    chunk_bytes=message_bytes,
                    chunk_compression=record.chunk_compression,
                    chunk_length=record.chunk_length,
                )
                if not return_full_chunk:
                    # we only return the relevant part of the chunk
                    message_bytes = message_bytes[
                        record.chunk_offset : record.chunk_offset + record.chunk_length
                    ]
            else:
                if not return_full_chunk:
                    raise Exception(
                        "Cannot return partial chunk without decompressing it."
                    )

        return message_bytes

    def get_contiguous_record_offsets(
        self, records: Iterable[Record]
    ) -> tuple[int, int]:
        start_offset = None
        end_offset = None
        ingestion_id = None
        source = None
        for record in records:
            if ingestion_id is None:
                ingestion_id = record.ingestion_id
                if record.source is not None:
                    source = record.source

            if record.ingestion_id != ingestion_id:
                raise Exception(
                    "All records must have the same ingestion. Found {record.ingestion_id} and {ingestion.id}."
                )

            if record.source != source:
                raise Exception(
                    "All records must have the same source. Found {record.source} and {source}."
                )

            if start_offset is None:
                start_offset = record.data_offset

            if end_offset is None:
                end_offset = record.data_offset + record.data_length

            current_end_offset = record.data_offset + record.data_length
            if current_end_offset < end_offset:
                raise Exception(
                    "Records must be ordered by data offset. Found current end offset {current_end_offset} less than last end offset {end_offset}."
                )
            else:
                end_offset = current_end_offset

        return start_offset, end_offset

    def get_record_sets(
        self,
        records: Iterable[Record],
        density_threshold: float = 0.9,
        max_contiguous_size: int = 100 * 1000 * 1000,  # 100 MB
        max_contiguous_records: int = 1000,
    ) -> list[list[Record]]:
        record_sets: list[list[Record]] = []
        record_set: list[Record] = []
        relevant_length = 0
        full_length = 0
        start_offset = None
        last_ingestion_id = None
        last_source = None
        last_offset = None

        for record in records:
            if start_offset is None:
                start_offset = record.data_offset
            if last_ingestion_id is None:
                last_ingestion_id = record.ingestion_id
            if last_source is None:
                last_source = record.source
            if last_offset is None:
                last_offset = record.data_offset + record.data_length

            relevant_length += record.data_length
            full_length = record.data_offset + record.data_length - start_offset
            if (
                relevant_length / full_length > density_threshold
                and last_ingestion_id == record.ingestion_id
                and last_source == record.source
                and len(record_set) < max_contiguous_records
                and full_length < max_contiguous_size
                and record.data_offset + record.data_length >= last_offset
            ):
                record_set.append(record)
                last_offset = record.data_offset + record.data_length
            else:
                if len(record_set) == 0:
                    raise Exception("Record set cannot be empty.")
                record_sets.append(record_set)
                record_set = [record]
                relevant_length = record.data_length
                full_length = record.data_length
                start_offset = record.data_offset
                last_ingestion_id = record.ingestion_id
                last_source = record.source

        if len(record_set) > 0:
            record_sets.append(record_set)
        return record_sets

    def iter_dense_record_data(
        self,
        records: Iterable[Record],
        deserialize_results: bool = True,
        transcoder: Transcode | None = None,
        stream_data: bool = True,
        ingestions: dict[str, Ingestion] = {},
        topics: dict[str, Topic] = {},
    ) -> Iterator[tuple[Record, bytes | dict]]:
        if transcoder is None:
            transcoder = Transcode()

        object_key: str | None = None
        source: str | None = None

        start_offset = None
        end_offset = None
        for record in records:
            ingestion_id = str(record.ingestion_id)
            if ingestion_id not in ingestions:
                ingestions[ingestion_id] = self.app.fetch.ingestion(ingestion_id).data
            ingestion = ingestions[ingestion_id]

            if object_key is None:
                object_key = str(ingestion.object_key)
                if record.source is not None:
                    source = record.source
                    object_key = get_relative_object_path(
                        object_key=object_key, source=record.source
                    )

            if record.ingestion_id != ingestion.id:
                raise Exception(
                    "All records must have the same ingestion. Found {record.ingestion_id} and {ingestion.id}."
                )

            if record.source != source:
                raise Exception(
                    "All records must have the same source. Found {record.source} and {source}."
                )

            if start_offset is None:
                start_offset = record.data_offset

            if end_offset is None:
                end_offset = record.data_offset + record.data_length

            current_end_offset = record.data_offset + record.data_length
            if current_end_offset < end_offset:
                raise Exception(
                    "Records must be ordered by data offset. Found current end offset {current_end_offset} less than last end offset {end_offset}."
                )
            else:
                end_offset = current_end_offset

        # Now we fetch the object meta data and open a stream to the data
        if ingestion.object_store_id is None:
            # the data is coming from a log object
            object_meta: Object = self.app.fetch.log_object(
                object_key=object_key,
                log_id=ingestion.log_id,
                redirect=False,
                offset=start_offset,
                length=end_offset - start_offset,
            ).data
        else:
            # the data is coming from an object store
            object_meta: Object = self.app.fetch.object(
                object_key=object_key,
                object_store_id=ingestion.object_store_id,
                redirect=False,
                offset=start_offset,
                length=end_offset - start_offset,
            ).data

        presigned_url = object_meta.presigned_url
        headers = {
            "Range": f"bytes={start_offset}-{end_offset - 1}",
        }
        if stream_data:
            buffer_length = 1_000_000 * 32  # 32 MB
            r = requests.get(presigned_url, headers=headers, stream=True)
            r.raise_for_status()
            data_stream = io.BufferedReader(r.raw, buffer_length)
        else:
            r = requests.get(presigned_url, headers=headers, stream=False)
            r.raise_for_status()
            data_stream = io.BytesIO(r.content)

        # Now we can iterate over the records and read the data from the stream
        decompressed_bytes: bytes | None = None
        compressed_chunk_offset: int | None = None
        current_offset = start_offset
        for record in records:
            data_offset = record.data_offset
            data_length = record.data_length

            if (
                compressed_chunk_offset is not None
                and record.chunk_compression is not None
                and record.data_offset == compressed_chunk_offset
            ):
                message_bytes = decompressed_bytes[
                    record.chunk_offset : record.chunk_offset + record.chunk_length
                ]
            else:
                data_stream.read(data_offset - current_offset)
                message_bytes = data_stream.read(data_length)
                current_offset = data_offset + data_length

            if record.chunk_compression is not None:
                decompressed_bytes = decompress_chunk_bytes(
                    chunk_bytes=message_bytes,
                    chunk_compression=record.chunk_compression,
                    chunk_length=record.chunk_length,
                )
                message_bytes = decompressed_bytes[
                    record.chunk_offset : record.chunk_offset + record.chunk_length
                ]
                compressed_chunk_offset = record.data_offset

            if deserialize_results:
                # if we want to deserialize the results, we need the topic
                topic_id = str(record.topic_id)
                if topic_id not in topics:
                    # if we haven't seen this record's topic yet, we fetch it here
                    topics[topic_id] = self.app.fetch.topic(record.topic_id).data
                topic = topics[topic_id]
                record_data = transcoder.deserialize(
                    type_encoding=topic.type_encoding,
                    type_name=topic.type_name,
                    type_data=topic.type_data,
                    message_bytes=message_bytes,
                )
                yield (record, record_data)
            else:
                yield (record, message_bytes)

    def iter_record_data(
        self,
        records: Iterable[Record],
        deserialize_results: bool = True,
        transcoder: Transcode | None = None,
        density_threshold: float = 0.9,
        max_contiguous_size: int = 100 * 1000 * 1000,
        max_contiguous_records: int = 1000,
        max_workers: int | None = 10,
        return_as_completed: bool = False,
    ) -> Iterator[tuple[Record, bytes | dict]]:

        if transcoder is None:
            transcoder = Transcode()

        record_sets = self.get_record_sets(
            records=records,
            density_threshold=density_threshold,
            max_contiguous_size=max_contiguous_size,
            max_contiguous_records=max_contiguous_records,
        )

        def generate_data(
            records: Iterable[Record],
            deserialize_results: bool = True,
            transcoder: Transcode | None = None,
            ingestions: dict[str, Ingestion] = {},
            topics: dict[str, Topic] = {},
        ):
            results = [
                d
                for d in self.iter_dense_record_data(
                    records=records,
                    deserialize_results=deserialize_results,
                    transcoder=transcoder,
                    ingestions=ingestions,
                    topics=topics,
                )
            ]
            return results

        ingestions: dict[str, Ingestion] = {}
        topics: dict[str, Topic] = {}
        futures: list[Future[list[bytes | dict]]] = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for record_set in record_sets:
                future = executor.submit(
                    generate_data,
                    records=record_set,
                    deserialize_results=deserialize_results,
                    transcoder=transcoder,
                    ingestions=ingestions,
                    topics=topics,
                )
                futures.append(future)

            future_iterator = None
            if return_as_completed:
                future_iterator = as_completed(futures)
            else:
                future_iterator = futures

            for future in future_iterator:
                results = future.result()
                for result in results:
                    yield result
