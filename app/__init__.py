import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for
from db import makeDb, addUser, getPass, changeBalance
import key
import blackjack
#import dice
#import coin

makeDb()

app = Flask(__name__)  # Initialize the Flask app
app.secret_key = key.key()

key_flip = None
try:
    with open("keys/key_coinflip.txt", "r") as file:
        key_flip = file.read()
except:
    print('no coinflip key')

key_freesound = None
try:
    with open("keys/key_freesound.txt", "r") as file:
        key_freesound = file.read()
except:
    print('no freesound key')

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    if 'email' and 'password' in session:
        name = session['email']
        # Boost balance by a fixed amount (e.g., 10 currency units)
        #changeBalance(name, 10)
        return render_template('homepage.html', user=name)
    return render_template('login.html')  # renders login page

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    session.pop('password', None)
    return render_template('logout.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Verify credentials
        stored_password = getPass(username)
        if stored_password == password:
            session["username"] = username
            session["password"] = password
            changeBalance(username, 50)
            return redirect(url_for("homepage"))
        else:
            return "Invalid username or password"
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Check if the username already exists
        existing_user = getPass(username)
        if existing_user:
            return "Username already exists. Please choose another."
        else:
            # Register the new user
            addUser(username, password)
            print(addUser)
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    '''session['email'] = request.form['username']
    session['password'] = request.form['password']
    name = session['email']'''
    return render_template('homepage.html')#, user=name)

@app.route("/blackjack", methods=["GET", "POST"])
def blackjack_result():
    # If POST request (hit or stay)
    action = request.form.get("action")  # 'hit' or 'stay'
    if action == "hit":
        blackjack.hit()
        return render_template('blackjack.html', 
                               user = session["username"],
                               userscore = blackjack.user,
                               win = blackjack.win,
                               end = blackjack.end,
                               bust = blackjack.bust,
                               yourturn = blackjack.yourturn,
                               user_imgs = blackjack.user_imgs,
                               dealerimg = blackjack.dealerimg, 
                               dealer_imgs = blackjack.dealer_imgs)
    elif action == "stay":
        blackjack.stay()
        return render_template('blackjack.html', 
                               user = session["username"],
                               userscore = blackjack.user,
                               win = blackjack.win,
                               end = blackjack.end,
                               bust = blackjack.bust,
                               yourturn = blackjack.yourturn,
                               user_imgs = blackjack.user_imgs,
                               dealerimg = blackjack.dealerimg,
                               dealer_imgs = blackjack.dealer_imgs)
    elif action == "bot":
        blackjack.bot()
        return render_template('blackjack.html', 
                               user = session["username"],
                               userscore = blackjack.user,
                               win = blackjack.win,
                               end = blackjack.end,
                               bust = blackjack.bust,
                               yourturn = blackjack.yourturn,
                               user_imgs = blackjack.user_imgs,
                               dealerimg = blackjack.dealerimg,
                               dealer_imgs = blackjack.dealer_imgs)
    else:
        blackjack.setup()
    if blackjack.end:
            if blackjack.win:
                changeBalance(session["username"], 20)  # Award +20 for winning
            else:
                changeBalance(session["username"], -10)  # Deduct -10 for losing
    return render_template('blackjack.html', 
                               user = session["username"],
                               userscore= blackjack.user,
                               win = blackjack.win,
                               end = blackjack.end,
                               yourturn = blackjack.yourturn,
                               user_imgs = blackjack.user_imgs,
                               dealerimg = blackjack.dealerimg, 
                               dealer_imgs = blackjack.dealer_imgs)

@app.route("/dice", methods=['GET', 'POST'])
def dice_result():
    if dice.end:
        if dice.win:
            user = session["username"]
            changeBalance(user, 20)  # Award +20 for winning
        else:
            user = session["username"]
            changeBalance(user, -10)  # Deduct -10 for losing
    if request.method == "POST":
        guessnum = request.form.get("guessnum")
        dice.guess(guessnum)
        render_template("dice.html", end = dice.end, win = dice.win, total = dice.num)
    return render_template('dice.html')

@app.route("/coin", methods=['GET', 'POST'])
def coin_result():
    if coin.end:
        if coin.win:
            user = session["username"]
            changeBalance(user, 20)  # Award +20 for winning
        else:
            user = session["username"]
            changeBalance(user, -10)  # Deduct -10 for losing
    action = request.form.get("action")
    if action == "heads":
        coin.flip(heads)
        render_template("dice.html", end = dice.end, win = dice.win, total = dice.num)
    elif action == "tails":
        coin.flip(tails)
        render_template("dice.html", end = dice.end, win = dice.win, total = dice.num)
    return render_template('coin.html')


if __name__ == "__main__":
    app.debug = True
    app.run()  # Ensure the app runs when this script is executed
