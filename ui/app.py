# ============================================================
# ui/app.py  —  DeepResearcher Interactive UI
# Dark command-center aesthetic — like a research terminal
# ============================================================

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from graph.research_graph import run_research

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="DeepResearcher",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background-color: #080c12 !important;
    color: #e2e8f0 !important;
}

.stApp {
    background: #080c12 !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1100px !important; }

/* ── Hero section ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}

.hero-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #00d4ff;
    border: 1px solid #00d4ff33;
    background: #00d4ff0a;
    padding: 0.3rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 4rem;
    font-weight: 800;
    line-height: 1;
    background: linear-gradient(135deg, #ffffff 0%, #00d4ff 50%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}

.hero-sub {
    font-size: 1.05rem;
    color: #64748b;
    font-weight: 400;
    margin-bottom: 2.5rem;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: #0f1623 !important;
    border: 1px solid #1e2d42 !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.2rem !important;
    transition: border 0.2s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 3px #00d4ff15 !important;
}

.stTextInput > div > div > input::placeholder {
    color: #334155 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #00d4ff, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2.5rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px #00d4ff30 !important;
}

/* ── Pipeline cards ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem;
    margin: 2rem 0;
}

.pipeline-card {
    background: #0f1623;
    border: 1px solid #1e2d42;
    border-radius: 12px;
    padding: 1rem 0.75rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.pipeline-card.active {
    border-color: #00d4ff;
    background: #00d4ff0a;
    box-shadow: 0 0 20px #00d4ff20;
}

.pipeline-card.done {
    border-color: #10b981;
    background: #10b9810a;
}

.pipeline-card .icon {
    font-size: 1.6rem;
    margin-bottom: 0.4rem;
    display: block;
}

.pipeline-card .label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: #475569;
    text-transform: uppercase;
}

.pipeline-card.active .label { color: #00d4ff; }
.pipeline-card.done .label   { color: #10b981; }

/* ── Stats row ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}

.stat-card {
    background: #0f1623;
    border: 1px solid #1e2d42;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}

.stat-number {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #00d4ff;
    line-height: 1;
}

.stat-label {
    font-size: 0.75rem;
    color: #475569;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── Report area ── */
.report-container {
    background: #0d1520;
    border: 1px solid #1e2d42;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin: 1.5rem 0;
    line-height: 1.8;
}

.report-container h1 {
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    color: #f1f5f9 !important;
    border-bottom: 1px solid #1e2d42 !important;
    padding-bottom: 1rem !important;
    margin-bottom: 1.5rem !important;
}

.report-container h2 {
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: #00d4ff !important;
    margin-top: 2rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

.report-container h3 {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    margin-top: 1.2rem !important;
}

.report-container p {
    color: #94a3b8 !important;
    font-size: 0.95rem !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: #0f1623 !important;
    border: 1px solid #10b981 !important;
    color: #10b981 !important;
    border-radius: 10px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    padding: 0.7rem 1.5rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

.stDownloadButton > button:hover {
    background: #10b9810f !important;
    box-shadow: 0 0 20px #10b98130 !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #00d4ff, #7c3aed) !important;
    border-radius: 100px !important;
}

.stProgress > div {
    background: #1e2d42 !important;
    border-radius: 100px !important;
    height: 6px !important;
}

/* ── Source tags ── */
.source-tag {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    margin: 0.2rem;
}

.tag-tavily    { background: #00d4ff15; color: #00d4ff; border: 1px solid #00d4ff30; }
.tag-wikipedia { background: #f59e0b15; color: #f59e0b; border: 1px solid #f59e0b30; }
.tag-none      { background: #ef444415; color: #ef4444; border: 1px solid #ef444430; }

/* ── Divider ── */
hr { border-color: #1e2d42 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0f1623 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #1e2d42 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
}

.stTabs [aria-selected="true"] {
    background: #1e2d42 !important;
    color: #e2e8f0 !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #00d4ff !important;
}

/* ── Log box ── */
.log-box {
    background: #060a0f;
    border: 1px solid #1e2d42;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #475569;
    line-height: 1.8;
    max-height: 200px;
    overflow-y: auto;
}

.log-box .log-ok   { color: #10b981; }
.log-box .log-warn { color: #f59e0b; }
.log-box .log-err  { color: #ef4444; }
.log-box .log-info { color: #00d4ff; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ LangGraph · Ollama · Tavily</div>
    <div class="hero-title">DeepResearcher</div>
    <div class="hero-sub">Enter any topic — get a comprehensive AI research report as PDF</div>
</div>
""", unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])

with col_input:
    topic = st.text_input(
        label="topic",
        label_visibility="collapsed",
        placeholder="e.g.  Impact of quantum computing on cybersecurity in 2025",
        key="topic_input",
    )

with col_btn:
    run = st.button("🚀  Research", use_container_width=True)


# ── Pipeline cards (always visible) ──────────────────────────
def pipeline_cards(step: str = ""):
    steps = [
        ("📋", "Planner",    "planner_done"),
        ("🔍", "Researcher", "researcher_done"),
        ("📝", "Summarizer", "summarizer_done"),
        ("✍️",  "Writer",     "writer_done"),
        ("📄", "PDF",        "pdf_done"),
    ]
    order = [s[2] for s in steps]

    cards_html = '<div class="pipeline-grid">'
    for icon, label, done_key in steps:
        if step == done_key:
            css = "active"
        elif done_key in order[:order.index(step)+1] if step in order else []:
            css = "done"
        else:
            css = ""
        cards_html += f"""
        <div class="pipeline-card {css}">
            <span class="icon">{icon}</span>
            <div class="label">{label}</div>
        </div>"""
    cards_html += '</div>'
    return cards_html


pipeline_placeholder = st.empty()
pipeline_placeholder.markdown(pipeline_cards(""), unsafe_allow_html=True)


# ── Run ───────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.markdown("""
        <div style="background:#ef444415;border:1px solid #ef444430;border-radius:10px;
        padding:0.8rem 1.2rem;color:#ef4444;font-size:0.85rem;margin-top:1rem;">
        ⚠️  Please enter a research topic before starting.
        </div>""", unsafe_allow_html=True)
        st.stop()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Progress bar
    progress = st.progress(0)

    # Run pipeline
    with st.spinner(""):
        st.markdown("""
        <div style="text-align:center;padding:0.5rem;
        font-family:'Space Mono',monospace;font-size:0.75rem;
        color:#475569;letter-spacing:0.1em;">
        PIPELINE RUNNING — this takes 2–4 minutes…
        </div>""", unsafe_allow_html=True)

        result = run_research(topic)

    # Update pipeline cards to done
    pipeline_placeholder.markdown(pipeline_cards("pdf_done"), unsafe_allow_html=True)
    progress.progress(1.0)

    # ── Error ─────────────────────────────────────────────────
    if result.get("error") and result.get("current_step") == "validation_error":
        st.markdown(f"""
        <div style="background:#ef444415;border:1px solid #ef444430;border-radius:10px;
        padding:1rem 1.2rem;color:#ef4444;margin:1rem 0;">
        ❌  <strong>Invalid topic:</strong> {result['error']}
        </div>""", unsafe_allow_html=True)
        st.stop()

    # ── Stats row ─────────────────────────────────────────────
    q_count  = len(result.get("sub_questions", []))
    s_count  = len(result.get("search_results", []))
    r_chars  = len(result.get("report", ""))

    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-number">{q_count}</div>
            <div class="stat-label">Sub-questions</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{s_count}</div>
            <div class="stat-label">Searches</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{r_chars:,}</div>
            <div class="stat-label">Report chars</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📄  REPORT", "🔍  SOURCES", "📋  QUESTIONS"])

    with tab1:
        report = result.get("report", "")
        if report:
            st.markdown(f'<div class="report-container">', unsafe_allow_html=True)
            st.markdown(report)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Report could not be generated.")

        st.markdown("<br>", unsafe_allow_html=True)

        pdf_path = result.get("pdf_path", "")
        if pdf_path and Path(pdf_path).exists():
            with open(pdf_path, "rb") as fh:
                st.download_button(
                    label="⬇  DOWNLOAD PDF REPORT",
                    data=fh.read(),
                    file_name=Path(pdf_path).name,
                    mime="application/pdf",
                    use_container_width=True,
                )

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        for r in result.get("search_results", []):
            src  = r.get("source", "none")
            css  = f"tag-{src}"
            icon = "🌐" if src == "tavily" else "📖" if src == "wikipedia" else "❌"
            hits = len(r.get("results", []))
            st.markdown(f"""
            <div style="background:#0f1623;border:1px solid #1e2d42;border-radius:10px;
            padding:0.8rem 1rem;margin-bottom:0.6rem;display:flex;
            align-items:center;gap:0.8rem;">
                <span class="source-tag {css}">{icon} {src.upper()}</span>
                <span style="font-size:0.85rem;color:#94a3b8;flex:1;">{r['question']}</span>
                <span style="font-family:'Space Mono',monospace;font-size:0.7rem;
                color:#475569;">{hits} results</span>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        for i, q in enumerate(result.get("sub_questions", []), 1):
            st.markdown(f"""
            <div style="background:#0f1623;border:1px solid #1e2d42;border-radius:10px;
            padding:0.9rem 1.2rem;margin-bottom:0.6rem;display:flex;gap:1rem;align-items:start;">
                <span style="font-family:'Space Mono',monospace;font-size:0.8rem;
                color:#00d4ff;min-width:1.5rem;">0{i}</span>
                <span style="color:#94a3b8;font-size:0.9rem;">{q}</span>
            </div>
            """, unsafe_allow_html=True)