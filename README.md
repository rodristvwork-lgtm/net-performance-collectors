# net-performance-collectors

## Linux Environment Installation

### Prerequisites
- Python 3
- Iperf3
- net-tools or iproute2
- wget
- dos2unix (optional)

### Step 1 - Install Python Environment and Requirements

python -m venv .venv
pip install -r requirements.txt

### Step 2 - Format Bash Scripts

. init_launcher.sh

### Step 3 - Run sh scripts manually (Optional)

. iperf_launcher.sh
. ping_launcher.sh
. wget_launcher.sh

## Container Docker Installation

### Prerequisites
- Docker version > 29.0

### Step 1 - Build Image using Dockerfile

docker build -t net-performance-image:1.0 .
    Note: image "net-performance-image:1.0" is optional , you can choose the name of the image

### Step 2 - Create container with mounted directory (using this net-performance-collectors directory)

docker run -it --name net-performance-container -v C:<path>\net-performance-collectors:/app net-performance-image:1.0 bash 
    
    e.g docker run -it --name net-performance-container -v C:\user\python\net-performance-collectors:/app net-performance-image:1.0 bash

### step 3 - Access to Contatiner "net-performance-container"

docker start -ai net-performance-container


### step 4 - Inside the container run Scripts manually

- go to "app" directory , cd app
- create Python Environment: python3 -m venv .venv
- run init_launcher.sh
- (optional) run net performance scripts e.g iperf_launcher.sh