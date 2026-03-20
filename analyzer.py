import re

FILLER_WORDS = [
    "umm", "um", "uh", "like", "basically", "you know",
    "actually", "literally", "kind of", "sort of", "i mean",
    "right", "so yeah", "okay so", "hmm"
]

def analyze(transcript: str) -> dict:
    """Analyze transcript for filler words, word count, estimated WPM."""
    text_lower = transcript.lower()
    words = transcript.split()
    word_count = len(words)

    # Count filler words
    filler_count = 0
    filler_found = []
    for filler in FILLER_WORDS:
        pattern = r'\b' + re.escape(filler) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            filler_count += len(matches)
            filler_found.append(f"{filler} ({len(matches)}x)")

    # Estimate speaking duration from word count (avg 130 WPM)
    estimated_duration_min = word_count / 130
    wpm = round(word_count / estimated_duration_min) if estimated_duration_min > 0 else 0

    # Pace feedback
    if wpm < 90:
        pace_feedback = "Too slow — try to speak with more confidence."
    elif wpm > 160:
        pace_feedback = "Too fast — slow down so the interviewer can follow."
    else:
        pace_feedback = "Good pace — clear and comfortable to follow."

    # Sentence completeness (rough check)
    sentences = re.split(r'[.!?]', transcript)
    complete_sentences = [s.strip() for s in sentences if len(s.strip().split()) >= 4]
    completeness = round(len(complete_sentences) / max(len(sentences), 1) * 100)

    return {
        "word_count": word_count,
        "wpm": wpm,
        "pace_feedback": pace_feedback,
        "filler_count": filler_count,
        "fillers_found": filler_found,
        "completeness_pct": completeness
    }
