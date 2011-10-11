#!/usr/bin/env python
# encoding: utf-8

import config
import pymongo
from time import time
from datetime import datetime

class Database(object):
  def __init__(self):
    self.db = pymongo.Connection(config.SERVER, config.PORT)[config.DATABASE]
    self.db.authenticate(config.USERNAME,config.PASSWORD)
    self.collection = self.db.eff
    self.collection.ensure_index('eff')
    self.collection.ensure_index('count')
    self.collection.ensure_index('date_modified')
    self._cache = {}

  def __del__(self):
    self.db.logout()

  def save(self, item):
    return self.collection.save(item)

  def increment(self, item):
    now = datetime.now()
    self.collection.update({'eff': item},
            {'$inc': {'count': 1, 'day_access.%s'%(now.date()): 1},
             '$push': {'date_access': now},
             '$set': {'date_modified': now}})

  def __getitem__(self, item):
    result = self.collection.find_one({'eff': item})
    if result is None:
      raise KeyError
    return result

  def get_access_times(self, item):
    return self.collection.find_one({"eff":item}, fields={'date_access' : 1 })

  def get_popular(self, limit=10):
    return self.collection.find(fields={'eff': 1, 'count': 1}) \
                          .sort([('count', pymongo.DESCENDING),('eff', pymongo.ASCENDING)]) \
                          .limit(limit)

  def get_recent(self, limit=10):
    return self.collection.find(fields={'eff': 1, 'date_modified': 1}) \
                          .sort([('date_modified', pymongo.DESCENDING)]) \
                          .limit(limit)



if __name__ == "__main__":
  from time import time
  d = Database()
  print "Popular:", [x["eff"] for x in d.get_popular(2)]
  print "Recent: ", [x["eff"] for x in d.get_recent(10)]
