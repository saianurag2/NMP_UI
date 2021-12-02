import requests
import logging
import json
from flask import Blueprint, render_template, redirect, url_for, session

home = Blueprint('home', __name__,
                 template_folder='templates')
API_ROOT = 'http://localhost:9001/device/'
headers = {'content-type': 'application/json'}


@home.route('/')
def index():
    """
    List of Schools
    """
    if session.get("username"):
        bldgs = list()
        try:
            response = requests.get(API_ROOT, headers=headers)
            if response.status_code == requests.codes.ok:
                obj = json.loads(response.text)
                for bldg in obj:
                    bldgs.append(bldg["building"])
        except requests.exceptions.HTTPError:
            logging.error(response.status_code, response.reason)
        finally:
            return render_template("home/index.html", buildings=bldgs)
    else:
        return redirect(url_for("auth.login"))
