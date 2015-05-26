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
#app.config.from_object('config.DevelopmentConfig')
if not os.environ.get('APP_SETTINGS'):
  os.environ['APP_SETTINGS'] = 'config.DevelopmentConfig'
app.config.from_object(os.environ.get('APP_SETTINGS'))
db = SQLAlchemy(app)

from models import *


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
  try:
    # Get log in info from jquery
    user_string = str(request.form.get('username_input'))
    user = User(user_string,user_string+'@fakeemail.com')
    db.session.add(user)
    db.session.commit()
    session['user'] = user_string
    # Set random avatar if none was given
    avatar = get_random_avatar()
    session['user_avatar'] = avatar
    return redirect("/passwordgame", code=302)
  except Exception as login_error:
    print login_error
    return redirect('/error', code=302)

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

@app.route('/error')
def error():
  return """
      <p>Error has occured</p>
      <p><a href="/passwordgame">Return to Home</a></p>
      """

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0',port=80)




