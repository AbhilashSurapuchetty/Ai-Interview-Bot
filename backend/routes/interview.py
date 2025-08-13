'''from flask import Blueprint, render_template, request, session, redirect, url_for, flash , jsonify
import google.generativeai as genai
import os
from uuid import uuid4
import json 
from datetime import datetime 

interview_bp = Blueprint("interview", __name__)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

@interview_bp.route("/interview", methods=["GET", "POST"])
def interview():
    if "user" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    name = session["user"]["name"]

    if request.method == "POST":
        role = request.form.get("role")
        description = request.form.get("description")
        difficulty = request.form.get("difficulty")
        num_questions = request.form.get("num_questions")

        if not role or not description or not difficulty or not num_questions:
            flash("Please fill in all fields", "danger")
            return redirect(url_for("interview.interview"))

        # Build the prompt
        prompt = f"""
You are an expert interviewer.
The candidate's name is {name}.
Generate exactly {num_questions} professional interview questions for the job role "{role}".
Job Description: {description}
Difficulty Level: {difficulty}

Your output must have:
1. A single intro line: "Here goes your questions, {name}, asked with {difficulty} difficulty for the {role} role ({num_questions} questions)."
2. Then a section title: "Interview Questions:"
3. Then list each question in numbered format:
1. <Question 1>
2. <Question 2>
...
{num_questions}. <Question {num_questions}>

Do not include anything else.
"""

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            lines = [line.strip() for line in response.text.strip().split("\n") if line.strip()]

            intro = lines[0] if lines else ""
            # Remove intro and "Interview Questions:" line
            questions = [
                q for q in lines[1:] if not q.lower().startswith("interview questions")
            ]

            return render_template(
                "interview.html",
                name=name,
                role=role,
                difficulty=difficulty,
                num_questions=num_questions,
                intro=intro,
                questions=questions,
                done=True
            )
        except Exception as e:
            flash(f"AI service error: {e}", "danger")
            return redirect(url_for("interview.interview"))

    return render_template("interview.html", name=name, done=False)'''
    
    
    # backend/routes/interview.py
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
import google.generativeai as genai
from uuid import uuid4
import json
import os
from datetime import datetime

interview_bp = Blueprint("interview", __name__)

# ---------- Paths ----------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
UPLOAD_DIR = os.path.join(BASE_DIR, "frontend", "static", "uploads")
DATA_DIR = os.path.join(BASE_DIR, "backend", "data", "interviews")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# ---------- Gemini ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def _state_path(interview_id: str) -> str:
    return os.path.join(DATA_DIR, f"{interview_id}.json")

def _load_state(interview_id: str) -> dict:
    with open(_state_path(interview_id), "r", encoding="utf-8") as f:
        return json.load(f)

