from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

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


# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')


# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

######################################################
from sqlalchemy import create_engine

# db_string = "postgres://testing:testing123@:postgres.default.svc.cluster.local/demodb"

# db = create_engine(db_string)


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import psycopg2

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://testing:testing123@:postgres.default.svc.cluster.local/demodb"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Teams(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=datetime.now())
    team_name = db.Column(db.String(30))
    players = db.Column(db.String(30))

db.drop_all()
db.create_all()




from flask import Flask, render_template, request
import psycopg2
import os

db_user = os.environ.get('POSTGRES_USER')
db_psw = os.environ.get('POSTGRES_PASSWORD')
db_host = os.environ.get('SERVICE_POSTGRES_SERVICE_HOST')
database_name = "demo_db"

app = Flask(__name__)

db_con = psycopg2.connect(
            database = database_name,
            user = db_user,
            password = db_psw,
            host = db_host
            port = "5432"
)

db_con.autocommit = True
cursor = db_con.cursor()

query = "CREATE DATABASE demo_db"
cursor.execute(query)

create_table_query = """
CREATE TABLE [IF NOT EXISTS] teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    team_name TEXT NOT NULL,
    players TEXT NOT NULL,
);
"""

db_con.autocommit = True
cursor = db_con.cursor()
cursor.execute(create_table_query)

insert_team1_query = """
INSERT INTO teams (team_name, players) VALUES (?, ?),
('First Team', 'Players for the first team')
)
"""


CREATE TABLE [IF NOT EXISTS] teams (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   team_name TEXT NOT NULL,
   players TEXT NOT NULL,

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM teams').fetchall()
    conn.close()
    return render_template('index.html', teams=teams)






from flask.ext.sqlalchemy import SQLAlchemy
