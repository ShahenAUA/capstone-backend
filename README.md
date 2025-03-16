# capstone-backend

## The prerequisites
1. Python installed
2. A running MySQL server with already created database named `pet_welfare`

### (Optional) steps to setup virtual environment
``` sh
python -m venv .venv
.venv\scripts\activate
```

## To install the packages run
``` sh
pip install -r requirements.txt
```

## Do not forget to copy the content of `pet_welfare/secrets.example.py` into `pet_welfare/secrets.py` and adjust the values for your configuration

## Make sure to run the migrations of the database
``` sh
py manage.py migrate
```

## Finally run the server
``` sh
py manage.py runserver
```
