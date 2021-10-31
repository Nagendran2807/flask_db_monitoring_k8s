from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# app.config.from_pyfile('config.cfg')

# db = SQLAlchemy()
# db.init_app(app)

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String())
#     surname = db.Column(db.String())

# @app.route('/test')
# def test():
#     return 'Hello World! I am from docker!'

# @app.route('/test_db')
# def test_db():
#     db.create_all()
#     db.session.commit()
#     user = User.query.first()
#     if not user:
#         u = User(name='Mudasir', surname='Younas')
#         db.session.add(u)
#         db.session.commit()
#     user = User.query.first()
#     return "User '{} {}' is from database".format(user.name, user.surname)

app = Flask(__name__)

db_user = os.environ.get('POSTGRES_DB_USER')
db_psw = os.environ.get('POSTGRES_DB_PSW')
db_host = os.environ.get('SERVICE_POSTGRES_SERVICE_HOST')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/launchpage'.format(
    db_user, db_psw, db_host
)
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email