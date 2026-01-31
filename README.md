# net-performance-collectors

## A) Linux Environment Installation

### prerequisites

- Python 3
- Iperf3
- net-tools or iproute2
- wget
- dos2unix

### step 1 - install Python Environment and Requirements
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### step 2 - download Firefox driver
python download_firefox_driver.py

### step 3 - format Bash Scripts
. init_launcher.sh

### step 4 - give permissions
In net-performance-collectors directory launch:
chmod -R 777 .


## B) Docker Container Installation

### Prerequisites
Docker version > 29.0

### step 1 - build Image using Dockerfile
docker build -t net-performance-collectors-image:1.1 .

### step 2 - create container with mounted directory (using this net-performance-collectors directory)
docker run -it --name net-performance-collectors-container -p 5000:5000 -p 5678:5678 -v "$(Get-Location):/app" net-performance-collectors-image:1.1 bash

exit

### step 3 - access to Contatiner and create enviroment
docker start -ai net-performance-collectors-container

### step 4 - Python libraries intallation

####  step 4.1  - create environment
python -m venv .venv

####  step 4.2  - activate environment
source .venv/bin/activate

####  step 4.3  - update pip
python -m pip install --upgrade pip

####  step 4.2  - install requirements
pip install -r requirements.txt

### step 5 - Debug
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client "filename".py