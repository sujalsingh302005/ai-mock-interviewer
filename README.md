# 🎯 AI Mock Interviewer

Practice technical interviews with real-time AI feedback on your spoken answers.

## Features
- 🎙️ Speak your answer into the mic
- 📝 Whisper transcribes your speech to text
- 🔍 Detects filler words, speaking pace, word count
- 🤖 Groq LLM evaluates technical correctness
- 📊 Session history and score tracking

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a FREE Groq API key
- Go to https://console.groq.com
- Sign up for free
- Create an API key
- Paste it in the app when prompted

### 3. Run the app
```bash
streamlit run app.py
```

## Project Structure
```
mock_interviewer/
├── app.py           # Main Streamlit app
├── questions.py     # Question bank (DSA, OS, DBMS, HR)
├── recorder.py      # Mic recording
├── transcriber.py   # Whisper transcription
├── analyzer.py      # NLP analysis (fillers, pace)
├── evaluator.py     # Groq LLM evaluation
├── session.py       # Session history tracker
├── requirements.txt
└── sessions/        # Auto-created, stores session JSONs
```

## Topics Covered
- **DSA** — Stack/Queue, Binary Search, BST, DP, BFS/DFS
- **OS** — Deadlock, Process vs Thread, Paging, CPU Scheduling, Virtual Memory
- **DBMS** — Normalization, SQL vs NoSQL, Indexes, ACID, Joins
- **HR** — Tell me about yourself, Weaknesses, Projects, Career goals

## Notes
- Whisper "base" model runs on CPU (no GPU needed)
- First run downloads the Whisper model (~150MB), subsequent runs are instant
- All sessions are saved locally in the `sessions/` folder
