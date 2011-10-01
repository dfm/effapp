#!/usr/bin/env python
# encoding: utf-8

import os

from flask import Flask
import pymongo

from models import Eff, collection

app = Flask(__name__)

@app.route("/<new_eff>/")
def do_eff(new_eff):
    if new_eff != "favicon.ico":
        eff = Eff(new_eff)
        eff.inc()
        eff.save()
    return "<br>".join(["Fuck %s! (%d)"%(doc['eff'], doc['count'])
        for doc in collection.find(
            fields={'eff': 1, 'count': 1}).sort('count', pymongo.DESCENDING)])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

