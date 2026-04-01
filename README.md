# net-performance-collectors version2

##  Installation

#### Get collectors

git clone -b version2 https://github.com/rodristvwork-lgtm/net-performance-collectors.git

#### 1.Create environment
python3 -m venv .venv

#### 2. Activate environment
source .venv/bin/activate

#### 3. Update pip
python -m pip install --upgrade pip

#### 4. Install requirements
pip install -r requirements.txt

#### 5. download/update Firefox driver ("geckodriver")
(keep active Python environment)

python download_firefox_driver.py

#### (optional) Format Bash Scripts for Crontab jobs
. init_launcher.sh

#### (optional) Permissions for Crontab jobs
chmod -R 777 .

#### (optional) - 1. , 2. ,3. all in one line
python -m venv .venv && source .venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt