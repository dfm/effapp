#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import config


class Eff(object):
    def __init__(self, eff, db):
        self.db = db
        try:
            self._doc = db[eff]
        except KeyError:
            self._doc = {'eff': eff, 'count': 0, 'date_created': datetime.now()}
            self.db.save(self._doc)
        self.short_url = '/'.join([config.BASEURL, "fuck", eff])

    def __getattr__(self, name):
        return self._doc[name]

    def add_location(self, location):
        self.db.add_location(self._doc['eff'])

    def increment(self):
        self.db.increment(self._doc['eff'])
        self._doc['count'] += 1

