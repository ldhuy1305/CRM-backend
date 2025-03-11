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
├── README.md
├── requirements.txt                        - package
```

### Requirements

- [Python](https://www.python.org/)
- [Git](https://git-scm.com/downloads)
- [Docker](https://store.docker.com/editions/community/docker-ce-desktop-mac) >= 17.12

## Installation

Config environment for Django System in django .env file (`src/.env`)

```bash
cd src2
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
## Command

```bash
cd src2

# create app
python manage.py startapp app

# create supper user
python manage.py createsuperuser

# make migrations
python manage.py makemigrations

# apply migrations
python manage.py migrate

# run server
python manage.py runserver
```

## Command

```bash
cd src2

# create app
python manage.py startapp app

# create supper user
python manage.py createsuperuser

# make migrations
python manage.py makemigrations

# apply migrations
python manage.py migrate

# run server
python manage.py runserver
```