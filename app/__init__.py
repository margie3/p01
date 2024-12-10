from flask import Flask, render_template, session, request, flash, redirect
import sqlite3
from db import changeBalance, addGame, getBalance
import key
import blackjack

app = Flask(__name__)
app.secret_key = key.key()

key_flip = None
try:
    with open("keys/key_coinflip.txt", "r") as file:
        key_merriam = file.read().strip()
except:
    print('no coinflip key')

key_freesound = None
try:
    with open("keys/key_freesound.txt", "r") as file:
        key_unsplash = file.read().strip()
except:
    print('no freesound key')

@app.route("/",  methods=['GET','POST'])
def disp_loginpage():
    if 'email' and 'password' in session:
        name = session['email']
        # Boost balance by a fixed amount (e.g., 10 currency units)
        changeBalance(username, 10)
        return render_template('homepage.html', user=name)
    blackjack.run()
    return render_template( 'login.html' ) #renders homepage


@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.pop('email', None)
    session.pop('password', None)
    return render_template('logout.html')


@app.route("/homepage", methods = ['GET', 'POST'])
def redirect():
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    name = session['email']
    return render_template('homepage.html', user=name)

app.route("/blackjack", methods=["POST"])
def blackjack_result():
    try:
        game_result = request.json  # e.g., {"username": "stuy_guy", "win": True, "score": 20}
        username = game_result["username"]
        win = game_result["win"]
        score = game_result["score"]

        # Update balance based on win/loss
        balance_change = score if win else -score
        changeBalance(username, balance_change)

        # Record the game result in the scores table
        addGame(username, "blackjack", score)

        return {"message": "Game result recorded!", "balance": getBalance(username)}
    except KeyError:
        return {"error": "Invalid game result format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.debug = True
    app.run()

