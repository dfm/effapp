#!/usr/bin/env python
# encoding: utf-8

import config
import pymongo

class Database(object):
  def __init__(self):
    self.db = pymongo.Connection(config.SERVER, config.PORT)[config.DATABASE]
    self.db.authenticate(config.USERNAME,config.PASSWORD)
    self.collection = self.db.eff
    self.collection.ensure_index('eff')
    self.collection.ensure_index('count')
    self.collection.ensure_index('date_modified')
    self._cache = {}

  def save(self, item):
    return self.collection.save(item)

  def __getitem__(self, item):
    result = self.collection.find_one({'eff': item})
    if result is None:
      raise KeyError
    return result

  def cache_list_request(field):
    def wrap(func):
      def cache(self, limit=10, *args, **kwargs):
        try:
          if self._cache[field]["limit"] <= limit:
            return self._cache[field]["data"][:limit]
        except KeyError:
          self._cache[field] = {"limit":0, "data":None}
        finally:
          self._cache[field]["limit"] = limit
          self._cache[field]["data"]  = func(self, limit, *args, **kwargs)
          return self._cache[field]["data"]
      return cache
    return wrap

  @cache_list_request("popular")
  def get_popular(self, limit=10):
    return self.collection.find(fields={'eff': 1, 'count': 1}) \
                          .sort([('count', pymongo.DESCENDING),('eff', pymongo.ASCENDING)]) \
                          .limit(limit)

  @cache_list_request("recent")
  def get_recent(self, limit=10):
    return self.collection.find(fields={'eff': 1, 'date_modified': 1}) \
                          .sort([('date_modified', pymongo.DESCENDING),('eff', pymongo.ASCENDING)]) \
                          .limit(limit)

if __name__ == "__main__":
  d = Database()
  from time import time
  
  start = time()
  popular = d.get_popular(10)
  print "Getting populars with DB call took %f s"%(time()-start)
  start = time()
  popular = d.get_popular(10)
  print "Getting populars with cache took %f s"%(time()-start)
  start = time()
  popular = d.get_popular(2)
  print "Getting populars with cache took %f s"%(time()-start)

  print "Popular:", [x["eff"] for x in d.get_popular(2)]
  print "Recent: ", [x["eff"] for x in d.get_recent(10)]
