# ============================================================
# graph/research_graph.py
# Pure LangGraph StateGraph — production grade.
#
# Robustness added:
#   ✅ Input validation before graph runs
#   ✅ Run logging — start/end logged to logs/run.log
#   ✅ Clean error surface — caller gets structured result
# ============================================================

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from graph.state          import ResearchState
from nodes.planner        import planner_node
from nodes.researcher     import researcher_node
from nodes.summarizer     import summarizer_node
from nodes.writer         import writer_node
from nodes.pdf_generator  import pdf_generator_node
from utils.logger         import get_logger, log_run_start, log_run_end
from utils.validator      import validate_topic, InvalidTopicError

from langgraph.graph import StateGraph, START, END

log = get_logger(__name__)


def build_graph():
    g = StateGraph(ResearchState)

    g.add_node("planner",       planner_node)
    g.add_node("researcher",    researcher_node)
    g.add_node("summarizer",    summarizer_node)
    g.add_node("writer",        writer_node)
    g.add_node("pdf_generator", pdf_generator_node)

    g.add_edge(START,           "planner")
    g.add_edge("planner",       "researcher")
    g.add_edge("researcher",    "summarizer")
    g.add_edge("summarizer",    "writer")
    g.add_edge("writer",        "pdf_generator")
    g.add_edge("pdf_generator", END)

    return g.compile()


def run_research(topic: str) -> ResearchState:
    """
    Validates input, runs the 5-node pipeline, logs result.

    Args:
        topic: Raw topic string from user.

    Returns:
        Final ResearchState with report and pdf_path.
    """
    # ── Input validation ─────────────────────────────────────
    try:
        topic = validate_topic(topic)
    except InvalidTopicError as exc:
        log.error(f"VALIDATION FAILED | {exc}")
        return {
            "topic":          topic,
            "sub_questions":  [],
            "search_results": [],
            "summaries":      [],
            "report":         "",
            "pdf_path":       "",
            "current_step":   "validation_error",
            "error":          str(exc),
        }

    log_run_start(topic)

    initial: ResearchState = {
        "topic":          topic,
        "sub_questions":  [],
        "search_results": [],
        "summaries":      [],
        "report":         "",
        "pdf_path":       "",
        "current_step":   "start",
        "error":          None,
    }

    try:
        app   = build_graph()
        final = app.invoke(initial)
        log_run_end(topic, final.get("pdf_path", ""), final.get("error", ""))
        return final  # type: ignore[return-value]

    except Exception as exc:
        log.error(f"PIPELINE CRASHED | {exc}")
        log_run_end(topic, "", str(exc))
        initial["error"]        = str(exc)
        initial["current_step"] = "pipeline_error"
        return initial


# ── CLI ──────────────────────────────────────────────────────
if __name__ == "__main__":
    topic = input("Research topic: ").strip()
    if topic:
        result = run_research(topic)
        if result["pdf_path"]:
            print(f"\n✅ PDF saved: {result['pdf_path']}")
        if result.get("error"):
            print(f"\n⚠️  Error: {result['error']}")