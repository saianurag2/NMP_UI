import json
import requests
import logging
from markupsafe import escape
from flask import Blueprint, url_for, render_template, redirect, session, request

API_ROOT = 'http://localhost:9001/device/'
INTERFACE_URL = 'http://localhost:9001/device/interface/'
VLAN_URL = 'http://localhost:9001/device/vlan/'
headers = {'content-type': 'application/json'}

device = Blueprint('device', __name__,
                   template_folder='templates')


# View Device Logic
@device.route('/devices')
def index_view():
    """
    Web page listing devices in a building
    """
    building = escape(request.args.get('building'))
    fetch_query = dict()
    if not building == "":
        fetch_query.update({"building": building})
    response = requests.get(API_ROOT, params=fetch_query, headers=headers)
    obj = {}
    if response.status_code == requests.codes.ok:
        print("Index View Request : Success")
        obj = json.loads(response.text)
    else:
        print("Index View Request: Fail")
        logging.error(response.status_code, response.reason)
        return redirect(url_for("home.index"))

    print(f"view {obj}")
    return render_template('device/displaydevices.html', devices=obj)


@device.route('/view')
def view_devices():
    """
    Takes :param building and :param ip from user
    :return: Building level view or device level based on user input
    """
    if session.get("username"):
        return render_template('device/viewdevices.html')
    else:
        return redirect(url_for("home.index"))


@device.route('/display', methods=['GET', 'POST'])
def display_devices():
    """
    Makes a GET request
    Displays results of view_devices() and index_view()
    """
    bldg = escape(request.form.get("building"))
    ip = escape(request.form.get("ipaddress"))
    fetch_query = dict()
    if not bldg == "":
        fetch_query.update({"building": bldg})
    if len(ip) > 0:
        fetch_query.update({"ip": ip})
    response = requests.get(API_ROOT, params=fetch_query, headers=headers)
    obj = {}
    if response.status_code == requests.codes.ok:
        print("View Request : Success")
        obj = json.loads(response.text)
    else:
        print("View Request: Fail")
        logging.error(response.status_code, response.reason)

    return render_template('device/displaydevices.html', devices=obj)


# Add Device Logic
@device.route('/creating', methods=['POST'])
def create_device():
    """
    Makes a POST request for adding device
    """
    bldg = request.form.get("building")
    ip = request.form.get("ipaddress")
    snmp_str = request.form.get("snmpstr")
    description = request.form.get("descr")
    device_obj = {"building": bldg, "ip": ip, "community_string": snmp_str, "description": description}
    response = requests.post(API_ROOT, data=json.dumps(device_obj), headers=headers)
    if response.status_code == requests.codes.ok:
        print("Add Request : Success")
    else:
        print("Add Request: Fail")
        logging.error(response.status_code, response.reason)
    print(device_obj)
    print(f"Add device {response.text}")
    return redirect(url_for('index_view', building=bldg))


@device.route('/add', methods=['GET'])
def add_devices():
    """
    Renders a form to add new device details
    """
    if session.get("username"):
        return render_template('device/adddevices.html')
    else:
        return redirect(url_for("auth.login"))


@device.route('/update', methods=["GET", "POST"])
def update_devices():
    """
     Renders a form to update existing devices
    """
    if session.get("username"):
        print("Update Request")
        return render_template('device/updatedevices.html')
    else:
        return redirect(url_for("auth.login"))


@device.route('/updating', methods=['POST'])
def process_update():
    """
    Makes a PUT request to update existing device
    """
    data = request.form.to_dict()
    print(f"Initial form data: {data}")
    for key in [key for key in data if data[key] == ""]:
        del data[key]
    print(f"After removing empty fields: {data}")
    response = requests.put(API_ROOT, data=json.dumps(data), headers=headers)
    if response.status_code == requests.codes.ok:
        print("Update Request : Success")
    else:
        print("Update Request: Fail")
        logging.error(response.status_code, response.reason)
    print(f"Up device {response.text}")
    return redirect(url_for("home.index"))


@device.route('/delete', methods=["GET", "POST"])
def delete_devices():
    """
    Makes a DELETE request
    """
    if session.get("username"):
        if request.method == "POST":
            ip = request.form.get("ipaddress")
            obj = {"ip": ip}
            response = requests.delete(API_ROOT, data=json.dumps(obj), headers=headers)
            if response.status_code == requests.codes.ok:
                print("Delete Request : Success")
                return redirect(url_for("home.index"))
            else:
                print("Delete Request: Fail")
                logging.error(response.status_code, response.reason)
            print(f"Delete device {response.text}")
        return render_template('device/deletedevices.html')
    else:
        return redirect(url_for("auth.login"))


@device.route('/interface')
def fetch_interface():
    """
    Displays interface details of a particular device
    """
    building = request.args.get('building')
    ip = request.args.get('ip')
    fetch_query = dict()
    if not building == "":
        fetch_query.update({"building": building})
    if len(ip) > 0:
        fetch_query.update({"ip": ip})
    response = requests.get(INTERFACE_URL, params=fetch_query, headers=headers)
    obj = {}
    if response.status_code == requests.codes.ok:
        print("Interface View Request : Success")
        obj = json.loads(response.text)
    else:
        print("Interface View Request: Fail")
        logging.error(response.status_code, response.reason)
    return render_template('interface_view.html', device=fetch_query, interfaces=obj)


@device.route('/vlan')
def fetch_vlan():
    """
    Displays VLAN details of a particular device
    """
    building = request.args.get('building')
    ip = request.args.get('ip')
    fetch_query = dict()
    if not building == "":
        fetch_query.update({"building": building})
    if len(ip) > 0:
        fetch_query.update({"ip": ip})
    response = requests.get(VLAN_URL, params=fetch_query, headers=headers)
    obj = {}
    if response.status_code == requests.codes.ok:
        print("VLAN View Request : Success")
        obj = json.loads(response.text)
    else:
        print("VLAN View Request: Fail")
        logging.error(response.status_code, response.reason)
    return render_template('vlan_view.html', device=fetch_query, vlan=obj)
