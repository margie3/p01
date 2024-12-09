from flask import Flask, render_template, session, request, flash, redirect
import sqlite3
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


if __name__ == "__main__":
    app.debug = True
    app.run()

