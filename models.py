#!/usr/bin/python27
#-*- coding: utf-8 -*-

from app import db
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    avatar = db.Column(db.String())
    created_at = db.Column(db.DateTime)
    current_score = db.Column(db.Integer)
    last_game = db.Column(db.Integer)

    def __init__(self, username, created_at, current_score, last_game):
        self.username = username
        self.created_at = created_at
        self.current_score = current_score
        self.last_game = last_game

    def __repr__(self):
        return '<Username %r>' % self.username

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    url = db.Column(db.String())
    players = db.Column(JSON)
    created_at = db.Column(db.DateTime)
    current_player = db.Column(db.Integer)

    def __init__(self, name, url, players, created_at, current_player):
        self.url = url
        self.name = name
        self.players = players
        self.created_at = created_at
        self.current_player = current_player

    def __repr__(self):
        return '<id {}>'.format(self.id)