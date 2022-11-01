import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import os

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")
cur_user=[]
IMG_FOLDER = os.path.join('static', 'images')

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/student_register", methods=("GET", "POST"))
def student_register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        college_reg_no = request.form["college_reg_no"]
        password = request.form["password"]
        email=request.form["email"]
        db = get_db()
        error = None

        if not college_reg_no:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not email:
            error = "email is required."
        print("before if")
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (college_reg_no, password,email) VALUES (?, ?,?)",
                    (college_reg_no, generate_password_hash(password),email),
                )
                db.commit()
                
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {college_reg_no} or {email} is already registered."
            else:
                # Success, go to the login page.
                print("before login")
                return redirect(url_for("auth.student_login"))

        flash(error)

    return render_template("auth/register.html")

@bp.route("/faculty_register", methods=("GET", "POST"))
def faculty_register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        college_reg_no = request.form["college_reg_no"]
        password = request.form["password"]
        email=request.form["email"]
        db = get_db()
        error = None

        if not college_reg_no:
            error = "Reg No is required."
        elif not password:
            error = "Password is required."
        elif not email:
            error = "email is required."
        print("before if")
        if error is None:
            try:
                db.execute(
                    "INSERT INTO faculty (college_reg_no, password,email) VALUES (?, ?,?)",
                    (college_reg_no, generate_password_hash(password),email),
                )
                db.commit()
                
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"faculty {college_reg_no} or {email} is already registered."
            else:
                # Success, go to the login page.
                print("before login")
                return redirect(url_for("auth.faculty_login"))

        flash(error)

    return render_template("auth/registerf.html")

@bp.route("/faculty_login", methods=("GET", "POST"))
def faculty_login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        college_reg_no = request.form["college_reg_no"]
        password = request.form["password"]
        db = get_db()
        print("sadas")
        error = None
        user = db.execute(
            "SELECT * FROM faculty WHERE college_reg_no = ?", (college_reg_no,)
        ).fetchone()
        cur_user=[user]
        if user is None:
            error = "Incorrect college_reg_no."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            print("usesss",g.user)
            return redirect(url_for("blog.faculty_welcome"))

        flash(error)

    return render_template("auth/loginf.html")



@bp.route("/student_login", methods=("GET", "POST"))
def student_login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        college_reg_no = request.form["college_reg_no"]
        password = request.form["password"]
        db = get_db()
        print("sadas")
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE college_reg_no = ?", (college_reg_no,)
        ).fetchone()
        cur_user=[user]
        if user is None:
            error = "Incorrect college_reg_no."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("blog.welcome"))

        flash(error)

    return render_template("auth/index.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    cur_user=[]
    return redirect(url_for("index"))
