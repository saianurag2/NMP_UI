from flask import Flask
from flask_session import Session
from blueprint.home.views import home
from blueprint.auth.views import auth
from blueprint.device.views import device

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(device)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

