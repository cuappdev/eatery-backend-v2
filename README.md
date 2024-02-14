# eatery-blue-backend

This is the backend for eatery-blue-backend.

# Postgres Setup

---

- Install PostgresSQL here at https://www.postgresql.org/download/
- Login to postgres via command line by entering `psql postgres`
- Create the eatery database via `create database "eatery-dev";`
- Quit psql via `\q`
- Create an `.envrc` file and fill out the environment variables from the `.envrctemplate` file corresponding to your local postgres database
- To set up the tables and data, make sure current working directory is the `src` folder and run `bash reset_db.sh`
- To run the backend, run `bash start.sh`

## SP24 Members

- Thomas Vignos
- Aayush Agnihotri

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
