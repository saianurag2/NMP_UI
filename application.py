import requests
import json
from hashlib import sha256
from flask import Flask, request
from markupsafe import escape
from flask import render_template, redirect, url_for, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine("sqlite:///user_details.db")
BASE_URL = 'http://localhost:9001/device/'
INTERFACE_URL = 'http://localhost:9001/device/interface/'
VLAN_URL = 'http://localhost:9001/device/vlan/'
headers = {'content-type': 'application/json'}
# TODO use base url to get buildings list
BUILDINGS = ['LHTC', 'CC', 'Hall']


@app.route('/')
def index():
    """
    List of Buildings
    """
    if session.get("username"):
        bldgs = list()
        try:
            response = requests.get(BASE_URL, headers=headers)
            if response.status_code == requests.codes.ok:
                obj = json.loads(response.text)
                for bldg in obj:
                    bldgs.append(bldg["building"])
        except Exception:
            print(response.text)
        finally:
            return render_template("index.html", buildings=bldgs)
    else:
        return redirect(url_for("login"))


# User Authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        h = sha256()
        h.update(password.encode('utf-8'))
        crypt_pswd = h.hexdigest()
        db = scoped_session(sessionmaker(bind=engine))
        user = db.execute(
            "SELECT * FROM users WHERE (username = '" + username + "') AND (password = '" + crypt_pswd + "')").first()
        db.close()
        if user:
            session["username"] = user.username
            return redirect(url_for("index"))
        error = 'Invalid Credentials. Please try again'
        return render_template('user_login.html', error=error)
    else:
        return render_template('user_login.html', error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        pswd = request.form['password']
        confirm_pswd = request.form['password']
        email_id = request.form['email']
        if pswd == confirm_pswd:
            db = scoped_session(sessionmaker(bind=engine))
            user = db.execute("SELECT * FROM users WHERE (username = '" + username + "')").first()
            if user:
                error = "Username already exists"
                db.close()
            else:
                h = sha256()
                h.update(pswd.encode('utf-8'))
                crypt_pswd = h.hexdigest()
                db.execute("INSERT into users (username,email,password) values (:username,:email,:password)",
                           {"username": username, "email": email_id, "password": crypt_pswd})
                new_row = db.execute("SELECT * FROM users WHERE (username = '" + username + "')").first()
                print(f"Created new user :{new_row}")
                db.commit()
                db.close()
                return redirect(url_for('index'))
        else:
            error = "Passwords don't match. Try Again!"
    return render_template('user_signup.html', error=error)


# View Device Logic


@app.route('/devices')
def index_view():
    """
    Web page listing devices in a building
    """
    building = escape(request.args.get('building'))
    fetch_query = dict()
    if not building == "":
        fetch_query.update({"building": building})
    response = requests.get(BASE_URL, params=fetch_query, headers=headers)
    if response.status_code == requests.codes.ok:
        print("Index View Request : Success")
    else:
        print("Index View Request: Fail")
        response.raise_for_status()
        return redirect(url_for("index"))
    obj = json.loads(response.text)
    print(f"view {obj}")
    return render_template('displaydevices.html', devices=obj)


@app.route('/view')
def view_devices():
    """
    Takes :param building and :param ip from user
    :return: Building level view or device level based on user input
    """
    if session.get("username"):
        return render_template('viewdevices.html')
    else:
        return redirect(url_for("index"))


@app.route('/display', methods=['POST'])
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
    response = requests.get(BASE_URL, params=fetch_query, headers=headers)
    if response.status_code == requests.codes.ok:
        print("View Request : Success")
    else:
        print("View Request: Fail")
        response.raise_for_status()
    obj = json.loads(response.text)
    return render_template('displaydevices.html', devices=obj)


# Add Device Logic


@app.route('/creating', methods=['POST'])
def create_device():
    """
    Makes a POST request for adding device
    """
    bldg = request.form.get("building")
    ip = request.form.get("ipaddress")
    snmp_str = request.form.get("snmpstr")
    description = request.form.get("descr")
    device_obj = {"building": bldg, "ip": ip, "community_string": snmp_str, "description": description}
    response = requests.post(BASE_URL, data=json.dumps(device_obj), headers=headers)
    if response.status_code == requests.codes.ok:
        print("Add Request : Success")
    else:
        print("Add Request: Fail")
        response.raise_for_status()
    print(device_obj)
    print(f"Add device {response.text}")
    return redirect(url_for('index_view', building=bldg))


@app.route('/add', methods=['GET'])
def add_devices():
    """
    Renders a form to add new device details
    """
    if session.get("username"):
        return render_template('adddevices.html')
    else:
        return redirect(url_for("login"))


@app.route('/update', methods=["GET", "POST"])
def update_devices():
    """
     Renders a form to update existing devices
    """
    if session.get("username"):
        print("Update Request")
        return render_template('updatedevices.html')
    else:
        return redirect(url_for("login"))


@app.route('/updating', methods=['POST'])
def process_update():
    """
    Makes a PUT request to update existing device
    """
    data = request.form.to_dict()
    print(f"Initial form data: {data}")
    for key in [key for key in data if data[key] == ""]:
        del data[key]
    print(f"After removing empty fields: {data}")
    response = requests.put(BASE_URL, data=json.dumps(data), headers=headers)
    if response.status_code == requests.codes.ok:
        print("Update Request : Success")
    else:
        print("Update Request: Fail")
        response.raise_for_status()
    print(f"Up device {response.text}")
    return redirect(url_for("index"))


@app.route('/delete', methods=["GET", "POST"])
def delete_devices():
    """
    Makes a DELETE request
    """
    if session.get("username"):
        if request.method == "POST":
            ip = request.form.get("ipaddress")
            obj = {"ip": ip}
            response = requests.delete(BASE_URL, data=json.dumps(obj), headers=headers)
            if response.status_code == requests.codes.ok:
                print("Delete Request : Success")
                return redirect(url_for("index"))
            else:
                print("Delete Request: Fail")
                response.raise_for_status()
            print(f"Delete device {response.text}")
        return render_template('deletedevices.html')
    else:
        return redirect(url_for("login"))


@app.route('/interface')
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
    if response.status_code == requests.codes.ok:
        print("Interface View Request : Success")
    else:
        print("Interface View Request: Fail")
        response.raise_for_status()
    obj = json.loads(response.text)
    return render_template('interface_view.html', device=fetch_query, interfaces=obj)
