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
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, balance INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS scores (username TEXT, game TEXT, score INTEGER)")
    db.commit()

# Registers a user with a username and password
def addUser(u, p):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, 100)", (u,p))  # Add default balance of 100
    db.commit()

# Adds a new game score to the scores table
def addGame(user, game, score):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO scores VALUES (?, ?, ?)", (user, game, score))
    db.commit()

# Gets the balance in a user's account
def getBalance(user):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT balance FROM users WHERE username = ?", (user,))
    result = c.fetchone()
    return result[0] if result else 0
    db.commit()

# Changes the balance in a user's account
def changeBalance(user, delta):
    db = get_db()
    c = db.cursor()
    new_balance = delta + getBalance(user)
    c.execute("UPDATE users SET balance = ? WHERE username = ?", (new_balance, user))
    db.commit()

# Gets the top N highest scores for a specific game
def getHiScores(num, game):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM scores WHERE game = ? ORDER BY score DESC LIMIT ?", (game, num))
    return c.fetchall()
    db.commit()

# Gets the top N highest scores for a specific game for a specific user
def getUserHiScores(num, game, user):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM scores WHERE game = ? AND username = ? ORDER BY score DESC LIMIT ?", (game, user, num))
    return c.fetchall()
    db.commit()

# Gets the user's password (for verification purposes)
def getPass(user):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (user,))
    result = c.fetchone()
    return result[0] if result else None
