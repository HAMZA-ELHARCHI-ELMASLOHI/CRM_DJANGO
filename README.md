# CRM-DJANGO

Django Web application that aims to provide a Client Shop and a manager dashboard attached with invoices and orders

#Setup
## Run on local
```
#Environment
python -m venv venv
venv\Scripts\activate.bat

#install requirement
pip install -r requirements.txt

#migrate Database
python manage.py migrate

#create adminuser
python manage.py createsuperuser

#run the application
python manage.py runserver
```

## Run with docker

```
docker-compose up -d --build
docker-compose up

docker exec -it [app container ID] python manage.py migrate
docker exec -it [app container ID] python manage.py createsuperuser


```
    
add in pg_hba.conf

```
host replication all 0.0.0.0/0 md5
```

docker-compose up


#stop the containers
docker-compose down

docker exec -it d8bde4950075 python manage.py migrate

docker exec -it d8bde4950075 python manage.py createsuperuser

-pg_hba.conf

