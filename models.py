#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import urllib2
import json
import config

google_url = "https://www.googleapis.com/urlshortener/v1/url?key=%s"%(config.GAPIKEY)

class Eff(object):
    def __init__(self, eff, db):
        self.db = db
        try:
            self._doc = db[eff]
        except KeyError:
            self._doc = {'eff': eff, 'count': 0, 'date_created': datetime.now()}
        if 'short_url' not in self._doc:
            data = {"longUrl": '/'.join([config.BASEURL, eff])}
            headers = {"Content-Type": "application/json"}
            req = urllib2.Request(google_url, json.dumps(data), headers)
            res = json.loads(urllib2.urlopen(req).read())
            self._doc['short_url'] = res['id']

    def __getattr__(self, name):
        return self._doc[name]

    def increment(self):
        self._doc['date_modified'] = datetime.now()
        self._doc['count'] += 1

    def save(self):
        self._doc['_id'] = self.db.save(self._doc)


