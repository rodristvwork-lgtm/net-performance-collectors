import os, subprocess, requests, tarfile, io
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService

# get Firefox version
def get_firefox_version():
    
    out = subprocess.check_output(["firefox", "--version"]).decode()
    return out.strip().split()[-1] # e.g -> "Mozilla Firefox 131.0"

# download GeckoDriver
def fetch_arm64_geckodriver(version):
    
    # GeckoDriver taken from official GitHub
    url = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
    data = requests.get(url).json()
    driver_url = None
    
    for asset in data["assets"]:
        if "linux-aarch64.tar.gz" in asset["browser_download_url"]:
            driver_url = asset["browser_download_url"]
            break
        
    if not driver_url:
        raise RuntimeError(f"No ARM64 GeckoDriver found for current Firefox {version}")

    print("downloading...", driver_url)
    
    resp = requests.get(driver_url)
    
    tar = tarfile.open(fileobj=io.BytesIO(resp.content), mode="r:gz")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
     
    tar.extractall(base_dir)
    tar.close()

    return os.path.join(base_dir, "geckodriver")

# launch Firefox with Selenium

def launch_firefox():
    
    version = get_firefox_version()
    driver_path = fetch_arm64_geckodriver(version)
    service = FirefoxService(driver_path)
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=service, options=options)
    
    return driver

# Run
if __name__ == "__main__":
    try:
        
        driver = launch_firefox()
        print("driver downloaded")
    except Exception as e:
        print("Error:", e)