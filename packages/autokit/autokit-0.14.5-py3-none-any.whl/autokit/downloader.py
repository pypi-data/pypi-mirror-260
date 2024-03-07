import os

import requests
import zipfile
import tempfile
from pathlib import Path


def download(tool_directory: Path, url: str, chunk_size=1024, progress_callback=None) -> None:
    """
    Downloads a zip file from the given URL and extracts it.

    :param tool_directory: The directory where the tool will be installed.
    :param url: The URL of the zip file.
    :param chunk_size: The size of the download chunks.
    :param progress_callback: A callback function to track the download progress.
    """
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    bytes_downloaded = 0

    # get the filename from the URL by splitting it at the last '/' and removing any query parameters
    filename = url.split('/')[-1].split('?')[0]

    progress_context = type('', (), {})()

    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as fp:
        temp_file_name = fp.name
        for chunk in response.iter_content(chunk_size=chunk_size):
            bytes_downloaded += len(chunk)
            fp.write(chunk)
            if progress_callback:
                progress_callback(progress_context, filename, bytes_downloaded, total_size_in_bytes)

    if progress_callback:
        progress_callback(progress_context, filename, total_size_in_bytes, total_size_in_bytes)

    with zipfile.ZipFile(temp_file_name, 'r') as zip_ref:
        zip_ref.extractall(tool_directory)

    os.remove(temp_file_name)
