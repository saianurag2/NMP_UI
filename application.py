import requests, json
from hashlib import sha256
from flask import Flask, request
from flask import render_template, redirect, url_for, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine("sqlite:///user_details.db")
db = scoped_session(sessionmaker(bind=engine))

BASE_URL = 'https://localhost:9001/device/'


@app.route('/')
def index():
    if session.get("username"):
        return render_template("index.html")
    else:
        return redirect(url_for("login"))


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        h = sha256()
        h.update(password.encode('utf-8'))
        crypt_pswd = h.hexdigest()
        user = db.execute(
            "SELECT * FROM users WHERE (username = '" + username + "') AND (password = '" + crypt_pswd + "')").first()
        if user:
            session["username"] = user.username
            return redirect(url_for("index"))
        error = 'Invalid Credentials. Please try again.'
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
            user = db.execute("SELECT * FROM users WHERE (username = '" + username + "')").first()
            if user:
                error = "Username already exists"
            else:
                h = sha256()
                h.update(pswd.encode('utf-8'))
                crypt_pswd = h.hexdigest()
                db.execute("INSERT into users (username,email,password) values (:username,:email,:password)",
                           {"username": username, "email": email_id, "password": crypt_pswd})
                resp = db.execute("select * from users").fetchall()
                print(resp)
                db.commit()
                return redirect(url_for('index'))
        else:
            error = "Passwords don't match. Try Again!"
    return render_template('user_signup.html', error=error)


@app.route('/view')
def view_devices():
    if session.get("username"):
        return render_template('viewdevices.html')
    else:
        return redirect(url_for("index"))


@app.route('/display', methods=['POST'])
def display_devices():
    bldg = request.form.get("building")
    ip = request.form.get("ipaddress")
    fetch_query = {"building": bldg, "ip": ip}
    response = requests.get(BASE_URL, params=json.dumps(fetch_query))
    if response.status_code == requests.codes.ok:
        print("View Request : Success")
    else:
        print("View Request: Fail")
        response.raise_for_status()
    # obj = {"devices": [{"building": 'abc', "ip": '1.2.3.4', "community_string": "snap", "description": "gibber"},
    #                    {"building": "bla", "ip": '2.3.4.5', "community_string": "uber", "description": "parsel"}]}
    obj = json.loads(response.text)
    print(f"view {obj}")
    return render_template('displaydevices.html', devices=obj)


@app.route('/cd', methods=['POST'])
def create_device():
    bldg = request.form.get("building")
    ip = request.form.get("ipaddress")
    snmpstr = request.form.get("snmpstr")
    description = request.form.get("descr")
    device_obj = {"building": bldg, "ip": ip, "community_string": snmpstr, "description": description}
    response = requests.post(BASE_URL, data=device_obj)
    if response.status_code == requests.codes.ok:
        print("Add Request : Success")
    else:
        print("Add Request: Fail")
        response.raise_for_status()
    # TODO change it
    # response = requests.get(url="http://worldtimeapi.org/api/ip")
    print(device_obj)
    print(f"Add device \n {response.text}")
    return redirect(url_for("index"))


@app.route('/add', methods=['GET'])
def add_devices():
    if session.get("username"):
        return render_template('adddevices.html')
    else:
        return redirect(url_for("index"))


@app.route('/update', methods=["GET","POST"])
def update_devices():
    if session.get("username"):
        print("Update Request")
        return render_template('updatedevices.html')
    else:
        return redirect(url_for("index"))


@app.route('/delete', methods=["GET","POST"])
def delete_devices():
    if session.get("username"):
        if request.method == "POST":
            ip = request.form.get("ipaddress")
            obj = {"ip": ip}
            response = requests.delete(BASE_URL, data=json.dumps(obj) )
            if response.status_code == requests.codes.ok:
                print("Delete Request : Success")
            else:
                print("Delete Request: Fail")
                response.raise_for_status()
            print(f"Delete device \n{response.text}")
        return render_template('deletedevices.html')
    else:
        return redirect(url_for("index"))


