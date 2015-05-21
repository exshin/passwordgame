#!/usr/bin/python27
# -*- coding: utf-8 -*-

from psycopg2 import connect
from db.queries import *
from utils.util import utf_fix
from configs.config import connStr


def connect_db(connection='s4_production'):
  # connect to database
  try:
    conn = connect(connStr[connection])
    dbCursor = conn.cursor()
  except Exception as error:
    print error
    dbCursor = None
    conn = None
  return conn, dbCursor


def get_profile_list():
  # get profile list to serve up
  try:
    conn, dbCursor = connect_db('connect_db')
    dbCursor.execute(sql_get_served_candidates)
    served_list = dbCursor.fetchall()
    ss = transform_list(served_list)

    conn, dbCursor = connect_db()
    dbCursor.execute(dbCursor.mogrify(sql_profiles, [tuple(ss)]))
    results = dbCursor.fetchall()
    results = list(results)
    conn.close()
    for n in range(0, len(results)):
      results[n] = list(results[n])
      results[n][1] = utf_fix(results[n][1])
      results[n][2] = utf_fix(results[n][2])
  except Exception as error:
    print error, ':: Get Results Unsuccessful'
    results = []
  return results


def insert_served_candidates(person_id, user):
  # insert served candidates
  conn, dbCursor = connect_db('connect_db')
  if user:
    user_email = user + '@rivierapartners.com'
  else:
    user_email = None
  try:
    dbCursor.execute(sql_insert_served_candidates, [person_id, user_email, person_id])
    conn.commit()
    conn.close()
  except Exception as error:
    print error, ':: at inserting served candidates'
    conn.rollback()


def get_viewed_candidates(user):
  # get all viewed candidates by user and timeframe
  conn, dbCursor = connect_db('connect_db')
  if user:
    user_email = user + '@rivierapartners.com'
  else:
    user_email = None
  try:
    dbCursor.execute(sql_get_viewed_candidates, [user_email])
    results = dbCursor.fetchall()
    wk = []
    counts =[]
    if results:
      for row in results:
        wk.append(str(row[0]))
        counts.append(int(row[1]))
    conn.close()
    print wk
    print counts
    return wk,counts
  except Exception as error:
    print error, ':: at getting viewed candidates'
    conn.rollback()
    return [],[]


def transform_list(served_list):
  # change form of served list from [(1,), (2,), (3,)] to (1,2,3)
  result = []
  for row in served_list:
    result.append(row[0])
  return result
