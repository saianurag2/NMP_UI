from flask import Flask
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_details.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        main()
        db.session.add(User(username="Flask", email="example@example.com", password='secret'))
        db.session.commit()

