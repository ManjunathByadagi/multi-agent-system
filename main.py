import asyncio
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Research Assistant", layout="wide")


def run_async(coro):
    return asyncio.run(coro)


def missing_environment_keys():
    keys = []
    if not os.getenv("OPENAI_API_KEY"):
        keys.append("OPENAI_API_KEY")
    if not os.getenv("TAVILY_API_KEY"):
        keys.append("TAVILY_API_KEY")
    return keys


def load_agents():
    from agents.planner import planner
    from agents.researcher import researcher
    from agents.writer import writer
    from agents.critic import critic
    from memory.store import save

    return planner, researcher, writer, critic, save


def render_error(step, error):
    st.error(f"{step} failed: {error}")
    with st.expander("Show technical details"):
        st.exception(error)


def run_full_pipeline(query):
    planner, researcher, writer, critic, save = load_agents()

    st.markdown("---")
    st.markdown("## AI Thinking...")
    progress = st.progress(0)
    status = st.empty()

    status.info("Planning...")
    tasks = planner(query)
    progress.progress(20)

    status.info("Researching...")
    research_data = run_async(researcher(query, tasks))
    progress.progress(45)

    status.info("Writing...")
    draft = writer(research_data)
    progress.progress(70)

    status.info("Evaluating...")
    critique = critic(draft)
    progress.progress(90)

    for _ in range(2):
        improvements = critique.get("improvements", [])
        if critique.get("score", 0) >= 8 or not improvements:
            break
        status.info("Improving draft...")
        draft = writer(research_data + improvements)
        critique = critic(draft)

    status.success("Complete")
    progress.progress(100)
    save(query, draft)

    st.session_state["draft"] = draft
    st.session_state["critique"] = critique
    st.session_state["tasks"] = tasks
    st.session_state["research_data"] = research_data


def run_single_agent(section, query):
    planner, researcher, writer, critic, _ = load_agents()

    if section == "planner":
        box = st.empty()
        box.info("Generating plan...")
        tasks = planner(query)
        box.success("Plan ready")
        for index, task in enumerate(tasks, 1):
            st.write(f"{index}. {task}")

    elif section == "research":
        box = st.empty()
        box.info("Researching...")
        tasks = planner(query)
        research_data = run_async(researcher(query, tasks))
        box.success("Research complete")
        for result in research_data:
            st.write("- ", result[:300] + "...")

    elif section == "writer":
        box = st.empty()
        box.info("Writing...")
        tasks = planner(query)
        research_data = run_async(researcher(query, tasks))
        draft = writer(research_data)
        box.success("Draft ready")
        st.markdown(draft)

    elif section == "critic":
        box = st.empty()
        box.info("Evaluating...")
        tasks = planner(query)
        research_data = run_async(researcher(query, tasks))
        draft = writer(research_data)
        critique = critic(draft)
        box.success("Evaluation complete")
        st.progress(min(int(critique.get("score", 0) * 10), 100))
        st.json(critique)


st.markdown(
    """
<style>
.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 20% 20%, #0ea5e9, #020617 54%);
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
footer {
    display: none;
}

.hero {
    text-align: center;
    padding: 24px 12px 18px;
}

.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(34, 211, 238, 0.16);
    color: #67e8f9;
    border: 1px solid rgba(103, 232, 249, 0.22);
    margin-bottom: 16px;
    font-size: 13px;
    letter-spacing: 0.08em;
}

.typing {
    font-size: clamp(30px, 4vw, 56px);
    line-height: 1.08;
    font-weight: 900;
    background: linear-gradient(90deg, #e0f2fe, #67e8f9, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

.hero-sub {
    font-size: 16px;
    color: #e0f2fe;
    margin-top: 14px;
    margin-bottom: 22px;
}

.stTextInput input {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(34, 211, 238, 0.35);
    border-radius: 12px;
    color: white;
}

.stTextInput input:focus {
    border-color: #22d3ee;
    box-shadow: 0 0 0 1px #22d3ee;
}

.stButton button,
.stFormSubmitButton button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg, #22d3ee, #0ea5e9);
    color: white;
    border: 0;
    font-weight: 700;
}

.agent-card {
    min-height: 92px;
    background: rgba(34, 211, 238, 0.09);
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid rgba(34, 211, 238, 0.22);
    color: #f0f9ff;
}

.agent-card b {
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
    <div class="badge">AI SYSTEM ACTIVE</div>
    <div class="typing">Research anything with</div>
    <div class="typing">AI that thinks in teams</div>
    <div class="hero-sub">Multi-agent intelligence (Planner - Researcher - Writer - Critic)</div>
</div>
""",
    unsafe_allow_html=True,
)

missing_keys = missing_environment_keys()
if missing_keys:
    st.error(
        "Missing environment variable(s): "
        + ", ".join(missing_keys)
        + ". Add them to .env and restart Streamlit."
    )

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.form("research_form", clear_on_submit=False):
        query_input = st.text_input(
            "Research query",
            placeholder="Ask anything...",
            label_visibility="collapsed",
            key="query_input",
        )
        run = st.form_submit_button("Start")

if run:
    query = query_input.strip()
    if not query:
        st.warning("Enter a research question first.")
    elif missing_keys:
        st.warning("Fix the missing .env values above, then restart Streamlit.")
    else:
        st.session_state["query"] = query
        st.session_state["section"] = None
        st.session_state.pop("draft", None)
        st.session_state.pop("critique", None)
        try:
            run_full_pipeline(query)
        except Exception as error:
            render_error("Pipeline", error)

st.markdown("### Agents")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Planner", key="planner_button"):
        st.session_state["section"] = "planner"
    st.markdown('<div class="agent-card">Planner<br><b>Task breakdown</b></div>', unsafe_allow_html=True)

with col2:
    if st.button("Researcher", key="researcher_button"):
        st.session_state["section"] = "research"
    st.markdown('<div class="agent-card">Researcher<br><b>Web context</b></div>', unsafe_allow_html=True)

with col3:
    if st.button("Writer", key="writer_button"):
        st.session_state["section"] = "writer"
    st.markdown('<div class="agent-card">Writer<br><b>Draft answer</b></div>', unsafe_allow_html=True)

with col4:
    if st.button("Critic", key="critic_button"):
        st.session_state["section"] = "critic"
    st.markdown('<div class="agent-card">Critic<br><b>Quality score</b></div>', unsafe_allow_html=True)

query = st.session_state.get("query", "")
section = st.session_state.get("section")

if query:
    st.caption(f"Current query: {query}")

if section:
    if not query:
        st.warning("Enter a query and click Start once before using individual agents.")
    elif missing_keys:
        st.warning("Fix the missing .env values above, then restart Streamlit.")
    else:
        try:
            run_single_agent(section, query)
        except Exception as error:
            render_error(section.title(), error)

if st.session_state.get("draft"):
    st.markdown("## Final Answer")
    st.markdown(
        f"""
<div style="
    background: rgba(255, 255, 255, 0.08);
    padding: 24px;
    border-radius: 12px;
    color: #f8fafc;
    border: 1px solid rgba(34, 211, 238, 0.2);
">
{st.session_state["draft"]}
</div>
""",
        unsafe_allow_html=True,
    )

    critique = st.session_state.get("critique", {})
    st.progress(min(int(critique.get("score", 0) * 10), 100))
    with st.expander("Critic details"):
        st.json(critique)
