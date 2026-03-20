import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def evaluate(question: str, user_answer: str, ideal_answer: str, api_key: str) -> dict:
    """Evaluate user's answer using Groq LLM and return score + feedback."""

    # Clean the API key — remove any spaces or newlines user might have copied
    api_key = api_key.strip()

    prompt = f"""You are a strict but fair technical interviewer evaluating a student's spoken answer.

QUESTION: {question}

IDEAL ANSWER: {ideal_answer}

STUDENT'S ANSWER: {user_answer}

Evaluate the student's answer and respond ONLY in this exact format (no extra text):
SCORE: <number from 0 to 10>
FEEDBACK: <2-3 sentences about what was good and what was missing>
MISSING: <key concepts the student missed, comma-separated, or None>
VERDICT: <exactly one of: Excellent, Good, Needs Improvement, Poor>
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=20
        )

        if response.status_code == 401:
            return _error_result("Invalid API key. Please check your Groq API key.")
        elif response.status_code == 400:
            return _error_result(f"Bad request: {response.text[:200]}")
        elif response.status_code != 200:
            return _error_result(f"API error {response.status_code}: {response.text[:200]}")

        content = response.json()["choices"][0]["message"]["content"].strip()

        # Parse response safely
        score = _extract(content, "SCORE:", "FEEDBACK:")
        feedback = _extract(content, "FEEDBACK:", "MISSING:")
        missing = _extract(content, "MISSING:", "VERDICT:")
        verdict = _extract(content, "VERDICT:", None)

        # Convert score to float
        try:
            score = float(score.strip())
        except:
            score = 5.0

        return {
            "score": score,
            "feedback": feedback.strip() if feedback else "No feedback generated.",
            "missing_concepts": missing.strip() if missing else "None",
            "verdict": verdict.strip() if verdict else "Needs Improvement",
            "error": None
        }

    except requests.exceptions.ConnectionError:
        return _error_result("No internet connection. Please check your network.")
    except requests.exceptions.Timeout:
        return _error_result("Request timed out. Please try again.")
    except Exception as e:
        return _error_result(str(e))


def _extract(text: str, start_key: str, end_key: str) -> str:
    """Extract value between two keys."""
    try:
        start = text.find(start_key)
        if start == -1:
            return ""
        start += len(start_key)
        if end_key:
            end = text.find(end_key, start)
            if end == -1:
                return text[start:].strip()
            return text[start:end].strip()
        return text[start:].strip()
    except:
        return ""


def _error_result(message: str) -> dict:
    return {
        "score": 0,
        "feedback": f"Error: {message}",
        "missing_concepts": "N/A",
        "verdict": "Error",
        "error": message
    }
