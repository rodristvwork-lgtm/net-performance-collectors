# net-performance-collectors

## Linux Environment Installation
set +e
### Prerequisites

- Python 3
- Iperf3
- net-tools or iproute2
- wget
- dos2unix

### Step 1 - Install Python Environment and Requirements

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### Step 2 - Format Bash Scripts

. init_launcher.sh

### Step 3 - Run sh scripts manually (Optional)

. iperf_launcher.sh
. ping_launcher.sh
. wget_launcher.sh

## Container Docker Installation in Windows environment (Test Purposes)

### Prerequisites

- Docker version > 29.0

### Step 1 - Build Image using Dockerfile

docker build -t net-performance-image:1.0 .
    
Note: image'name "net-performance-image:1.0" is optional , you can choose the name of the image

### Step 2 - Create container with mounted directory (using this net-performance-collectors directory)

docker run -it --name net-performance-container -v "$(Get-Location):/app" net-performance-image:1.0 bash
exit

### step 3 - Access to Contatiner and create Enviroment "net-performance-container"

docker start -ai net-performance-container

#### step 3.1 Access to Container Enviroment and update
 
 - In "app" directory launch the following commands:

python -m venv .venv
pip install -r requirements.txt
. init_launcher.sh
(optional) run net performance scripts e.g iperf_launcher.sh