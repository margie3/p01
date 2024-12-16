import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for
from db import makeDb, addUser, getPass, changeBalance
import key
import blackjack

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
        changeBalance(name, 10)
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
    if request.method == "GET":
        game_data = blackjack.setup()
        return render_template('blackjack.html', 
                               user_score=game_data["user_score"],
                               dealer_score=game_data["dealer_score"],
                               user_images=game_data["user_images"],
                               dealer_images=game_data["dealer_images"])

    # If POST request (hit or stay)
    action = request.form.get("action")  # 'hit' or 'stay'
    if action == "hit":
        game_data = blackjack.hit()
        return jsonify({"user_score": game_data["user_score"], "user_image": game_data["user_image"]})

    elif action == "stay":
        game_data = blackjack.stay()
        return jsonify({"game_over": game_data["game_over"], 
                        "win": game_data["win"], 
                        "user_score": game_data["user_score"], 
                        "dealer_score": game_data["dealer_score"]})

    return render_template('blackjack.html')

if __name__ == "__main__":
    app.debug = True
    app.run()  # Ensure the app runs when this script is executed
