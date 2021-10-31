from flask import Flask, render_template, jsonify, request, url_for, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort
import os

from sqlalchemy import create_engine, engine
app = Flask(__name__)

import os

db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
db_host = "postgres_new"
#db_host = os.environ.get('SERVICE_POSTGRES_SERVICE_HOST')
database_url = 'postgresql://{0}:{1}@{2}/post_db'.format(db_user, db_pass, db_host)

app.config.from_object("config.Config")
db = SQLAlchemy(app)
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(50), nullable=False)
db.drop_all()
db.create_all()
db.session.add(Post(
    title = "INDIA",
    content = 'virat, rohit',
))

db.session.add(Post(
    title = "England",
    content = 'maxwel, rohit',
))

db.session.commit()
db.session.remove()


db_engine = create_engine(database_url)


@app.route('/')
def index():
    conn = db_engine.connect()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

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

# @app.route('/')
# def index():
#     return render_template('test.html')

@app.route('/ping')
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

# @app.route('/test', methods=['POST'])
# def test():
#     if request.method == 'POST':
        

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
