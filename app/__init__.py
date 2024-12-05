from flask import Flask, render_template, session, request, flash, redirect
import sqlite3
import key

app = Flask(__name__)
app.secret_key = key.key()

@app.route("/")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.debug = True
    app.run()

