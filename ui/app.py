# ============================================================
# ui/app.py  —  DeepResearcher Interactive UI
# Clean white Google-style aesthetic
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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #FFFFFF !important;
    color: #1a1a2e !important;
}
.stApp { background: #FFFFFF !important; }

/* ── Hide chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1100px !important; }

/* ── Hero ── */
.hero { text-align: center; padding: 3rem 0 2rem; }
.hero-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #1A73E8;
    border: 1px solid #1A73E820;
    background: #1A73E808;
    padding: 0.3rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 4rem;
    font-weight: 600;
    line-height: 1;
    background: linear-gradient(135deg, #1a1a2e 0%, #1A73E8 60%, #0d47a1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero-sub {
    font-size: 1.05rem;
    color: #6B7280;
    font-weight: 400;
    margin-bottom: 2.5rem;
}

/* ── Input ── */
.stTextInput > div > div > input {
    background: #F9FAFB !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.2rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #1A73E8 !important;
    box-shadow: 0 0 0 3px #1A73E815 !important;
}
.stTextInput > div > div > input::placeholder { color: #9CA3AF !important; }

/* ── Button ── */
.stButton > button {
    background: #1A73E8 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #1557B0 !important;
    box-shadow: 0 4px 15px #1A73E830 !important;
    transform: translateY(-1px) !important;
}

/* ── Pipeline cards ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem;
    margin: 2rem 0;
}
.pipeline-card {
    background: #F9FAFB;
    border: 1.5px solid #E5E7EB;
    border-radius: 12px;
    padding: 1rem 0.75rem;
    text-align: center;
    transition: all 0.3s ease;
}
.pipeline-card.active {
    border-color: #1A73E8;
    background: #1A73E808;
    box-shadow: 0 0 16px #1A73E820;
}
.pipeline-card.done {
    border-color: #10b981;
    background: #10b98108;
}
.pipeline-card .icon { font-size: 1.6rem; margin-bottom: 0.4rem; display: block; }
.pipeline-card .label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: #9CA3AF;
    text-transform: uppercase;
}
.pipeline-card.active .label { color: #1A73E8; }
.pipeline-card.done .label   { color: #10b981; }

/* ── Stats ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.stat-card {
    background: #F9FAFB;
    border: 1.5px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.stat-number {
    font-family: 'DM Mono', monospace;
    font-size: 2rem;
    font-weight: 500;
    color: #1A73E8;
    line-height: 1;
}
.stat-label {
    font-size: 0.75rem;
    color: #9CA3AF;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── Report ── */
.report-container {
    background: #F9FAFB;
    border: 1.5px solid #E5E7EB;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin: 1.5rem 0;
    line-height: 1.8;
}
.report-container h1 {
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    color: #1a1a2e !important;
    border-bottom: 1.5px solid #E5E7EB !important;
    padding-bottom: 1rem !important;
    margin-bottom: 1.5rem !important;
}
.report-container h2 {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #1A73E8 !important;
    margin-top: 2rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
.report-container h3 {
    font-size: 1rem !important;
    font-weight: 500 !important;
    color: #374151 !important;
}
.report-container p { color: #4B5563 !important; font-size: 0.95rem !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background: #FFFFFF !important;
    border: 1.5px solid #10b981 !important;
    color: #10b981 !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.7rem 1.5rem !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background: #10b98108 !important;
    box-shadow: 0 4px 15px #10b98120 !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #1A73E8, #0d47a1) !important;
    border-radius: 100px !important;
}
.stProgress > div {
    background: #E5E7EB !important;
    border-radius: 100px !important;
    height: 6px !important;
}

/* ── Source tags ── */
.source-tag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    margin: 0.2rem;
}
.tag-tavily    { background: #EFF6FF; color: #1A73E8; border: 1px solid #BFDBFE; }
.tag-wikipedia { background: #FFFBEB; color: #D97706; border: 1px solid #FDE68A; }
.tag-none      { background: #FEF2F2; color: #EF4444; border: 1px solid #FECACA; }

/* ── Divider ── */
hr { border-color: #E5E7EB !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #F9FAFB !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1.5px solid #E5E7EB !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #9CA3AF !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #1A73E8 !important;
    box-shadow: 0 1px 4px #00000010 !important;
}

/* ── Log box ── */
.log-box {
    background: #F9FAFB;
    border: 1.5px solid #E5E7EB;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #9CA3AF;
    line-height: 1.8;
    max-height: 200px;
    overflow-y: auto;
}
.log-box .log-ok   { color: #10b981; }
.log-box .log-warn { color: #D97706; }
.log-box .log-err  { color: #EF4444; }
.log-box .log-info { color: #1A73E8; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ LangGraph · Groq · Tavily</div>
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
        <div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:10px;
        padding:0.8rem 1.2rem;color:#EF4444;font-size:0.85rem;margin-top:1rem;">
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
        font-family:'DM Mono',monospace;font-size:0.75rem;
        color:#9CA3AF;letter-spacing:0.1em;">
        PIPELINE RUNNING — this takes 2–4 minutes…
        </div>""", unsafe_allow_html=True)

        result = run_research(topic)

    # Update pipeline cards to done
    pipeline_placeholder.markdown(pipeline_cards("pdf_done"), unsafe_allow_html=True)
    progress.progress(1.0)

    # ── Error ─────────────────────────────────────────────────
    if result.get("error") and result.get("current_step") == "validation_error":
        st.markdown(f"""
        <div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:10px;
        padding:1rem 1.2rem;color:#EF4444;margin:1rem 0;">
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
            <div style="background:#F9FAFB;border:1.5px solid #E5E7EB;border-radius:10px;
            padding:0.8rem 1rem;margin-bottom:0.6rem;display:flex;
            align-items:center;gap:0.8rem;">
                <span class="source-tag {css}">{icon} {src.upper()}</span>
                <span style="font-size:0.85rem;color:#4B5563;flex:1;">{r['question']}</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.7rem;
                color:#9CA3AF;">{hits} results</span>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        for i, q in enumerate(result.get("sub_questions", []), 1):
            st.markdown(f"""
            <div style="background:#F9FAFB;border:1.5px solid #E5E7EB;border-radius:10px;
            padding:0.9rem 1.2rem;margin-bottom:0.6rem;display:flex;gap:1rem;align-items:start;">
                <span style="font-family:'DM Mono',monospace;font-size:0.8rem;
                color:#1A73E8;min-width:1.5rem;">0{i}</span>
                <span style="color:#4B5563;font-size:0.9rem;">{q}</span>
            </div>
            """, unsafe_allow_html=True)