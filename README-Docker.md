# Docker Container for windows

## Prerequisites
Docker version > 29.0

## step 1 - Build Image using Dockerfile
docker build --no-cache -t net-performance-collectors-image:1.4 .

## step 2 - Create container with mounted directory (using this net-performance-collectors directory)
docker run -it --name net-performance-collectors-container -p 5000:5000 -p 5678:5678 -p 5900:5900 -v "$(Get-Location):/app" net-performance-collectors-image:1.4

exit

## step 3 - Access to Contatiner and create enviroment
docker start -ai net-performance-collectors-container

## (optional)Add certification
docker cp "<< path of certificate>>" net-performance-collectors-container:/usr/local/share/ca-certificates/corp-root.crt

e.g:

    docker cp "C:\certs\corp-root-zscaler.cer" net-performance-collectors-container:/usr/local/share/ca-certificates/corp-root.crt

then inside the container run:

    update-ca-certificates

### (optional) - access in another console
docker exec -it net-performance-collectors-container bash

## step 4 - Python libraries intallation

###  step 4.1  - create environment
python -m venv .venv

###  step 4.2  - activate environment
source .venv/bin/activate

###  step 4.3  - update pip
python -m pip install --upgrade pip

###  step 4.4  - install requirements
pip install -r requirements.txt

###  step 4.5  Download/Update Firefox driver ("geckodriver")
(keep active Python environment)

python download_firefox_driver.py

### (optional) - all in one line
python -m venv .venv && source .venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt  && python download_firefox_driver.py

## (optional) - For Debug
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client "filename".py


# B) Docker Container Configs

## WebB

## For VNC Viewer

Launch these comands container console:

export DISPLAY=:0
disable headless option
