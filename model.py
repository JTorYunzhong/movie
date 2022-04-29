import sqlite3

conn = sqlite3.connect('Info.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Movies ''')
cur.execute('''DROP TABLE IF EXISTS Actors ''')
cur.execute('''DROP TABLE IF EXISTS Movies_actors ''')

cur.execute('''CREATE TABLE IF NOT EXISTS Movies
    (Id INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, Year INTEGER,
     Genre TEXT,  
     Plot BLOB, ImdbRating TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Actors
    (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT UNIQUE)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Movies_actors
    (Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Movie_id INTEGER, Actor_id INTEGER,
    FOREIGN KEY(Movie_id) REFERENCES Movies(Id),
    FOREIGN KEY(Actor_id) REFERENCES Actors(Id)
    )''')

cur.close()

print("Database initialized.")