import streamlit as st
import uuid
import time
import os
from questions import questions
from recorder import start_recording, stop_recording, is_recording, cleanup
from transcriber import transcribe
from analyzer import analyze
from evaluator import evaluate
from session import save_result, get_all_sessions, compute_summary

st.set_page_config(
    page_title="AI Mock Interviewer",
    page_icon="🎯",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}
.stMarkdown, .stText, .stTitle, .stHeader, .stSubheader,
.stButton > button, .stTextInput input,
h1, h2, h3, p, li, label, .stMetric {
    font-family: 'Outfit', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
.big-question {
    font-size: 1.4rem;
    font-weight: 600;
    padding: 1.2rem 1.5rem;
    background: #f0f4ff;
    border-left: 5px solid #4f6ef7;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    color: #1a1a2e;
}
.score-card {
    text-align: center;
    padding: 1rem;
    border-radius: 12px;
    background: #f8f9fa;
}
.verdict-excellent { color: #2ecc71; font-weight: 700; font-size: 1.2rem; }
.verdict-good { color: #3498db; font-weight: 700; font-size: 1.2rem; }
.verdict-needs { color: #e67e22; font-weight: 700; font-size: 1.2rem; }
.verdict-poor { color: #e74c3c; font-weight: 700; font-size: 1.2rem; }
.ideal-box {
    background: #e8f5e9;
    border-left: 4px solid #27ae60;
    padding: 1rem 1.2rem;
    border-radius: 6px;
    font-size: 0.95rem;
    color: #1b5e20;
}
.transcript-box {
    background: #fff8e1;
    border-left: 4px solid #f39c12;
    padding: 1rem 1.2rem;
    border-radius: 6px;
    font-size: 0.95rem;
    font-style: italic;
    color: #4a3800;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ───────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if "current_q_idx" not in st.session_state:
    st.session_state.current_q_idx = 0
if "topic" not in st.session_state:
    st.session_state.topic = None
if "phase" not in st.session_state:
    st.session_state.phase = "setup"
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "rec_active" not in st.session_state:
    st.session_state.rec_active = False
if "rec_seconds" not in st.session_state:
    st.session_state.rec_seconds = 0

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("AI Mock Interviewer")
st.caption("Practice technical interviews with real-time AI feedback")
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — SETUP
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.phase == "setup":
    st.subheader("Let's set up your interview session")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.selectbox("📚 Choose topic", list(questions.keys()))
    with col2:
        num_q = st.slider("Number of questions", 1, 5, 3)

    api_key = st.text_input("🔑 Groq API Key (free at console.groq.com)", type="password",
                            help="Get your free API key from console.groq.com")

    record_duration = st.slider("⏱️ Max recording time per answer (seconds)", 30, 120, 60)

    st.markdown("---")
    if st.button("🚀 Start Interview", use_container_width=True, type="primary"):
        if not api_key:
            st.error("Please enter your Groq API key to continue.")
        else:
            import random
            pool = questions[topic].copy()
            random.shuffle(pool)
            st.session_state.selected_questions = pool[:num_q]
            st.session_state.topic = topic
            st.session_state.api_key = api_key
            st.session_state.record_duration = record_duration
            st.session_state.current_q_idx = 0
            st.session_state.phase = "interview"
            st.rerun()

    all_sessions = get_all_sessions()
    if all_sessions:
        st.markdown("---")
        st.subheader("📊 Past Sessions")
        for s in all_sessions[:3]:
            summary = compute_summary(s)
            with st.expander(f"Session {s['session_id']} — {s['date']} | Avg score: {summary.get('average_score', 'N/A')}/10"):
                st.write(f"**Questions answered:** {summary.get('total_questions', 0)}")
                st.write(f"**Total filler words:** {summary.get('total_fillers', 0)}")
                if summary.get("topic_scores"):
                    st.write("**Topic scores:**", summary["topic_scores"])

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — INTERVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "interview":
    q_list = st.session_state.selected_questions
    idx = st.session_state.current_q_idx
    topic = st.session_state.topic

    progress = idx / len(q_list)
    st.progress(progress, text=f"Question {idx + 1} of {len(q_list)} — Topic: {topic}")

    current_q = q_list[idx]
    st.markdown(f'<div class="big-question">❓ {current_q["question"]}</div>', unsafe_allow_html=True)
    st.info("💡 Click **Start Recording**, speak your answer, then click **Stop & Evaluate**.")

    col1, col2 = st.columns(2)

    with col1:
        if not st.session_state.rec_active:
            start_clicked = st.button("🎙️ Start Recording", use_container_width=True, type="primary")
        else:
            start_clicked = False
            st.button("🔴 Recording...", use_container_width=True, disabled=True)

    with col2:
        stop_clicked = st.button("⏹️ Stop & Evaluate", use_container_width=True,
                                  disabled=not st.session_state.rec_active)

    if start_clicked:
        st.session_state.rec_active = True
        st.session_state.rec_seconds = st.session_state.record_duration
        start_recording(max_duration=st.session_state.record_duration)
        st.rerun()

    if st.session_state.rec_active:
        import time as time_module
        timer_box = st.empty()
        secs = st.session_state.rec_seconds
        timer_box.markdown(
            f"<div style='text-align:center;font-size:3rem;font-weight:700;color:#e74c3c;padding:0.5rem;font-family:Outfit,sans-serif;'>⏱️ {secs}s remaining</div>",
            unsafe_allow_html=True
        )

        if not stop_clicked and secs > 0:
            time_module.sleep(1)
            st.session_state.rec_seconds -= 1
            st.rerun()
        else:
            timer_box.empty()
            st.session_state.rec_active = False
            with st.spinner("Saving recording..."):
                audio_path = stop_recording()

            if not audio_path:
                st.error("No audio detected. Please try again.")
                st.rerun()
            else:
                with st.spinner("Transcribing your answer..."):
                    transcript = transcribe(audio_path)

                if not transcript or len(transcript.split()) < 3:
                    st.error("Could not detect speech. Please try again.")
                    st.rerun()
                else:
                    with st.spinner("Analyzing speech patterns..."):
                        analysis = analyze(transcript)
                    with st.spinner("AI is evaluating your answer..."):
                        evaluation = evaluate(
                            current_q["question"],
                            transcript,
                            current_q["ideal_answer"],
                            st.session_state.api_key
                        )
                    save_result(
                        st.session_state.session_id,
                        topic,
                        current_q["question"],
                        transcript,
                        analysis,
                        evaluation
                    )
                    st.session_state.last_result = {
                        "question": current_q["question"],
                        "ideal_answer": current_q["ideal_answer"],
                        "transcript": transcript,
                        "analysis": analysis,
                        "evaluation": evaluation
                    }
                    cleanup()
                    st.session_state.rec_seconds = 0
                    st.session_state.phase = "result"
                    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — RESULT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "result":
    r = st.session_state.last_result
    ev = r["evaluation"]
    an = r["analysis"]
    idx = st.session_state.current_q_idx
    q_list = st.session_state.selected_questions

    st.subheader("📋 Feedback")

    verdict = ev.get("verdict", "N/A")
    score = ev.get("score", 0)
    verdict_class = {
        "Excellent": "verdict-excellent",
        "Good": "verdict-good",
        "Needs Improvement": "verdict-needs",
        "Poor": "verdict-poor"
    }.get(verdict, "verdict-needs")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏆 Score", f"{score}/10")
    col2.metric("🗣️ Filler words", an["filler_count"])
    col3.metric("💬 Words/min", an["wpm"])
    col4.metric("📝 Words spoken", an["word_count"])

    st.markdown(f'<div class="score-card"><span class="{verdict_class}">{verdict}</span></div>',
                unsafe_allow_html=True)

    st.markdown("**Your answer (transcribed):**")
    st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)

    st.markdown("**AI feedback:**")
    st.write(ev.get("feedback", ""))

    if ev.get("missing_concepts") and ev["missing_concepts"] != "None":
        st.warning(f"⚠️ **Missing concepts:** {ev['missing_concepts']}")

    if an["fillers_found"]:
        st.error(f"🔴 **Filler words detected:** {', '.join(an['fillers_found'])}")

    st.info(f"🎙️ **Pace:** {an['pace_feedback']}")

    with st.expander("💡 See ideal answer"):
        st.markdown(f'<div class="ideal-box">{r["ideal_answer"]}</div>', unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Re-record this answer", use_container_width=True):
            st.session_state.phase = "interview"
            st.rerun()
    with col2:
        is_last = idx >= len(q_list) - 1
        btn_label = "📊 View Session Summary" if is_last else "➡️ Next Question"
        if st.button(btn_label, use_container_width=True, type="primary"):
            if is_last:
                st.session_state.phase = "summary"
            else:
                st.session_state.current_q_idx += 1
                st.session_state.phase = "interview"
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 4 — SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "summary":
    from session import load_session

    st.subheader("📊 Session Summary")
    session = load_session(st.session_state.session_id)
    summary = compute_summary(session)

    col1, col2, col3 = st.columns(3)
    col1.metric("📝 Questions answered", summary.get("total_questions", 0))
    col2.metric("🏆 Average score", f"{summary.get('average_score', 0)}/10")
    col3.metric("🗣️ Total filler words", summary.get("total_fillers", 0))

    scores = summary.get("scores_list", [])
    if scores:
        import pandas as pd
        df = pd.DataFrame({"Question": list(range(1, len(scores)+1)), "Score": scores})
        st.line_chart(df.set_index("Question"))

    if summary.get("topic_scores"):
        st.markdown("**Topic scores:**")
        for t, s in summary["topic_scores"].items():
            st.write(f"- **{t}:** {s}/10")

    avg = summary.get("average_score", 0)
    if avg >= 8:
        st.success("🎉 Outstanding performance! You are interview-ready.")
    elif avg >= 6:
        st.info("👍 Good job! Focus on the missing concepts and reduce filler words.")
    else:
        st.warning("📚 Keep practicing! Review the ideal answers and try again.")

    if st.button("🔄 Start New Session", use_container_width=True, type="primary"):
        for key in ["session_id", "current_q_idx", "topic", "phase", "last_result",
                    "selected_questions", "api_key", "rec_active", "rec_seconds"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
