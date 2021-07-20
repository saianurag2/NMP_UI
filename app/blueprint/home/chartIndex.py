import requests
import logging
import json
from flask import Blueprint, render_template, redirect, url_for, session

visual = Blueprint('visual', __name__,
                   template_folder='templates')
API_ROOT = 'http://localhost:9001/device/'
headers = {'content-type': 'application/json'}


@visual.route('/chart')
def chart_index():
    """
    Stacked bar chart of Buildings
    """
    if session.get("username"):
        bldgs = list()
        online_devices = list()
        offline_devices = list()
        try:
            response = requests.get(API_ROOT, headers=headers)
            if response.status_code == requests.codes.ok:
                obj = json.loads(response.text)
                resp_size = len(obj)
                if resp_size > 1:
                    for index in range(resp_size):
                        if index == resp_size - 1:
                            for bldg in bldgs:
                                online_devices.append(obj[index][bldg]['Number of Online devices'])
                                offline_devices.append(obj[index][bldg]['Total number of devices']
                                                       - obj[index][bldg]['Number of Online devices'])
                            break
                        bldgs.append(obj[index]['building'])
                    # print(offline_devices)
                    # print(online_devices)
                    # print(bldgs)
        except requests.exceptions.HTTPError:
            logging.error(response.status_code, response.reason)
        finally:
            return render_template("home/dispState.html", buildings=json.dumps(bldgs), online=json.dumps(online_devices)
                                   , offline=json.dumps(offline_devices))
    else:
        return redirect(url_for("auth.login"))
