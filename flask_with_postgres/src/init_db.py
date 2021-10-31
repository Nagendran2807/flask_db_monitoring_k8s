import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO teams (team_name, players) VALUES (?, ?)",
            ('First Team', 'Players for the first team')
            )

cur.execute("INSERT INTO teams (team_name, players) VALUES (?, ?)",
            ('Second Team', 'Players for the second team')
            )

connection.commit()
connection.close()