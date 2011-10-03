#!/usr/bin/env python
# encoding: utf-8

import os

import json
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

def give_fuck(fuck):
    eff = Eff(fuck, db)
    eff.increment()
    eff.save()
    return eff

@app.route("/fuck/<new_eff>/")
def do_eff_gui(new_eff):
    if new_eff != None:
        eff = give_fuck(new_eff)
        return home(current=eff)
    return home()

@app.route("/text/<new_eff>/")
def do_eff_text(new_eff):
    if new_eff != None:
        eff = give_fuck(new_eff)
        return flask.make_response("Fucks given about %s: %s"%(new_eff, eff.count))
    return flask.make_response("You don't give a fuck about giving a fuck")

@app.route("/data/<eff_name>/")
def show_data(eff_name):
  eff = Eff(eff_name, db)
  return flask.make_response(json.dumps(eff.date_access, default=str))

@app.route("/favicon.ico")
def favicon():
  pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

