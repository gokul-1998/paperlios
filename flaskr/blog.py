from locale import currency
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from .auth import cur_user
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    # """Show all the posts, most recent first."""
    # db = get_db()
    # posts = db.execute(
    #     "SELECT p.id, title, body, created, author_id, username"
    #     " FROM post p JOIN user u ON p.author_id = u.id"
    #     " ORDER BY created DESC"
    # ).fetchall()
    cur_user=[]
    print(cur_user)
    return render_template("auth/home.html")

@bp.route("/welcome")
def welcome():
    return render_template("auth/welcome.html")

@bp.route("/faculty_welcome")
def faculty_welcome():
    return render_template("auth/welcomef.html")

@bp.route("/student_proposals")
def new_proposals():
    proposal = (
        get_db()
        .execute(
            "SELECT event_description,status"
            " FROM proposal "
            " WHERE author_id = ?",
            ( g.user["id"],),
        )
        .fetchall())
    print(g.user['id'])
    return render_template("blog/yourproposal.html",proposal=proposal)


@bp.route("/add_new_proposal", methods=("GET", "POST"))
def add_new_proposal():
    """Create a new post for the current user."""
    if request.method == "POST":
        to_email = request.form["to_email"]
        event_description = request.form["event_description"]
        error = None

        if not event_description:
            error = "event_description is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO proposal (to_email, event_description, author_id) VALUES (?, ?, ?)",
                (to_email, event_description, g.user["id"]),
            )
            db.commit()
            print("before commit",g.user['id'])
            return redirect(url_for("blog.new_proposals"))
    faculty = (
        get_db()
        .execute(
            "SELECT email"
            " FROM faculty"
        )
        .fetchall()
    )
    return render_template("blog/newproposal.html",faculty=faculty)


@bp.route("/faculty_proposals", methods=("GET", "POST"))
@login_required
def add_faculty_proposal():
    """Create a new post for the current user."""
    if request.method == "POST":
        to_email = request.form["to_email"]
        event_description = request.form["event_description"]
        error = None

        if not event_description:
            error = "event_description is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO proposal (to_email, event_description, author_id) VALUES (?, ?, ?)",
                (to_email, event_description, g.user["id"]),
            )
            db.commit()
            print("before commit",g.user['id'])
            return redirect(url_for("blog.new_proposals"))
    proposal = (
        get_db()
        .execute(
            "SELECT event_description,status"
            " FROM proposal",
        )
        .fetchall())
    print("aaaa",g.user["email"])
    print("bbbb",cur_user)
    return render_template("blog/faculty_proposal.html",proposal=proposal)

@bp.route("/student_duty_leave")
def student_duty_leave():
    duty_leave=(
        get_db()
        .execute(
            "SELECT duty_leave_description,status"
            " FROM dutyleave "
           
        )
        .fetchall())
    return render_template("blog/dutyleave.html",duty_leave=duty_leave)

@bp.route("/add_student_duty_leave", methods=("GET", "POST"))
def add_student_duty_leave():
    """Create a new post for the current user."""
    if request.method == "POST":
        to_email = request.form["to_email"]
        duty_leave_description = request.form["duty_leave_description"]
        error = None

        if not duty_leave_description:
            error = "duty_leave_description is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO dutyleave (to_email, duty_leave_description, author_id) VALUES (?, ?, ?)",
                (to_email, duty_leave_description, g.user["id"]),
            )
            db.commit()
            print("before commit",g.user['id'])
            return redirect(url_for("blog.student_duty_leave"))
    faculty = (
        get_db()
        .execute(
            "SELECT email"
            " FROM faculty"
        )
        .fetchall()
    )
    return render_template("blog/newdutyleave.html",faculty=faculty)


@bp.route("/student_bus_pass")
def student_bus_pass():
    return render_template("blog/yourproposal.html")

@bp.route("/faculty_duty_leave")
def faculty_duty_leave():
    return render_template("blog/yourproposal.html")

@bp.route("/faculty_bus_pass")
def faculty_bus_pass():
    return render_template("blog/yourproposal.html")

def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            ( g.user["id"],),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
