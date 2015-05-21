#!/usr/bin/python27
#-*- coding: utf-8 -*-

import os
import requests
from flask import Flask, make_response, render_template, request, jsonify
from flask import send_from_directory, session, url_for, redirect
from datetime import datetime
from datetime import timedelta
from profiles import *
import json

app = Flask(__name__)


@app.route('/')
def index():
  return redirect("/profiles", code=302)

@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
  user = session.get('user')
  return render_template('profiles.html',
          user=user)

@app.route('/login/', methods=['POST'])
def login():
  # get log in info from jquery
  user = str(request.form.get('email_input'))
  password = str(request.form.get('password_input'))
  print 'user: ',user,', password: ',password
  if password == 'riviera' and '@rivierapartners.com' in user:
    session['user'] = user.replace('@rivierapartners.com','').strip(' ')
    return redirect("/profiles", code=302)
  else:
    return redirect('/error', code=302)

@app.route('/error', methods=['GET','POST'])
def error_page():
  return render_template('error.html')

@app.route('/candidate_click/', methods=['GET'])
def candidate_click():
  # insert clicked candidate into DB
  user = session.get('user')
  person_id = int(str(request.args.get('person_id')))
  print user, person_id
  # insert into db
  insert_served_candidates(person_id,user)
  # query new my_votes
  return jsonify({'person_id': person_id})

@app.route('/stats',methods=['POST','GET'])
def stats():
  # get stats
  user = session.get('user')
  wk, counts = get_viewed_candidates(user)
  return render_template('stats.html',
          user=user, wk=wk, counts=counts)

@app.route('/list/', methods=['GET'])
def generate_list():
  profile_list = get_profile_list()
  if session.get('user'):
    return jsonify({'profiles':profile_list})
  else:
    return jsonify({'profiles':[]})

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')

@app.route('/clear_sessions')
def clear_sessions():
  session.clear()
  return """
      <p>Session Cleared</p>
      <p><a href="/profiles">Return to Home</a></p>
      """

@app.route('/logout')
def logout():
  session.clear()
  return """
      <p>Logged out</p>
      <p><a href="/profiles">Return to Home</a></p>
      """

@app.route('/shutdown', methods=['POST'])
def shutdown():
  shutdown_server()
  return 'Server shutting down...'

app.secret_key = 'p0^r80j/3yX r~XHH!jm[]]L^x/,?RT'

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0',port=80)