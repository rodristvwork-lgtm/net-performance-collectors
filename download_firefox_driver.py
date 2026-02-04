import os
import subprocess
import requests
import tarfile
import io
import platform
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRIVER_NAME = "geckodriver"
DRIVER_PATH = os.path.join(BASE_DIR, DRIVER_NAME)

# Firefox detection
def firefox_installed():
    return shutil.which("firefox") is not None

def get_firefox_version():
    try:
        out = subprocess.check_output(
            ["firefox", "--version"],
            stderr=subprocess.DEVNULL
        ).decode()
        return out.strip().split()[-1]
    except Exception:
        return None

# GeckoDriver detection
def geckodriver_exists():
    return os.path.isfile(DRIVER_PATH)

def get_geckodriver_version():
    try:
        out = subprocess.check_output(
            [DRIVER_PATH, "--version"],
            stderr=subprocess.DEVNULL
        ).decode()
        return out.splitlines()[0]
    except Exception:
        return None

# Architecture detection
def detect_driver_asset(assets):
    system = platform.system().lower()
    arch = platform.machine().lower()

    for asset in assets:
        url = asset["browser_download_url"]

        if system == "linux":
            if arch in ("aarch64", "arm64") and "linux-aarch64.tar.gz" in url:
                return url
            if arch in ("x86_64", "amd64") and "linux64.tar.gz" in url:
                return url
    return None

# GeckoDriver download
def download_geckodriver():
    
    api_url = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
    resp = requests.get(api_url, timeout=10)
    resp.raise_for_status()

    data = resp.json()
    driver_url = detect_driver_asset(data["assets"])

    if not driver_url:
        raise RuntimeError("No compatible GeckoDriver found")

    print("Downloading GeckoDriver:", driver_url)

    bin_resp = requests.get(driver_url, timeout=20)
    bin_resp.raise_for_status()

    with tarfile.open(fileobj=io.BytesIO(bin_resp.content), mode="r:gz") as tar:
        tar.extractall(BASE_DIR)

    os.chmod(DRIVER_PATH, 0o755)

# Firefox update (placeholder)
def update_firefox():
    print("Updating Firefox to latest version...")

# Main logic
def main():
    if not firefox_installed():
        print("firefox not installed")
        return

    firefox_version = get_firefox_version()

    if geckodriver_exists():
        print("driver already exists")
        return
    try:
        download_geckodriver()
        print("driver for firefox installed")
    except Exception:
        update_firefox()
        download_geckodriver()
        print("firefox and driver installed")

if __name__ == "__main__":
    main()