#!/usr/bin/python27
#-*- coding: utf-8 -*-

import os
import requests
from random import randint
from flask import Flask, make_response, render_template, request, jsonify
from flask import send_from_directory, session, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta
import json
from api.password_game import *
from config import *

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import User


@app.route('/')
def index():
  if not session.get('teams'):
    session['teams'] = {'a':[],'b':[]}
  return redirect("/passwordgame", code=302)

@app.route('/passwordgame', methods=['GET', 'POST'])
def game_start():
  user = session.get('user')
  if not session.get('teams'):
    session['teams'] = {'a':[],'b':[]}
  return render_template('password_game.html',
          user=user)

@app.route('/login/', methods=['POST'])
def login():
  # Get log in info from jquery
  user = str(request.form.get('username_input'))
  session['user'] = user
  # Set random avatar if none was given
  avatar = get_random_avatar()
  session['user_avatar'] = avatar
  # Add to the team with the fewest players
  if not session.get('teams'):
    session['teams'] = {'a':[],'b':[]}
  if len(session['teams'].get('a')) == len(session['teams'].get('b')):
    session['teams']['a'].append({'user':user,'avatar':avatar})
    session['user_team'] = 'a'
  elif len(session['teams'].get('a')) > len(session['teams'].get('b')):
    session['teams']['b'].append({'user':user,'avatar':avatar})
    session['user_team'] = 'b'
  else:
    session['teams']['a'].append({'user':user,'avatar':avatar})
    session['user_team'] = 'a'
  user = User('JohnDoe', 'john.doe@example.com')
  db.session.add(user)
  db.session.commit()
  return redirect("/passwordgame", code=302)

@app.route('/random_word/', methods=['POST','GET'])
def random_word():
  # Get a random word
  if session.get('used_words'):
    word = get_random_word(used_words=session['used_words'])
  else:
    session['used_words'] = []
    word = get_random_word()
  session['used_words'].append(word)
  return jsonify({'word': word})

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')

@app.route('/clear_sessions')
def clear_sessions():
  session.clear()
  return """
      <p>Session Cleared</p>
      <p><a href="/passwordgame">Return to Home</a></p>
      """

@app.route('/logout')
def logout():
  session.clear()
  return """
      <p>Logged out</p>
      <p><a href="/passwordgame">Return to Home</a></p>
      """

app.secret_key = 'p0^r80j/3yx r~XaH!jm[]]L^I/,?RT'

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0',port=80)
  print(os.environ['APP_SETTINGS'])



