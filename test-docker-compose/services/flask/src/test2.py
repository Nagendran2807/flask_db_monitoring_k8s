import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
# secret key is used to secure sessions, which allow Flask to remember information from one request to another,
# such as moving from the new team page to the index page.
app.config['SECRET_KEY'] = '36G8]Etakt#:GK-nJv'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_team(team_id):
    conn = get_db_connection()
    team_info = conn.execute('SELECT * FROM teams WHERE id = ?',
                        (team_id,)).fetchone()
    conn.close()
    if team_info is None:
        abort(404)
    return team_info

@app.route('/')
def index():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM teams').fetchall()
    conn.close()
    return render_template('index.html', teams=teams)

@app.route('/<int:team_id>')
def team(team_id):
    team_info = get_team(team_id)
    return render_template('team.html', team=team_info)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        team_name = request.form['title']
        players = request.form['content']

        if not team_name:
            flash('Team Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO teams (team_name, players) VALUES (?, ?)',
                         (team_name, players))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    team_info = get_team(id)

    if request.method == 'POST':
        team_name = request.form['title']
        players = request.form['content']

        if not team_name:
            flash('TeamName is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE teams SET team_name = ?, players = ?'
                         ' WHERE id = ?',
                         (team_name, players, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', team=team_info)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    team_info = get_team(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM teams WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(team_info['team_name']))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug=True
    # run() method of Flask class runs the application
    # on the local development server
    app.run()