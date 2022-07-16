virtualenv -p `which python3.10` venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 ./manage.py migrate
