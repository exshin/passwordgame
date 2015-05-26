#!/usr/bin/python27
#-*- coding: utf-8 -*-

import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'p0^r80j/3yx r~XaH!jm[]]L^I/,?RT'
    if not os.environ.get('DATABASE_URL'):
      SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/passwordgame'
    else:
      SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/passwordgame'


class TestingConfig(Config):
    TESTING = True

