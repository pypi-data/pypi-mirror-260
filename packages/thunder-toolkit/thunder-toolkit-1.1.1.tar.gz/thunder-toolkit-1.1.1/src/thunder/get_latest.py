import os
import requests
import urllib.request  # download into memory
import hashlib  # for hashing
import gzip  # for decompressing
import platform  # which OS
import distro  # which linux distribution
from colorama import Fore, Style


# Pulling latest binary from gcs
def get_latest(version, path):
    if version != "host" and version != "client":
        return None

    # Validate the platform we're trying to run on
    operating_system = platform.system().lower()
    print(f"Operating System = {operating_system}")
    if version == "host" and operating_system != "windows":
        print(
            Fore.RED
            + "Error: Thunder hosting only supported on Windows machines"
            + Style.RESET_ALL
        )
        exit(1)
    elif version == "client" and operating_system != "linux":
        print(
            Fore.RED
            + "Error: Thunder client only supported on Linux machines"
            + Style.RESET_ALL
        )
        exit(1)

    architecture = platform.machine().lower()
    if operating_system == "linux":
        distribution = distro.id().lower()

    metadata_url = f"https://storage.googleapis.com/storage/v1/b/thunder_binary/o/{version}_{operating_system}_{architecture}?alt=json"
    latest_metadata = requests.get(metadata_url).json().get("metadata")
    if latest_metadata == None:
        print("Cannot find metadata of latest binary")
        return None

    latest_hash = latest_metadata.get("hash")
    if latest_hash == None:
        print("Cannot find hash of latest binary")
        return None

    # Check if we already have latest binary
    if os.path.isfile(path):
        current_hash = hashlib.md5(open(path, "rb").read()).hexdigest()
        print(f"Current Hash = {current_hash}")
        if current_hash == latest_hash:
            return path

    download_url = f"https://storage.googleapis.com/thunder_binary/{version}_{operating_system}_{architecture}"
    print("PULLING FROM ", download_url)
    compressed_data = urllib.request.urlopen(download_url).read()
    decompressed_data = gzip.decompress(compressed_data)
    with open(path, "wb") as f:
        f.write(decompressed_data)

    print(f"Downloaded latest {version} binary to {path}")
    return path


# For host desktop app
if __name__ == "__main__":
    get_latest("host", "C:\\Users\\gpugang\\Desktop\\thunder\\main.exe")
