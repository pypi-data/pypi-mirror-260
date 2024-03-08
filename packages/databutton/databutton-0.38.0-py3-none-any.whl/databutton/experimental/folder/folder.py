import io
import os
import zipfile

import databutton as db


def zip_folder_to_bytes(folder_path: str) -> bytes:
    """Zip the contents of a folder and return as bytes."""
    zip_bytes = io.BytesIO()  # Use BytesIO as a buffer
    with zipfile.ZipFile(zip_bytes, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(
                    file_path,
                    os.path.relpath(file_path, os.path.join(folder_path, "..")),
                )
    zip_bytes.seek(0)  # Go to the start of the BytesIO buffer
    return zip_bytes.getvalue()


def unzip_bytes_to_folder(bytes_data: bytes, extract_path: str):
    """Unzip bytes into a folder."""
    # Ensure the extraction path exists
    os.makedirs(extract_path, exist_ok=True)
    zip_bytes = io.BytesIO(bytes_data)
    with zipfile.ZipFile(zip_bytes, "r") as zip_ref:
        zip_ref.extractall(extract_path)


def upload(key: str, folder_path: str):
    """Zip and upload a folder to blob storage."""
    zipped_bytes = zip_folder_to_bytes(folder_path)
    db.storage.binary.put(key, zipped_bytes)


def download(key: str, folder_path: str):
    """Download and unzip a folder from blob storage."""
    zipped_bytes = db.storage.binary.get(key)
    if zipped_bytes is not None:
        # Ensure the target folder exists before extraction
        os.makedirs(folder_path, exist_ok=True)
        unzip_bytes_to_folder(zipped_bytes, folder_path)
