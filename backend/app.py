# backend/app.py
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env (optional)

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

# load secret from env if available
app.secret_key = os.urandom(24)

# Register blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.ai import ai_bp
from routes.interview import interview_bp

app.register_blueprint(interview_bp)


app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(ai_bp)

if __name__ == "__main__":
    app.run(debug=True)


















'''from flask import Flask, render_template, request, redirect, url_for, session , flash
import json
import os
import re 

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.secret_key = "secret_key123"  # Needed for sessions

USERS_FILE = "users.json"

# Ensure JSON file exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

def is_valid_password(password) :
    # Check if password is at least 8 characters long, contains uppercase, lowercase, digit, and special character
    if len(password) < 8 or not re.search(r"[a-z]",password) or not re.search(r"[A-Z]",password) or not re.search(r"[0-9]",password) or not re.search(r"[!@#$%^&*]",password) :
        return False
    return True




def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        
        if not name or not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for("signup"))

        
        if not is_valid_password(password) :
            flash("Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character.", "error")
            return redirect(url_for("signup"))
        
        
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        
        
        
        if any(u["email"] == email for u in users):
            flash ("Email already exists!", "Danger")
            return redirect(url_for("signup"))
        

        users.append({"name": name, "email": email, "password": password})
        
        
        with open(USERS_FILE,"w") as f :
            json.dump(users,f)
        
        flash("Signup successful! You can now log in.", "success")
        
        
        
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])

def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        
        
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        
        if user :
            session["user"] = user 
            return redirect(url_for("main"))
        else :
            flash("Invalid email or password!", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/main")
def main():
    
    if "user" not in session:
        flash("You need to log in first!", "danger")
        return redirect(url_for("login"))
    
    
    return render_template("main.html", name=session["user"]["name"])


@app.route("/logout")

def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("landing"))


if __name__ == "__main__":
    app.run(debug=True)'''
