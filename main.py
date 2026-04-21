import streamlit as st
import asyncio
import time

from agents.planner import planner
from agents.researcher import researcher
from agents.writer import writer
from agents.critic import critic
from memory.store import save

st.set_page_config(page_title="AI Research Assistant", layout="wide")

# ================= UI ================= #

st.markdown("""
<style>

/* REMOVE ALL STREAMLIT SPACING */
.block-container { padding: 0 !important; }
[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; }
section.main > div { padding: 0 !important; }
.stApp > div:first-child { padding-top: 0 !important; }

/* Hide default */
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stToolbar"] {display: none;}

/* 🌊 CYAN GRADIENT BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 20% 20%, #0ea5e9, #020617);
}

/* HERO */
.hero {
    text-align: center;
    padding-top: 40px;
}

/* TITLE */
.typing {
  font-size: clamp(28px, 3.8vw, 54px);
  line-height: 1.1;
  font-weight: 900;
  background: linear-gradient(90deg, #67e8f9, #22d3ee);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  max-width: 800px;
  margin: auto;
  text-align: center;
}

/* Subtitle */
.hero-sub {
    font-size: 16px;
    color: #e0f2fe;
    margin-bottom: 20px;
}

/* Badge */
.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(34,211,238,0.15);
    color: #67e8f9;
    margin-bottom: 16px;
}

/* INPUT */
.stTextInput input {
    width: 100% !important;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(34,211,238,0.3);
    border-radius: 16px;
    padding: 14px;
    color: white;
}

/* Glow */
.stTextInput input:focus {
    border: 1px solid #22d3ee !important;
    box-shadow: 0 0 12px #22d3ee;
}

/* BUTTON CENTER */
div[data-testid="stButton"] {
    display: flex;
    justify-content: center;
}

.stButton button {
    width: 100%;
    background: linear-gradient(90deg, #22d3ee, #0ea5e9);
    border-radius: 16px;
    padding: 10px;
    color: white;
    font-weight: 600;
}

/* CARDS */
.agent-card {
    background: rgba(34,211,238,0.08);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid rgba(34,211,238,0.2);
    backdrop-filter: blur(10px);
    transition: 0.3s;
}

.agent-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 0 15px rgba(34,211,238,0.4);
}

</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
<div class="badge">AI SYSTEM ACTIVE</div>

<div class="typing">Research anything with</div>
<div class="typing">AI that thinks in teams</div>

<div class="hero-sub">
Multi-agent intelligence (Planner • Researcher • Writer • Critic)
</div>
</div>
""", unsafe_allow_html=True)

# INPUT CENTERED
col1, col2, col3 = st.columns([1,2,1])

with col2:
    query = st.text_input("", placeholder="Ask anything...")
    run = st.button("🚀 Start", use_container_width=True)

# SAVE QUERY
if run and query:
    st.session_state["query"] = query

# ================= CARDS ================= #

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🧭 Planner"):
        st.session_state["section"] = "planner"
    st.markdown('<div class="agent-card">🧭<br><b>Planner</b></div>', unsafe_allow_html=True)

with col2:
    if st.button("🔍 Researcher"):
        st.session_state["section"] = "research"
    st.markdown('<div class="agent-card">🔍<br><b>Researcher</b></div>', unsafe_allow_html=True)

with col3:
    if st.button("✍️ Writer"):
        st.session_state["section"] = "writer"
    st.markdown('<div class="agent-card">✍️<br><b>Writer</b></div>', unsafe_allow_html=True)

with col4:
    if st.button("🧪 Critic"):
        st.session_state["section"] = "critic"
    st.markdown('<div class="agent-card">🧪<br><b>Critic</b></div>', unsafe_allow_html=True)

section = st.session_state.get("section")
query = st.session_state.get("query")

# ================= INTERACTIVE AGENTS ================= #

if section == "planner" and query:
    box = st.empty()
    box.info("🧭 Generating plan...")
    tasks = planner(query)
    box.success("✅ Plan ready")

    for i, t in enumerate(tasks, 1):
        st.write(f"{i}. {t}")

elif section == "research" and query:
    box = st.empty()
    box.info("🔍 Researching...")
    tasks = planner(query)
    research_data = asyncio.run(researcher(query, tasks))
    box.success("✅ Done")

    for r in research_data:
        st.write("- ", r[:200] + "...")

elif section == "writer" and query:
    box = st.empty()
    box.info("✍️ Writing...")
    tasks = planner(query)
    research_data = asyncio.run(researcher(query, tasks))
    draft = writer(research_data)
    box.success("✅ Draft ready")

    st.markdown(draft)

elif section == "critic" and query:
    box = st.empty()
    box.info("🧪 Evaluating...")
    tasks = planner(query)
    research_data = asyncio.run(researcher(query, tasks))
    draft = writer(research_data)
    critique = critic(draft)
    box.success("✅ Done")

    st.progress(int(critique.get("score", 0) * 10))

# ================= FULL PIPELINE ================= #

if run and query:

    st.markdown("---")
    st.markdown("## 🤖 AI Thinking...")

    status = st.empty()

    status.info("🧭 Planning...")
    tasks = planner(query)
    time.sleep(0.3)
    status.success("✅ Plan ready")

    status = st.empty()
    status.info("🔍 Researching...")
    research_data = asyncio.run(researcher(query, tasks))
    time.sleep(0.3)
    status.success("✅ Done")

    status = st.empty()
    status.info("✍️ Writing...")
    draft = writer(research_data)
    time.sleep(0.3)
    status.success("✅ Draft ready")

    status = st.empty()
    status.info("🧪 Evaluating...")
    critique = critic(draft)

    while critique.get("score", 0) < 8:
        draft = writer(research_data + critique.get("improvements", []))
        critique = critic(draft)

    status.success("✅ Complete")

    st.markdown("## ✍️ Final Answer")

    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.08);
            padding: 30px;
            border-radius: 20px;
        ">
        {draft}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(int(critique.get("score", 0) * 10))

    save(query, draft)