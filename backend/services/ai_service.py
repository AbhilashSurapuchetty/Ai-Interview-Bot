import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_greeting(name: str) -> str:
    if not GEMINI_API_KEY:
        return f"Hi {name}! Welcome to your AI-powered interview. When you're ready, click Start Interview."

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro
        prompt = f"Write a professional, warm, and encouraging two line introduction for an interview candidate named {name}. Make it sound like a real person is speaking."

        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:
        print("AI service error:", e)

    # Fallback
    return f"Hi {name}! Welcome to your AI-powered interview. When you're ready, click Start Interview."
