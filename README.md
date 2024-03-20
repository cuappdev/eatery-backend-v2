# eatery-blue-backend

This is the backend for eatery-blue-backend.

# Postgres Setup

---

- Install PostgresSQL here at https://www.postgresql.org/download/
- Login to postgres via command line by entering `psql postgres`
- Create the eatery database via `create database "eatery-dev";`
- Quit psql via `\q`
- Create an `.envrc` file and fill out the environment variables from the `.envrctemplate` file corresponding to your local postgres database
- Create a python virtual environment in the root directory by running `python3 -m venv venv` and then activate it by running `source venv/bin/activate` (MacOS) or `venv\Scripts\activate` (Windows)
- Install the required dependencies by running `pip3 install -r requirements.txt`
- Load the environment variables by running `source .envrc`
- To set up the tables and data (or if reseting the database), make sure current working directory is the `src` folder and run `python3 manage.py makemigrations; python3 manage.py migrate; python3 manage.py populate_models`
- To run the backend, run `python3 manage.py runserver 0.0.0.0:8000` (Ensuring the env variables are loaded and all dependencies are installed)

## SP24 Members

- Thomas Vignos
- Aayush Agnihotri
- Daniel Weiner

## FA23 Members

- Mateo Weiner
- Thomas Vignos

## SP23 Members

- Mateo Weiner
- Kidus Zegeye

## FA22 Members

- Marya Kim
- Sasha Loayza

## SP22 Members

- Marya Kim
- Archit Mehta
