# Esgrown Backend


## Run Locally (No Docker)

```SQL
/*
We assume you a have local postgresql server running on your machine
Create the database in postgres 
*/

CREATE DATABASE esgrown;
CREATE DATABASE esgrown_test_db;
```

```bash
# clone the repo
# hello world
git clone https://github.com/bwpnigeria/esgrown-python.git

cd esgrown

# create a virtual env
python -m venv 

# activate the virtual env
source esgrown_env/bin/activate

# install all dependencies
pip install -r requirements.txt

# decrypt .env file
git secret reveal

# create migrations
alembic upgrade head

# setup initial data
python initialize.py

# run the app
uvicorn app.main:app --reload

# run tests
pytest

```