def _save_state(interview_id: str, state: dict) -> None:
    with open(_state_path(interview_id), "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

@interview_bp.route("/interview", methods=["GET", "POST"])
def interview():
    if "user" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    name = session["user"]["name"]

    if request.method == "POST":
        role = request.form.get("role")
        description = request.form.get("description")
        difficulty = request.form.get("difficulty")
        num_questions = request.form.get("num_questions")

        if not role or not description or not difficulty or not num_questions:
            flash("Please fill in all fields", "danger")
            return redirect(url_for("interview.interview"))

        # ---- Build the prompt for questions ----
        prompt = f"""
You are an expert interviewer.
The candidate's name is {name}.
Generate exactly {num_questions} professional interview questions for the job role "{role}".
Job Description: {description}
Difficulty Level: {difficulty}

Your output must have:
1. A single intro line: "Here goes your questions, {name}, asked with {difficulty} difficulty for the {role} role ({num_questions} questions)."
2. Then a section title: "Interview Questions:"
3. Then list each question in numbered format:
1. <Question 1>
2. <Question 2>
...
{num_questions}. <Question {num_questions}>

Do not include anything else.
"""

        try:
            if not GEMINI_API_KEY:
                # Fallback mock questions
                lines = [
                    f"Here goes your questions, {name}, asked with {difficulty} difficulty for the {role} role ({num_questions} questions).",
                    "Interview Questions:"
                ] + [f"{i+1}. Sample {role} question #{i+1}" for i in range(int(num_questions))]
            else:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                lines = [line.strip() for line in response.text.strip().split("\n") if line.strip()]

            intro = lines[0] if lines else ""
            questions = [q for q in lines[1:] if not q.lower().startswith("interview questions")]

            # ---- Persist an interview state on disk ----
            interview_id = uuid4().hex
            state = {
                "id": interview_id,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "candidate": name,
                "role": role,
                "difficulty": difficulty,
                "num_questions": int(num_questions),
                "intro": intro,
                "questions": questions,
                "answers": []  # each: {index, question, transcript, video_url}
            }
            _save_state(interview_id, state)

            # session pointer only (tiny)
            session["interview_id"] = interview_id

            return render_template(
                "interview.html",
                name=name,
                interview_id=interview_id,
                role=role,
                difficulty=difficulty,
                num_questions=int(num_questions),
                intro=intro,
                questions=questions,
                done=True
            )
        except Exception as e:
            flash(f"AI service error: {e}", "danger")
            return redirect(url_for("interview.interview"))

    # GET -> show setup form
    return render_template("interview.html", name=name, done=False)

@interview_bp.route("/interview/save_answer", methods=["POST"])
def save_answer():
    if "user" not in session:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    interview_id = request.form.get("interview_id")
    q_index = int(request.form.get("q_index", -1))
    question = request.form.get("question", "")
    transcript = request.form.get("transcript", "").strip()
    file = request.files.get("video")

    if not interview_id or q_index < 0 or not question or not file:
        return jsonify({"ok": False, "error": "Missing fields"}), 400

    # Save video
    filename = f"{uuid4().hex}.webm"
    save_path = os.path.join(UPLOAD_DIR, filename)
    file.save(save_path)

    video_url = url_for("static", filename=f"uploads/{filename}", _external=False)

    # Update state on disk
    state = _load_state(interview_id)
    # ensure one record per index
    existing = [a for a in state["answers"] if int(a["index"]) == q_index]
    if existing:
        existing[0]["question"] = question
        existing[0]["transcript"] = transcript
        existing[0]["video_url"] = video_url
    else:
        state["answers"].append({
            "index": q_index,
            "question": question,
            "transcript": transcript,
            "video_url": video_url
        })
    _save_state(interview_id, state)

    return jsonify({"ok": True, "video_url": video_url, "saved_count": len(state["answers"])})

@interview_bp.route("/interview/report", methods=["GET"])
def interview_report():
    if "user" not in session:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))

    interview_id = session.get("interview_id")
    if not interview_id:
        flash("No interview in progress.", "warning")
        return redirect(url_for("interview.interview"))

    state = _load_state(interview_id)
    name = state["candidate"]
    role = state["role"]
    difficulty = state["difficulty"]
    answers = sorted(state["answers"], key=lambda a: int(a["index"]))

    # Build evaluation prompt
    qa_list = [{"index": a["index"], "question": a["question"], "answer": a.get("transcript", "")} for a in answers]

    eval_prompt = f"""
You are an interview evaluator. Rate the candidate's answers concisely.

Candidate: {name}
Role: {role}
Difficulty: {difficulty}

Here are the questions and the candidate's transcripts as JSON:
{json.dumps(qa_list, ensure_ascii=False, indent=2)}

Return STRICT JSON with this exact structure (no extra text):
{{
  "overall_summary": "<2-4 sentence overview>",
  "overall_rating": <float 0-5>,
  "skills": [
    {{"name": "Communication", "rating": <0-5>, "note": "<one sentence>"}},
    {{"name": "Problem Solving", "rating": <0-5>, "note": "<one sentence>"}}
  ],
  "per_question": [
    {{
      "index": <int>,
      "rating": <0-5>,
      "strengths": "<one sentence>",
      "improvements": "<one sentence>"
    }}
  ]
}}
"""

    evaluation = None
    raw_text = None
    try:
        if GEMINI_API_KEY:
            model = genai.GenerativeModel("gemini-1.5-flash")
            resp = model.generate_content(eval_prompt)
            raw_text = (resp.text or "").strip()
        else:
            # Fallback mock
            raw_text = json.dumps({
                "overall_summary": "Solid communication with room for deeper specifics.",
                "overall_rating": 3.8,
                "skills": [
                    {"name": "Communication", "rating": 4.0, "note": "Clear and structured."},
                    {"name": "Problem Solving", "rating": 3.5, "note": "Reasonable approach, could justify trade-offs more."}
                ],
                "per_question": [
                    {"index": a["index"], "rating": 3.5, "strengths": "Answered confidently.", "improvements": "Add concrete examples."}
                    for a in answers
                ]
            }, indent=2)

        # Try parsing JSON (robust)
        try:
            evaluation = json.loads(raw_text)
        except Exception:
            # Try to extract the first {...} block
            start = raw_text.find("{")
            end = raw_text.rfind("}")
            if start != -1 and end != -1:
                evaluation = json.loads(raw_text[start:end+1])
            else:
                evaluation = None
    except Exception as e:
        flash(f"AI evaluation error: {e}", "danger")

    return render_template(
        "report.html",
        name=name,
        role=role,
        difficulty=difficulty,
        answers=answers,
        evaluation=evaluation,
        raw_text=raw_text
    )

