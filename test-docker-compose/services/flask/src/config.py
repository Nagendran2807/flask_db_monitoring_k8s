import os

db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
db_host = "postgres_new"
#db_host = os.environ.get('SERVICE_POSTGRES_SERVICE_HOST')

database_url = 'postgresql://{0}:{1}@{2}/post_db'.format(db_user, db_pass, db_host)

class Config(object):
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False