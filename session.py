import json
import os
from datetime import datetime

SESSIONS_DIR = "sessions"

def save_result(session_id: str, topic: str, question: str, transcript: str, analysis: dict, evaluation: dict):
    """Save a single question result to the session file."""
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    filepath = os.path.join(SESSIONS_DIR, f"{session_id}.json")

    # Load existing session or create new
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            session = json.load(f)
    else:
        session = {
            "session_id": session_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "results": []
        }

    session["results"].append({
        "topic": topic,
        "question": question,
        "transcript": transcript,
        "analysis": analysis,
        "evaluation": evaluation
    })

    with open(filepath, "w") as f:
        json.dump(session, f, indent=2)

def load_session(session_id: str) -> dict:
    filepath = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

def get_all_sessions() -> list:
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    sessions = []
    for fname in os.listdir(SESSIONS_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(SESSIONS_DIR, fname)) as f:
                sessions.append(json.load(f))
    return sorted(sessions, key=lambda x: x.get("date", ""), reverse=True)

def compute_summary(session: dict) -> dict:
    results = session.get("results", [])
    if not results:
        return {}

    scores = [r["evaluation"]["score"] for r in results if r["evaluation"].get("score") is not None]
    fillers = [r["analysis"]["filler_count"] for r in results]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    total_fillers = sum(fillers)

    topic_scores = {}
    for r in results:
        t = r["topic"]
        if t not in topic_scores:
            topic_scores[t] = []
        topic_scores[t].append(r["evaluation"]["score"])
    topic_avg = {t: round(sum(v)/len(v), 1) for t, v in topic_scores.items()}

    return {
        "total_questions": len(results),
        "average_score": avg_score,
        "total_fillers": total_fillers,
        "topic_scores": topic_avg,
        "scores_list": scores
    }
