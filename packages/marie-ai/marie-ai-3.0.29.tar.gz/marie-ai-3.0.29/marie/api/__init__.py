import hashlib
import imghdr
import io
import os
from datetime import datetime
from typing import Dict, Tuple

import cv2
import numpy as np

from marie.logging.predefined import default_logger
from marie.storage import StorageManager
from marie.utils.base64 import base64StringToBytes
from marie.utils.utils import FileSystem, ensure_exists

logger = default_logger

ALLOWED_TYPES = {"png", "jpeg", "tiff"}
TYPES_TO_EXT = {"png": "png", "jpeg": "jpg", "tiff": "tif"}


def store_temp_file(message_bytes, queue_id, file_type, store_raw) -> tuple[str, str]:
    """Store temp file from decoded payload message
    :param message_bytes: message bytes
    :param queue_id: queue id to use for storing temp files
    :param file_type: file type to store
    :param store_raw: store raw file or convert to image
    :return: tuple of temp file and checksum
    """

    m = hashlib.sha256()
    m.update(message_bytes)
    file_digest = m.hexdigest()

    upload_dir = ensure_exists(f"/tmp/marie/{queue_id}")
    ext = TYPES_TO_EXT[file_type]

    tmp_file = f"{upload_dir}/{file_digest}.{ext}"

    if store_raw:
        # message read directly from a file
        with open(tmp_file, "wb") as tmp:
            tmp.write(message_bytes)
    else:
        # TODO : This does not handle multipage tiffs
        # convert to numpy array as the message has been passed from base64
        npimg = np.frombuffer(message_bytes, np.uint8)
        # convert numpy array to image
        img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
        cv2.imwrite(tmp_file, img)

    return tmp_file, file_digest


def extract_payload(payload, queue_id) -> tuple[str, str, str]:
    """
    Extract payload from the message. Determine how to extract payload based on the type of the key supplied.

    :param payload:  message payload
    :param queue_id:  queue id to use for storing temp files
    :return:  tuple of bytes and file type
    """

    #
    # Possible keys
    # data, srcData, srcFile, srcUrl, srcBase64, uri

    # This indicates that the contents are a file contents and need to stored as they appear
    store_raw = False
    if "data" in payload or "srcData" in payload:
        raw_data = payload["data"]
        data = base64StringToBytes(raw_data)
    elif "srcBase64" in payload:
        raw_data = payload["srcBase64"]
        data = base64StringToBytes(raw_data)
        store_raw = True
    elif "srcFile" in payload:  # this is a deprecated key and will be removed in future
        img_path = payload["srcFile"]
        # FIXME: relative path resolution is not working as expected
        # FIXME : Use PathManager
        base_dir = FileSystem.get_share_directory()
        path = os.path.abspath(os.path.join(base_dir, img_path))
        logger.info(f"resolved path = {path}")
        if not os.path.exists(path):
            raise Exception(f"File not found : {img_path}")
        with open(path, "rb") as file:
            data = file.read()
        store_raw = True
    elif "uri" in payload or "srcUrl" in payload:
        uri = (
            payload["uri"] if "uri" in payload else payload["srcUrl"]
        )  # for backwards compatibility
        import tempfile

        if not StorageManager.can_handle(uri):
            raise Exception(
                f"Unable to read file from {uri} no suitable storage manager configured"
            )

        # make sure the directory exists
        ensure_exists(f"/tmp/marie")
        # Read remote file to a byte array
        with tempfile.NamedTemporaryFile(
            dir="/tmp/marie", delete=False
        ) as temp_file_out:
            # with open("/tmp/sample.tiff", "w") as temp_file_out:
            if not StorageManager.exists(uri):
                raise Exception(f"Remote file does not exist : {uri}")

            StorageManager.read_to_file(uri, temp_file_out, overwrite=True)
            # Read the file to a byte array
            temp_file_out.seek(0)
            data = temp_file_out.read()
        store_raw = True
    else:
        raise Exception("Unable to determine datasource in payload")

    if not data:
        raise Exception("No data read from payload")

    with io.BytesIO(data) as memfile:
        file_type = imghdr.what(memfile)

    if file_type not in ALLOWED_TYPES:
        raise Exception(f"Unsupported file type, expected one of : {ALLOWED_TYPES}")

    # if we have a tiff file we need to store as RAW otherwise only first page will be converted
    if file_type == "tiff":
        store_raw = True

    tmp_file, file_digest = store_temp_file(data, queue_id, file_type, store_raw)
    # if we don't perform this check our method returns
    # <built-in function print> instead of the actual value <str, str>
    if not isinstance(file_digest, str):
        raise Exception("Checksum is not a string")

    logger.info(f"File info: {file_digest} {file_type}, {tmp_file}")
    return tmp_file, file_digest, file_type


def extract_payload_to_uri(payload, queue_id) -> str:
    """
    Extract payload from the message if it is a raw data key object. if the payload is a uri then return the uri directly

    :param payload:  message payload
    :param queue_id:  queue id to use for storing temp files
    :return:  uri to the stored file
    """

    #
    # Possible keys
    # data, srcData, srcFile, srcUrl, srcBase64, uri

    # This indicates that the contents are a file contents and need to stored as they appear
    store_raw = False
    uri = None

    if "data" in payload or "srcData" in payload:
        raw_data = payload["data"]
        data = base64StringToBytes(raw_data)
    elif "srcBase64" in payload:
        raw_data = payload["srcBase64"]
        data = base64StringToBytes(raw_data)
        store_raw = True
    elif "srcFile" in payload:  # this is a deprecated key and will be removed in future
        img_path = payload["srcFile"]
        # FIXME: relative path resolution is not working as expected
        # FIXME : Use PathManager
        base_dir = FileSystem.get_share_directory()
        path = os.path.abspath(os.path.join(base_dir, img_path))
        logger.info(f"resolved path = {path}")
        if not os.path.exists(path):
            raise Exception(f"File not found : {img_path}")
        with open(path, "rb") as file:
            data = file.read()
        store_raw = True
    elif "uri" in payload or "srcUrl" in payload:
        uri = (
            payload["uri"] if "uri" in payload else payload["srcUrl"]
        )  # for backwards compatibility
    else:
        raise Exception("Unable to determine datasource in payload")

    if uri:
        return uri

    # data was not a uri, so we need to store it locally and then return the URI

    with io.BytesIO(data) as memfile:
        file_type = imghdr.what(memfile)

    if file_type not in ALLOWED_TYPES:
        raise Exception(f"Unsupported file type, expected one of : {ALLOWED_TYPES}")

    # if we have a tiff file we need to store as RAW otherwise only first page will be converted
    if file_type == "tiff":
        store_raw = True

    tmp_file, file_digest = store_temp_file(data, queue_id, file_type, store_raw)
    # if we don't perform this check our method returns
    # <built-in function print> instead of the actual value <str, str>
    if not isinstance(file_digest, str):
        raise Exception("Checksum is not a string")

    logger.info(f"File info: {file_digest} {file_type}, {tmp_file}")
    # convert temp file to uri write
    uri = f"file://{tmp_file}"

    return uri


def value_from_payload_or_args(payload, key, default=None):
    """Get value from payload or from payloads args.
    This is due to compatibility issues with other frameworks we allow passing same arguments in the 'args' object

    :param payload: the payload to extract key from
    :param key: the key to check
    :param default: the default value to assign
    :return:
    """

    ret_type = default
    if key in payload:
        ret_type = payload[key]
    elif "args" in payload and key in payload["args"]:
        ret_type = payload["args"][key]
    return ret_type
