# backend/routes/main.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from services.ai_service import generate_greeting

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def landing():
    return render_template("landing.html")

@main_bp.route("/main")
def dashboard():
    if "user" not in session:
        flash("Please login to access the dashboard", "danger")
        return redirect(url_for("auth.login"))
    
    name = session["user"]["name"]
    greeting = generate_greeting(name)
    
    return render_template("main.html", name=name, greeting=greeting)

