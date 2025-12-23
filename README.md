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

### step 2 - format Bash Scripts

. init_launcher.sh

### step 3 - give permissions

In net-performance-collectors directory launch:

chmod -R 777 .


## B) Docker' Container Installation for Windows environment (Test Purposes)

### Prerequisites

- Docker version > 29.0

### step 1 - build Image using Dockerfile

docker build -t net-performance-image:1.0 .
    
Note: image'name "net-performance-image:1.0" is optional , you can choose the name of the image

### step 2 - create container with mounted directory (using this net-performance-collectors directory)

docker run -it --name net-performance-container -v "$(Get-Location):/app" net-performance-image:1.0 bash

exit

### step 3 - access to Contatiner and create Enviroment "net-performance-container"

docker start -ai net-performance-container

#### step - 3.1 access to Container Enviroment and update
 
In "app" directory launch the following commands:

python -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

. init_launcher.sh

### step 4 (Optional) - run new scripts using container

#### step 4.1 Python

- Create the new Python file, e.g main.py
- Access to container

docker start -ai net-performance-container

- Go to "app" directory
- Activate Python Enviroment:

source .venv/bin/activate

- Add new libraries (if they required e.g Pandas into requirements.txt file)
- Install dependencies:

pip install -r requirements.txt

- Run New script

Python main.py


#### step 4.1 Bash

- Create the new Bash file, e.g runner.sh
- Access to container

docker start -ai net-performance-container

- Go to "app" directory
- Add new file to init_launcher
- Run init_launcher.sh

. init_launcher

- if it is under a directory

dos2unix runner.sh

. runner.sh