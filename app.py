#!/usr/bin/env python
# encoding: utf-8

import os
import re
import json
import flask
import inflect
inflecteng = inflect.engine()
from models import Eff

import config
app = flask.Flask(__name__)
app.config.from_object(config)

from database import Database
db = Database()

check_mobile = re.compile(r"(iphone|ipod|blackberry|android|palm|windows\s+ce)", re.I)

def give_fuck(fuck):
    """
    Increment the eff count

    Parameters
    ----------
    fuck : str
        The name of the eff to increment

    Returns
    -------
    eff : Eff
        The incremented eff object

    """
    eff = Eff(fuck, db)
    eff.increment()
    return eff

@app.route("/geoip/")
def testgeoip():
    import GeoIP
    geo = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
    return flask.make_response("%s\n%s\n"%( geo.country_code_by_name("google.com"), geo.record_by_name("google.com"))

@app.route("/fuck/")
@app.route("/")
def root():
    return render_home()

@app.route("/fuck/<new_eff>")
@app.route("/fuck/<new_eff>/<gui>")
def do_eff_gui(new_eff, gui=None):
    if gui == 'text':
        return do_eff_text(new_eff)
    elif gui == 'data':
        return show_data(new_eff)
    if new_eff != None:
        eff = give_fuck(new_eff)
        return render_home(current=eff)
    return render_home()

def render_home(current=None):
    if check_mobile.search(flask.request.headers["user_agent"]) and not "force_desktop" in flask.session:
        #flask.session["force_desktop"] = True
        pass # is mobile
    else:
        pass # is not mobile
    ####
    number = None
    if current is not None:
        number = inflecteng.number_to_words(inflecteng.ordinal(current.count))
    return flask.render_template("index.html",
                                 current = current,
                                 number  = number,
                                 popular = db.get_popular(10),
                                 recent  = db.get_recent(10),
                                 google_analytics = config.GANALYTICS)

def do_eff_text(new_eff):
    if new_eff != None:
        eff = give_fuck(new_eff)
        return flask.make_response("Fucks given about %s: %s\n"%(new_eff, eff.count))
    return flask.make_response("You don't give a fuck about giving a fuck\n")

def show_data(eff_name):
    eff = Eff(eff_name, db)
    return flask.make_response(json.dumps(eff.day_access, default=str))

@app.route("/favicon.ico")
def favicon():
    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

