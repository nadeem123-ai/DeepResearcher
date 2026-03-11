# ============================================================
# graph/state.py
# The shared state that travels through every LangGraph node.
#
# Think of it as a baton in a relay race —
# each node receives it, adds its output, passes it forward.
#
# Node outputs:
#   planner       → sub_questions
#   researcher    → search_results
#   summarizer    → summaries
#   writer        → report
#   pdf_generator → pdf_path
# ============================================================

from typing import List, Optional
from typing_extensions import TypedDict


class ResearchState(TypedDict):
    # ── User input ───────────────────────────────────────────
    topic:          str

    # ── Node outputs ─────────────────────────────────────────
    sub_questions:  List[str]
    search_results: List[dict]
    summaries:      List[str]
    report:         str
    pdf_path:       str

    # ── Metadata ─────────────────────────────────────────────
    current_step:   str
    error:          Optional[str]