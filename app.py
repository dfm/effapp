#!/usr/bin/env python
# encoding: utf-8

import os

import flask
import pymongo
import inflect
inflecteng = inflect.engine()

from models import Eff, collection

app = flask.Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def home(current=None):
    number = None
    if current is not None:
        number = inflecteng.number_to_words(inflecteng.ordinal(current.count))
    return flask.render_template("index.html",
            current=current,
            number=number,
            popular=collection.find(fields={'eff': 1, 'count': 1})\
                     .sort([('count', pymongo.DESCENDING),
                         ('eff', pymongo.ASCENDING)]).limit(10),
            recent=collection.find(fields={'eff': 1, 'date_modified': 1})\
                     .sort([('date_modified', pymongo.DESCENDING),
                         ('eff', pymongo.ASCENDING)]).limit(10))

@app.route("/<new_eff>/")
def do_eff(new_eff):
    if new_eff.lower() in ['dan', 'daniel', 'dan f-m', 'dfm']:
        return "You wish!"
    if new_eff != "favicon.ico":
        eff = Eff(new_eff)
        eff.inc()
        eff.save()
        return home(current=eff)
    return home()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

