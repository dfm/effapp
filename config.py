#!/usr/bin/env python
# encoding: utf-8

import os

e = os.environ

DEBUG      = False
SECRET_KEY = e['SECRET_KEY']
USERNAME   = e['MONGO_USER']
PASSWORD   = e['MONGO_PASS']
DATABASE   = e['MONGO_DB']
SERVER     = e['MONGO_SERVER']
PORT       = int(e['MONGO_PORT'])
GAPIKEY    = e['GAPIKEY']
BASEURL    = e['BASEURL']
GANALYTICS = e['GANALYTICS']

