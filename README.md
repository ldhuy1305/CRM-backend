# Customer Relationship Management

## Project structure

```shell
.
└── src
    ├── api                                 - app main
    |   |── constants
    |   |    ├── constant.py
    |   |    ├── error_code.py
    │   |    ├── message.py
    │   ├── asgi.py
    │   ├── wsgi.py
    │   ├── urls.py
    │   └── settings.py
    ├── authentication                      - app authentication
    │   ├── migrations
    │   ├── admin.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── views.py
    ├── {other_app}                         - other app
    ├── utilities
    ├── .env
    ├── .env.example
    ├── .pre-commit-config.yaml             - fomatter code
    ├── cronjob.sh                          - cronjob file
    ├── manage.py                           - manager project
├── docker
    ├── docker-compose.yml                  - Docker compose
    ├── Dockerfile                          - Dockerfile
├── src 
├── README.md
├── requirements.txt                        - package
```

## Installation

Config environment for Django System in django .env file (`src/.env`)

```bash
cd src
cp .env.example .env
```
### Setup virtual envirement (venv) support project

```bash
# Create virtual venv
python3 -m venv venv

# Active venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

#### Add new package
```bash
# Active venv
source venv/bin/activate

# Install package_name
pip install package_name

# Add new package and dependenci to requirements.txt
pip freeze > requirements.txt

```


#### Remove new package
```bash
# Active venv
source venv/bin/activate

# Uninstall package_name
pip uninstall package_name

# Remove package from requirements.txt
pip freeze > requirements.txt

```

## Setup cronjob
```bash
# Using Cronjob in server (Run Script File)
source cronjob.sh
#or
. cronjob.sh

# Using crontab -l to check cronjob
crontab -l
```

## Formatter

```bash
pre-commit run --all-files
```

## Command

```bash
cd src

# create app
python manage.py startapp app

# make migrations
python manage.py makemigrations

# apply migrations
python manage.py migrate

# create master data group permission
python manage.py create_group_permission

# create fixtures data
python manage.py load_data

# create supper user
python manage.py createsuperuser

# run server
python manage.py runserver
```
