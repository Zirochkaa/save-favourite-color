from flask import render_template, request, session, redirect, url_for
from app import app, sqlite_model


@app.route("/", methods=["GET", "POST"])
def home():
    if "username" in session:
        username = session["username"]
        color = sqlite_model.get_color_for_user(username=username)
        return render_template("homepage.html", username=username, color=color)

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # If user is already logged in - don't show login page to them.
    if "username" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # `username` or `password` can't be empty. Also, they can't consist only from whitespaces.
        if not username or not username.strip() or not password or not password.strip():
            return render_template("login.html", message=f"Username/password can't be empty")

        if sqlite_model.check_user_exists(username=username, password=password) is False:
            return render_template("login.html", message=f"User with such username/password doesn't exist")

        session["username"] = username
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # If user is already logged in - don't show signup page to them.
    if "username" in session:
        return redirect(url_for("home"))

    colors = sqlite_model.get_all_colors()
    if request.method == "GET":
        return render_template("signup.html", colors=colors)

    username = request.form.get("username")
    password = request.form.get("password")
    favourite_color = request.form.get("color")

    # `username` or `password` can't be empty. Also, they can't consist only from whitespaces.
    if not username or not username.strip() or not password or not password.strip():
        return render_template("signup.html", colors=colors, message=f"Username/password can't be empty")

    # Since we had limited amount of colors, we need to check that color we got in form is from that limited amount.
    if sqlite_model.check_color_exists(color=favourite_color) is False:
        return render_template("signup.html", colors=colors, message=f"We don't support '{favourite_color}' color yet")

    # Check that user with this username already exists.
    signed_up = sqlite_model.signup(username=username, password=password, favourite_color=favourite_color)
    if signed_up is False:
        return render_template("signup.html", colors=colors, message="User with such username already exist")

    return render_template("after_signup.html")


@app.errorhandler(404)
def invalid_route(e):
    username = session["username"] if "username" in session else None
    return render_template("404_page.html", username=username)
