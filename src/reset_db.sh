source ../venv/bin/activate
source ../.envrc
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py populate_models