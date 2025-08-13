# backend/routes/ai.py
from flask import Blueprint, jsonify, session
from services.ai_service import generate_greeting

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/api/greeting")
def greeting():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    name = session["user"]["name"]
    text = generate_greeting(name)
    return jsonify({"greeting": text})
