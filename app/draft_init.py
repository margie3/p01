import os
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import key


app = Flask(__name__)
app.secret_key = key.key()


def length(a):
    return 1 + len(a) - len(a.replace(" ", ""))

@app.route("/")
def home():
    return render_template("homePage.html", projectName = "CasinoSim", description = "Our website serves as a casino simulator! Users are able to gamble their currency away or win big through a multitude of games. Think you have the skills to win? The luck to? Come play! And if you've hit rock bottom, log in tomorrow for your daily paycheck!")

@app.route("/response" , methods=['POST'])
def register():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if(request.form.get('username') == None):
        if(request.form.get('usernameL') != ""):
            c.execute("SELECT * FROM users WHERE username="+"'"+request.form.get('usernameL')+"'"+";")
            user = c.fetchone()
            if(user != None and user[1] == request.form.get('passwordL')):
                session['username'] = user[0]
                return redirect(url_for("home"))
    if(request.form.get('usernameL') == None):
        if(request.form.get('username') != ""): #Only change username if it's not none
            c.execute("SELECT * FROM users WHERE username="+"'"+request.form.get('username')+"'"+";")
            user = c.fetchone()
            if(user == None):

                c.execute("INSERT INTO users(username,password) VALUES (?,?);", (request.form.get('username'),request.form.get('password')))

                db.commit()
                db.close()
    return render_template('login.html')

@app.route('/createStories', methods=['GET', 'POST'])
def create_story():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if(request.method == 'POST'):
        if(request.form.get('title') != "" and request.form.get('text') != "" and session.get('username') != None):
            c.execute("SELECT * FROM stories WHERE name = ?;",(request.form.get('title'),))
            story = c.fetchone()
            print(length(request.form.get('text')))
            if(story == None and length(request.form.get('text')) < wordCount):
                c.execute("INSERT INTO stories(name) VALUES (?);", (request.form.get('title'),))
                c.execute("INSERT INTO usertext(user, story, text) VALUES (?,?,?);", (session.get('username'), request.form.get('title'), request.form.get('text')))
                db.commit()
                db.close()
                return redirect(url_for("home"))
    return render_template('createStories.html')

@app.route("/login")
def login():
    if(session.get('username') != None):
        return redirect(url_for("home"))
    return render_template("login.html", projectName="CasinoSim!")

@app.route("/logout")
def logout():
    session.pop('username',None)
    return render_template("logout.html")


@app.route("/storyTemplate", methods=['GET','POST'])
def story_temp():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if(request.args.get('story') != None):
        c.execute("SELECT * FROM usertext WHERE story = ?;",(request.args.get('story'),))
        story_text = c.fetchall()
        if(session.get('username') != None):
            loggedin = True
        else:
            loggedin = False
        c.execute("SELECT * FROM usertext WHERE story = ? and user = ?;",(request.args.get('story'),session.get('username')))
        ifEdited = c.fetchone()
        if (ifEdited != None):
            perm = False
        else:
            perm = True
        return render_template("storyTemplate.html", storyText=story_text,isLoggedIn = loggedin,title=request.args.get('story'),new=perm)
    return render_template("newStories.html", allStories = story_names)

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

