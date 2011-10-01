#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime

import pymongo

import config

db = pymongo.Connection(config.SERVER, config.PORT)[config.DATABASE]
db.authenticate(config.USERNAME,config.PASSWORD)

collection = db.eff
collection.ensure_index('eff')
collection.ensure_index('count')
collection.ensure_index('date_modified')

class Eff(object):
    def __init__(self, eff):
        self._doc = collection.find_one({'eff': eff})
        if self._doc is None:
            self._doc = {'eff': eff, 'count': 0, 'date_created': datetime.now()}

    def __getattr__(self, name):
        return self._doc[name]

    def inc(self):
        self._doc['date_modified'] = datetime.now()
        self._doc['count'] += 1

    def save(self):
        self._doc['_id'] = collection.save(self._doc)


