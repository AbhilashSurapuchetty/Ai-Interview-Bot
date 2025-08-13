# backend/services/user_service.py
import os, json, re
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
USERS_FILE = os.path.join(BASE_DIR, "users.json")

def ensure_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)

def load_users():
    ensure_users_file()
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def is_valid_password(password):
    # at least 8 chars, upper, lower, digit, special
    if (len(password) < 8 or
        not re.search(r"[a-z]", password) or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[0-9]", password) or
        not re.search(r"[!@#$%^&*]", password)):
        return False
    return True

def add_user(name, email, password):
    users = load_users()
    if any(u["email"] == email for u in users):
        return False
    hashed = generate_password_hash(password)
    users.append({"name": name, "email": email, "password": hashed})
    save_users(users)
    return True

def find_user_by_email(email):
    users = load_users()
    return next((u for u in users if u["email"] == email), None)

def verify_user(email, password):
    user = find_user_by_email(email)
    if user and check_password_hash(user["password"], password):
        return user
    return None
