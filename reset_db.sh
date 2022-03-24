source env/bin/activate
source .env
python3 src/manage.py makemigrations
python3 src/manage.py migrate