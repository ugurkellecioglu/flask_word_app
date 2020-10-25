import os
from typing import List

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from random_words import RandomWords
# Configure application
from PyDictionary import PyDictionary
import random
# Configure application


app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///users.db")
app.config['SECRET_KEY'] = 'the random string'

def replace(s, position, character):
    return s[:position] + character + s[position+1:]
def random_word():
    rw = RandomWords()
    word = rw.random_word()
    return word

def definition(word):
    word = word
    dictionary=PyDictionary(word)
    definitions = dictionary.getMeanings()
    definitionx = definitions[word]['Noun']
    return definitionx
class Word:
    def __init__(self, word):
        self.word = word





@app.route("/")
def home():
    return redirect('/login')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        newpsd = generate_password_hash(password, "sha256")
        db.execute("INSERT INTO users(username, password) VALUES(?, ?)", username, newpsd)
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():


    if request.method == "POST":

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return "invalid username and/or password"

        session["user_id"] = rows[0]["id"]

        return redirect("/words")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return render_template("home.html")

@app.route("/messages")
def messages():

    return render_template("message.html")
def give_a_word():
    rw = RandomWords()
    word = rw.random_word()
    return word
def get_meaning(word):
    
    dictionary=PyDictionary(word)
    print(word)
    definitions = dictionary.getMeanings()
    return definitions[word]['Noun']

class list_word():
    def __init__(self, liste):
        self.liste = liste
class Word:
    def __init__(self, word):
        self.word = word
    def setWord(self,word):
        self.word = word

class Tries:
    def __init__(self,tries):
        self.tries = tries
    def settries(self,tries):
        self.tries =tries
 
class Score:
    def __init__(self,score):
        self.score = score
    def setscore(self,score):
        self.score =score

word = random_word()

liste = []

l1 = list_word(liste)
w1 = Word(word)
w2 = Word(len(w1.word)* "_")

point = len(w1.word)
length = len(w1.word)
t = Tries(0)

score = Score(0)
best_scorex = Score(0)
t.settries(len(w1.word))
@app.route("/words", methods=["GET", "POST"])
def words():
 
    
    
    rnd = random.randint(0,len(w1.word)-1)
    if request.method == "GET":
        
        return render_template("words.html", word = w1.word, definitions = definition(w1.word), word2 = w2.word, len = len(w1.word))
    else: 
        
        ans = request.form.get('word')
        if ans == w1.word:
           
            scRow = db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])
            for sc in scRow:
                score.setscore(sc['score'])
                best_scorex.setscore(sc["best_score"])
            print(best_scorex.score, score.score)
            score.setscore(score.score + t.tries)
            if score.score > best_scorex.score:
                best_scorex.setscore(score.score)
                print(best_scorex.score)
                db.execute("UPDATE users SET score = ? WHERE id = ?", score.score, session['user_id'])
                db.execute("UPDATE users SET best_score = ? WHERE id = ?", best_scorex.score, session['user_id'])
            else:
                db.execute("UPDATE users SET score = ? WHERE id = ?", score.score, session['user_id'])
            

            
            old_word  = w1.word     
            w1.setWord(random_word())
            w2.setWord(len(w1.word)* "_") 
            l1.liste = []
            t.tries = len(w1.word)
            success = "TRUE the words was " + str(old_word)
            return render_template("words.html", word = w1.word, definitions = definition(w1.word), success = success,word2 = w2.word, len = len(w1.word))
        else:
            
            success = "FALSE"
            t.settries(t.tries - 1)
            if len(w1.word) - t.tries == len(w1.word) - 3:
                success = "YOU LOST"
                db.execute("UPDATE users SET score = ?  WHERE id = ?", 0, session['user_id'])
               
                return render_template("words.html",  word = w1.word, definitions = definition(w1.word), success = success, word2 = w2.word, len = len(w1.word)) 
            if rnd not in l1.liste:
                w2.word = replace(w2.word,rnd, w1.word[rnd])
                l1.liste.append(rnd)
            else:
                while rnd in l1.liste:
                    rnd = random.randint(0,len(w1.word)-1)
                    w2.word = replace(w2.word,rnd , w1.word[rnd])
            l1.liste.append(rnd)
            return render_template("words.html",  word = w1.word, definitions = definition(w1.word), success = success, word2 = w2.word, len = len(w1.word))
    
    
@app.route('/scoreboard')
def scoreboard():
    rows = db.execute("SELECT * FROM users ORDER BY best_score")
   
    return render_template('scoreboard.html', rows = rows)