# CRM-DJANGO-REACT


- python -m venv venv
activate environment
- venv\Scripts\activate.bat

desactivate environment
- deactivate

- pip freeze > requirements.txt

start django project
- django-admin startproject  .
    
docker-compose up -d --build

docker-compose down

docker exec -it d8bde4950075 python manage.py migrate

docker exec -it d8bde4950075 python manage.py createsuperuser

