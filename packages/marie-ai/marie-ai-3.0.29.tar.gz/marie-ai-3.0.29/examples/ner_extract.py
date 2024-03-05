import base64
import os
import threading
import time
import uuid

import requests

from examples.utils import online, setup_queue
from marie.utils.utils import ensure_exists

api_base_url = "http://127.0.0.1:51000/api"
default_queue_id = "0000-0000-0000-0000"
api_key = "mau_t6qDi1BcL1NkLI8I6iM8z1va0nZP01UQ6LWecpbDz6mbxWgIIIZPfQ"

auth_headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json; charset=utf-8",
}


def process_extract(
    queue_id: str, mode: str, file_location: str, stop_event: threading.Event = None
) -> str:
    if not os.path.exists(file_location):
        raise Exception(f"File not found : {file_location}")
    endpoint_url = f"{api_base_url}/ner/extract"
    print(endpoint_url)

    if False and not online(api_base_url):
        stop_event.set()
        raise Exception(f"API server is not online : {endpoint_url}")

    # Prepare file for upload
    with open(file_location, "rb") as file:
        encoded_bytes = base64.b64encode(file.read())
        base64_str = encoded_bytes.decode("utf-8")

    uid = str(uuid.uuid4())
    queue_id = "0000-0000-0000-0000"

    json_payload = {
        "queue_id": queue_id,
        "data": base64_str,
        # "uri": "s3://marie/incoming/PID_1764_8829_0_179519650.tif",
        "mode": mode,
        "output": "json",
        "doc_id": f"extract-{uid}",
        "doc_type": "lbx",
        # "features": [{"type": "LABEL_DETECTION", "maxResults": 1}],
    }

    # print(json_payload)
    # Upload file to api
    print(f"Uploading to marie-ai for processing : {file}")
    print(endpoint_url)

    NITER = 1
    json_result = None

    for k in range(NITER):
        start = time.time()
        result = requests.post(
            endpoint_url,
            headers=auth_headers,
            json=json_payload,
        )

        if result.status_code != 200:
            stop_event.set()
            raise Exception(f"Error : {result}")

        json_result = result.json()
        print(json_result)
        delta = time.time() - start
        print(f"Elapsed : {delta:.2f} seconds")

    return json_result


if __name__ == "__main__":
    stop_event = threading.Event()

    setup_queue(
        api_key,
        "ner",
        "ner.#",
        stop_event,
        ["ner.completed", "ner.failed"],
        lambda x: print(f"callback: {x}"),
    )

    # Specify the path to the file you would like to process
    src = os.path.expanduser("~/tmp/PID_1028_7826_0_157684456.tif")
    src = os.path.expanduser("~/tmp/PID_1925_9289_0_157186264.png")
    print(src)

    json_result = process_extract(
        queue_id=default_queue_id,
        mode="multiline",
        file_location=src,
        stop_event=stop_event,
    )

    print(json_result)
