# CRM-DJANGO-REACT


- python -m venv venv
activate environment
- venv\Scripts\activate.bat

desactivate environment
- deactivate

- pip freeze > requirements.txt

start django project
- django-admin startproject  .
    

docker-compose up

docker-compose up -d --build

docker-compose down

docker exec -it d8bde4950075 python manage.py migrate

docker exec -it d8bde4950075 python manage.py createsuperuser

# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

#CMD gunicorn Django-CRM.wsgi.application --bind 0.0.0.0:$PORT


heroku container:release -a radiant-lake-93774 web
heroku logs --tail -a radiant-lake-93774

git:remote -a radiant-lake-93774