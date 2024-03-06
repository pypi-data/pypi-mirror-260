import hashlib
import json
import os
import warnings
from pathlib import Path

import requests


def checksum(file_path):
    md5_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            md5_hash.update(data)

    return md5_hash.hexdigest()


def filesize(file_path):
    file_size = os.path.getsize(file_path)
    return file_size


def read_url_json(url, headers):  # pragma: no cover
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def download_url(url, target, headers):
    response = requests.get(url, headers=headers, stream=True)

    has_tqdm = True
    try:
        from tqdm import tqdm
    except ModuleNotFoundError:  # pragma: no cover
        has_tqdm = False

    if response.status_code == 200:
        with open(target, "wb") as file:
            if has_tqdm:
                file_size = int(response.headers.get('content-length', 0))
                desc = "(Unknown total file size)" if file_size == 0 else ""
                with tqdm(
                        total=file_size, unit='iB', unit_scale=True
                ) as bar:
                    for data in response.iter_content(chunk_size=1024):
                        size = file.write(data)
                        bar.update(size)
            else:
                for data in response.iter_content(chunk_size=1024):  # pragma: no cover
                    size = file.write(data)

        response.close()
    else:
        server_err = json.loads(response.content.decode('utf-8'))
        reason = server_err.get('reason', '')
        e = ValueError(f"Failed to download the file. Status code: {response.status_code}, reason: {reason}")
        response.close()
        raise e


def upload_to_url(upload_url, file_path, headers, params, name):  # pragma: no cover
    try:
        from tqdm import tqdm
        from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
        has_progress_bar = True
    except ModuleNotFoundError:
        warnings.warn('You need to install tqdm and requests_toolbelt to see upload progress bar.')
        has_progress_bar = False

    if has_progress_bar:
        path = Path(file_path)
        total_size = path.stat().st_size
        fields = {}
        with tqdm(
                desc=f'Uploading {name}',
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            with open(file_path, "rb") as f:
                fields["file"] = ("dataset-sh-file", f)
                e = MultipartEncoder(fields=fields)
                m = MultipartEncoderMonitor(
                    e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
                )
                headers["Content-Type"] = m.content_type
                response = requests.post(upload_url, data=m, headers=headers, params=params)


    else:
        with open(file_path, 'rb') as f:
            response = requests.post(
                upload_url,
                headers=headers,
                params=params,
                files={'file': ('data', f)}
            )
    response.raise_for_status()
