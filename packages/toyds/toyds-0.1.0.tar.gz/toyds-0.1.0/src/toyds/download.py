import tarfile

from toyds.constants import CACHE_DIR

from os import path, makedirs
from tqdm import tqdm
import os
import subprocess
from urllib import request
import zipfile
import shutil

def dl(link: str):
    if ":" in link:
        return dl_scp_file(link)
    else:
        return dl_http_file(link)


def dl_scp_file(link: str):
    """
    Downloads a file using rsync and scp subprocess

    hostname:runs/nanodrz/nanodrz/1705840799/0013500.pt

    Use rsync --partial --progress --human-readable -e ssh to download the file.
    """
    if ":" not in link:
        raise "Invalid scp path"

    file_path = path.join(CACHE_DIR, link.split(":")[-1])

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Use rsync --partial --progress --human-readable -e ssh
    cmd = [
        "rsync",
        "--partial",
        "--progress",
        "--human-readable",
        "-e",
        "ssh",
        link,
        file_path,
    ]
    print(" ".join(cmd))
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        text=True,
    )

    for line in process.stdout:
        print(line, end="")

    process.wait()

    return file_path


def dl_http_file(link: str):
    file_path = path.join(CACHE_DIR, path.basename(link))

    current_size = 0
    expected_size = int(request.urlopen(link).headers.get("content-length", 0))

    if os.path.exists(file_path):
        current_size = os.path.getsize(file_path)

        if current_size == expected_size:
            return file_path

    headers = {"Range": f"bytes={current_size}-"}
    req = request.Request(link, headers=headers)

    with request.urlopen(req) as response, open(file_path, "ab") as file:
        block_size = 1024 * 1024
        progress_bar = tqdm(
            total=expected_size - current_size,  # Adjust total size
            initial=current_size,
            desc=link,
            unit="B",
            unit_scale=True,
            leave=False,
        )

        while True:
            data = response.read(block_size)
            if not data:
                break
            progress_bar.update(len(data))
            file.write(data)

        progress_bar.close()

    return file_path


