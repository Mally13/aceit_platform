# Project Setup

This guide will help you set up the AceIt Platform API project on your local machine for development and testing purposes.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.9 or higher
- PostgreSQL
- Git

## Steps to Set Up the Project

### 1. Clone the Repository;

First, clone the repository from GitHub to your local machine

### 2. Create and activate the virtual environment
```
virtualenv venv
source venv/bin/activate
```

### 3. Install Dependancies
```
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database
- Open the PostgreSQL shell:
bash
```
psql
```
- Create a new database:
```
CREATE DATABASE aceit_db;
```

- Create a new user with a password:
```
CREATE USER aceit_user WITH PASSWORD 'your_password';
```

- Grant all privileges on the database to the new user:
```
GRANT ALL PRIVILEGES ON DATABASE aceit_db TO aceit_user;
```
### 5. Configure Django Settings
Update the database settings in ./aceit/aceit/settings.py to match your PostgreSQL setup:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aceit_db',
        'USER': 'aceit_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```