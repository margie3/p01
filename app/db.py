import sqlite3
import csv

DB_FILE = "casino.db"

# Function to create a new database connection per request (Flask-friendly)
def get_db():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    return db

# Makes tables in the database (run this once, or after changes)
def makeDb():
    db = get_db()
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, balance INTEGER")
    c.execute("CREATE TABLE IF NOT EXISTS scores (username TEXT, game TEXT, score INTEGER)")
    db.commit()

# Registers a user with a username and password
def addUser(u, p):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, 100)"(u,p))
    db.commit()

#adds a new game to the scores table
def addGame(user, game, score):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO scores VALUES (?, ?, ?)"(user,game,score))
    db.commit()

#get the balance in a users account
def getBalance(user):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT balance FROM users WHERE username = ?",(user,))
    return c.fetchone
    db.commit()

#change the balance in a users account
def changeBalance(user,delta):
    db = get_db()
    c = db.cursor()
    c.execute("""UPDATE scores
                SET balance = ?
                WHERE username = ?""", (user, delta + getBalance(user)))    
    db.commit()
#Gets the num highest scores for a specific game 
def getHiScores(num, game):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT TOP ? FROM scores WHERE game = ? ORDER BY score DESC", (num, game))
    return c.fetchall
    db.commit()

#Gets the num highest scores for a specific game 
def getUserHiScores(num, game, user):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT TOP ? FROM scores WHERE game = ? AND user = ? ORDER BY score DESC", (num, game, user))
    return c.fetchall
    db.commit()    

# Gets the user's password (for verification purposes)
def getPass(user):
    db = get_db()
    c = db.cursor()
    c.execute(f"SELECT password FROM users WHERE username = ?", (user,))
    return c.fetchone()