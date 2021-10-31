from flask import Flask, render_template, jsonify, request, url_for, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort
import os

#import psycopg2

app = Flask(__name__)
# app.config['SECRET_KEY'] = '36G8]Etakt#:GK-nJv'

# db_user = os.environ.get('POSTGRES_USER')
# db_pass = os.environ.get('POSTGRES_PASSWORD')
# db_host = "postgres"
# #db_host = os.environ.get('SERVICE_POSTGRES_SERVICE_HOST')


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/flask_db'.format(
#     db_user, db_pass, db_host
# )

app.config.from_object("config.Config")

db = SQLAlchemy(app)

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(50), nullable=False)
    players = db.Column(db.String(50), nullable=False)

db.drop_all()
db.create_all()
# # db.session.commit()

db.session.add(Team(
    team_name = "INDIA",
    players = 'virat, rohit',
))

db.session.add(Team(
    team_name = "England",
    players = 'maxwel, rohit',
))

db.session.commit()
db.session.remove()

# s_tb_name = "teams"
# ls_cols = ["team_name", "players"]
# ls_vals = ["('INDIA', 'virat, rohit')",
#             "('Australia', 'Maxwell, Hayden')"]
# s_cols = ', '.join(ls_cols)
# s_vals = ', '.join(ls_vals)
# session.execute(f"INSERT INTO {s_tb_name} ({s_cols}) VALUES {s_vals}")

# from sqlalchemy import create_engine
# db_string = 'postgresql://{0}:{1}@{2}/demo_db'.format(db_user, db_pass, db_host)

# db = create_engine(db_string)

# # Create 
# db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")  
# db.execute("INSERT INTO films (title, director, year) VALUES ('Doctor Strange', 'Scott Derrickson', '2016')")

# # Read
# result_set = db.execute("SELECT * FROM films")  
# for r in result_set:  
#     print(r)


# @app.route('/')
# def hello():
#     return "Hello Everyone"

@app.route('/hello/<name>')
def hello_name(name):
    return "Welcome to SRE Demo " + str(name)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/ping')
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        

# @app.route('/prereg', methods=['POST'])
# def prereg():
#     email = None
#     if request.method == 'POST':
#         email = request.form['email']
#         # Check that email does not already exist (not a great query, but works)
#         if not db.session.query(User).filter(User.email == email).count():
#             reg = User(email)
#             db.session.add(reg)
#             db.session.commit()
#             return render_template('success.html')
#     return render_template('index.html')


if __name__ == '__main__':
    app.debug=True
    app.run()
