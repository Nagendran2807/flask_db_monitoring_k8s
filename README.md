# flask_db_monitoring_k8s



minikube image load  <image-nme>  #### push local docker images to minikube ####

eval $(minikube docker-env)  ### reuse the Docker daemon from Minikube

SQLAlchemy offers several benefits over the raw SQL approach, including:

Cleaner code: Having SQL code as Python strings gets messy pretty quickly,
More secure code: Using SQLAlchemy's ORM functionalities can help mitigate against vulnerabilities such as SQL injection,
Simpler logic: SQLAlchemy allows us to abstract all of our database logic into Python objects. Instead of having to think on a table, row, and column level, we can consider everything on a class, instance, and attribute level.


kubectl run hello-foo --image=foo:0.0.1 --image-pull-policy=Never



psql -h localhost -U postgres -d postgres -p 5432

psql -h localhost -U db_user --password 123sdff -p 5432

psql -h localhost -U 'db_user' --password '123sdff' -p 5432 --dbname demo_db

psql -h 10.6.35.83 -U postgresadmin --pas -p 31768 postgresdb



from flask import Flask, render_template, request
import psycopg2
import os 

db_user = "postgres"
db_psw = "postgres"
db_host = os.environ.get('SERVICE_POSTGRES_SERVICE_HOST')
database_name = "postgres"


db_con = psycopg2.connect(
            database = database_name,
            user = "postgres",
            password = "postgres",
            host = "10.103.75.25",
            port = "5432"
)

psycopg2.connect("dbname=postgres user=postgres host=10.103.75.25 password=postgres port=5432")


psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="postgres", port ="5432")

dnsutils

iputils-ping

create user postgres with superuser password 'postgres';

psql "postgresql://postgres:pass1234@$localhost/postgres"


pod_name=$(kubectl get po -l db=postgres -o jsonpath="{.items[0].metadata.name}")
kubectl exec -it $pod_name -it -- psql -U postgres