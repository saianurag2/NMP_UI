from flask import Blueprint, request, render_template, redirect, url_for, session
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import sha256
from models import engine


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
        db = scoped_session(sessionmaker(bind=engine))
        user = db.execute(
            "SELECT * FROM users WHERE (username = '" + username + "') AND (password = '" + crypt_pswd + "')").first()
        db.close()
        if user:
            session["username"] = user.username
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
                return redirect(url_for('.login'))
        else:
            error = "Passwords don't match. Try Again!"
    return render_template('auth/user_signup.html', error=error)
