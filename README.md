# AI-Powered Video Interview Bot 🎥🤖

An AI-powered mock interview platform that generates role-specific questions, records responses, transcribes them, and provides AI-driven feedback.

## 🚀 Features
- Role-specific interview generation
- Video & audio recording
- Real-time speech-to-text transcription
- AI-powered interview report with feedback

## 🛠️ Tech Stack
- Frontend: HTML, CSS, JavaScript  
- Backend: Flask (Python)  
- AI/LLM: Google Gemini API (gemini-1.5-flash)  

## 📂 Project Structure
```
AI-INTERVIEW-BOT/
│── backend/
│   ├── routes/
│   ├── services/
│   ├── data/
│   ├── static/
│   ├── templates/
│   ├── .env
│   ├── app.py
│   └── users.json
│── frontend/
│── venv/
│── .gitignore
│── requirements.txt
│── README.md
```

## ⚙️ Setup
```bash
git clone https://github.com/your-username/AI-INTERVIEW-BOT.git
cd AI-INTERVIEW-BOT
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

## 🔑 Environment Variables
Create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

## ▶️ Run the App
```bash
cd backend
python app.py
```

App runs at: [http://127.0.0.1:5000](http://127.0.0.1:5000)
