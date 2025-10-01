import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_greeting(name: str, tone: str = "professional") -> str:
    """
    Generate a polished greeting for an interview candidate.
    
    Args:
        name (str): Candidate's name.
        tone (str): Desired tone, e.g., 'professional', 'friendly', 'formal'.
    
    Returns:
        str: A warm, two-line greeting.
    """
    fallback_greeting = f"Hi {name}! Welcome to your AI-powered interview. When you're ready, click Start Interview."

    if not GEMINI_API_KEY:
        return fallback_greeting

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""
        You are an AI interview assistant.
        Write exactly 2 short sentences as a warm, {tone} introduction for a candidate named {name}.
        - Keep it under 40 words total.
        - Make it sound like a human interviewer, encouraging and approachable.
        - Do not include bullet points or formatting, just plain text.
        """

        response = model.generate_content(prompt)

        # Handle empty/invalid responses
        if not response or not response.text:
            return fallback_greeting

        greeting = response.text.strip()
        # Ensure it ends with a period or exclamation mark
        if not greeting.endswith((".", "!", "?")):
            greeting += "."

        return greeting

    except Exception as e:
        print("AI service error:", e)
        return fallback_greeting
