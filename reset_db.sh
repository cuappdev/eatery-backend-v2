source venv/bin/activate
source .envrc
python3 src/manage.py makemigrations
python3 src/manage.py migrate