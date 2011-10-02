#!/usr/bin/env python
# encoding: utf-8

import os

import flask
import pymongo
import inflect
inflecteng = inflect.engine()

from models import Eff

app = flask.Flask(__name__)
app.config.from_object(__name__)

from database import Database
db = Database()


@app.route("/")
def home(current=None):
    number = None
    if current is not None:
        number = inflecteng.number_to_words(inflecteng.ordinal(current.count))
    return flask.render_template("index.html",
                                 current = current,
                                 number  = number,
                                 popular = db.get_popular(10),
                                 recent  = db.get_recent(10))

@app.route("/<new_eff>/")
def do_eff(new_eff):
    if new_eff != None:
        eff = Eff(new_eff, db)
        eff.increment()
        eff.save()
        return home(current=eff)
    return home()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

