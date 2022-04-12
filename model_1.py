import sqlite3

conn = sqlite3.connect('info.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Movies ''')
cur.execute('''DROP TABLE IF EXISTS Actors ''')
cur.execute('''DROP TABLE IF EXISTS Cast ''')

cur.execute('''CREATE TABLE IF NOT EXISTS Movies
    (id INTEGER PRIMARY KEY, title TEXT, year INTEGER,
     genre TEXT, actor TEXT, 
     plot BLOB, rottenTomatoes TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Actors
    (id INTEGER PRIMARY KEY, name TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Cast
    (movie_id INTEGER, actor_id INTEGER)''')
cur.close()