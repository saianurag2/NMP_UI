# from flask_sqlalchemy import SQLAlchemy
from . import db
# db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    role = db.Column(db.String(30), nullable=False, default="Viewer")
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)


