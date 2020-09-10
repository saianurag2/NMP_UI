from flask import Blueprint, request, render_template, redirect, url_for, session
from hashlib import sha256
from app.extensions import db
from app.models import User

auth = Blueprint('auth', __name__,
                 template_folder='templates')


# User Authentication
@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        h = sha256()
        h.update(password.encode('utf-8'))
        crypt_pswd = h.hexdigest()
        existing_user = User.query.filter_by(username=username, password=crypt_pswd).first()
        if existing_user:
            session["username"] = existing_user.username
            return redirect(url_for("home.index"))
        error = 'Invalid Credentials. Please try again'
        return render_template('auth/user_login.html', error=error)
    else:
        return render_template('auth/user_login.html', error=error)


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for(".login"))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        pswd = request.form['password']
        confirm_pswd = request.form['password']
        email_id = request.form['email']
        if pswd != confirm_pswd:
            error = "Passwords don't match. Try Again!"
        elif username and email_id:
            existing_user = User.query.filter(
                User.username == username or User.email == email_id
            ).first()
            if existing_user:
                error = "Username already exists"
            else:
                h = sha256()
                h.update(pswd.encode('utf-8'))
                crypt_pswd = h.hexdigest()
                new_user = User(username=username, password=crypt_pswd, email=email_id)
                db.session.add(new_user)
                db.session.commit()
                new_row = User.query.filter_by(username=username, password=crypt_pswd).first()
                print(f"Created new user :{new_row}")
                return redirect(url_for('.login'))
    return render_template('auth/user_signup.html', error=error)
