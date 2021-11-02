from flask import Flask, render_template, jsonify, request, url_for, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort
import os
import datetime

from sqlalchemy import create_engine, engine

app = Flask(__name__)

# secret key is used to secure sessions, which allow Flask to remember information from one request to another,
# such as moving from the new team page to the index page.
app.config['SECRET_KEY'] = '36sfjsab]Etakt#:GK-nJv'

############ create table and insert two items using ORM method ################
app.config.from_object("config.Config")
db = SQLAlchemy(app)
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    created = db.Column(db.String(50), default=datetime.datetime.now, nullable=True)
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
db.session.close()



####### create db engine ###############################
def get_db_connection():
    db_user = os.environ.get('POSTGRES_USER')
    db_pass = os.environ.get('POSTGRES_PASSWORD')
    db_host = os.environ.get('SERVICE_POSTGRES_SERVICE_HOST')
    db_name = os.environ.get('POSTGRES_DB')
    database_url = 'postgresql://{0}:{1}@{2}/{3}'.format(db_user, db_pass, db_host, db_name)
    db_engine = create_engine(database_url)
    conn = db_engine.connect()
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts where id = {};'.format(post_id)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


############ Display all teams info  (READ) #######
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


############# Display specific team info  (READ) ###########
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


############# Create New Team (CREATE) ###########
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('TeamName is required!')
        else:
            db.session.add(Post(
                title = title,
                content = content,
            ))
            db.session.commit()
            db.session.remove()
            db.session.close()
            return redirect(url_for('index'))

    return render_template('create.html')



############## Edit existing team (UPDATE) ##########
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('TeamName is required!')
        else:
            update_query = f"UPDATE posts SET title = '{title}', content = '{content}' where id = {int(id)}"
            db.session.execute(update_query)
            db.session.commit()
            db.session.remove()
            db.session.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

# @app.route('/<int:id>/edit', methods=('GET', 'POST'))
# def edit(id):
#     post = get_post(id)
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         if not title:
#             flash('TeamName is required!')
#         else:
#             conn = get_db_connection()
#             update_query =f"UPDATE posts SET title = '{title}', content = '{content}' where id = {int(id)}"
#             conn.execute(update_query)
#             conn.co
#             conn.close
#             return redirect(url_for('index'))

#     return render_template('edit.html', post=post)

############### Delete the team (DELETE) ##########
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    delete_query = f"DELETE FROM posts WHERE id = {id};"
    db.session.execute(delete_query)
    db.session.commit()
    db.session.remove()
    db.session.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

# @app.route('/<int:id>/delete', methods=('POST',))
# def delete(id):
#     post = get_post(id)
#     delete_query = f"DELETE FROM posts WHERE id = {id};"
#     conn = get_db_connection()
#     conn.execute(delete_query)
#     conn.close
#     flash('"{}" was successfully deleted!'.format(post['title']))
#     return redirect(url_for('index'))

############# Print the name who visit that hello path #############
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)



if __name__ == '__main__':
    app.debug=True
    app.run()
