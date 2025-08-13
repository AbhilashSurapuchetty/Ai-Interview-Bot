# backend/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.user_service import add_user, is_valid_password, verify_user, find_user_by_email

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for("auth.signup"))

        if not is_valid_password(password):
            flash("Password must be at least 8 characters, include upper/lowercase, a number and a special character.", "danger")
            return redirect(url_for("auth.signup"))

        if find_user_by_email(email):
            flash("Email already exists!", "danger")
            return redirect(url_for("auth.signup"))

        add_user(name, email, password)
        flash("Signup successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = verify_user(email, password)
        if user:
            session["user"] = {"name": user["name"], "email": user["email"]}
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("main.landing"))
