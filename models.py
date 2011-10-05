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
            self._doc = {'eff': eff, 'count': 0, 'date_created': datetime.now(), 'date_access': []}
        self.short_url = '/'.join([config.BASEURL, "fuck", eff])

    def __getattr__(self, name):
        return self._doc[name]

    def increment(self):
        self._doc['date_modified'] = datetime.now()
        self._doc['date_access'].append(datetime.now())
        self._doc['count'] += 1

    def save(self):
        self._doc['_id'] = self.db.save(self._doc)


