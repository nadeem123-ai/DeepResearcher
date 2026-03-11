# ============================================================
# nodes/researcher.py  —  Node 2
#
# Robustness features:
#   ✅ Retry logic          — Tavily retried 3x per question
#   ✅ Wikipedia fallback   — if Tavily fails, use Wikipedia
#   ✅ Graceful degradation — one failed search never crashes pipeline
#   ✅ Logging              — every search attempt logged
# ============================================================

import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings  import TAVILY_API_KEY, MAX_SEARCHES
from graph.state      import ResearchState
from utils.logger     import get_logger
from utils.retry      import retry

os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

from langchain_community.tools.tavily_search    import TavilySearchResults
from langchain_community.tools                  import WikipediaQueryRun
from langchain_community.utilities             import WikipediaAPIWrapper
import wikipedia

log      = get_logger(__name__)
_tavily  = TavilySearchResults(max_results=3)
_wiki    = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(wiki_client=wikipedia, top_k_results=1, doc_content_chars_max=800)
)


# ── Tavily search with retry ──────────────────────────────────
@retry(attempts=3, delay=3.0, exceptions=(Exception,))
def _tavily_search(query: str) -> list:
    return _tavily.invoke(query)


# ── Wikipedia fallback ────────────────────────────────────────
def _wiki_search(query: str) -> list:
    log.info(f"  FALLBACK → Wikipedia | query='{query[:60]}'")
    try:
        content = _wiki.invoke(query)
        return [{"title": "Wikipedia", "content": content, "url": "https://wikipedia.org"}]
    except Exception as exc:
        log.warning(f"  Wikipedia also failed: {exc}")
        return []


# ── Per-question search ───────────────────────────────────────
def _search_one(question: str, index: int, total: int) -> dict:
    log.info(f"  [{index}/{total}] Tavily → '{question[:70]}'")
    try:
        hits = _tavily_search(question)
        log.info(f"  [{index}/{total}] ✅ {len(hits)} results from Tavily")
        return {"question": question, "results": hits, "source": "tavily"}

    except Exception as tavily_exc:
        log.warning(f"  [{index}/{total}] Tavily failed after retries: {tavily_exc}")
        hits = _wiki_search(question)

        if hits:
            log.info(f"  [{index}/{total}] ✅ {len(hits)} results from Wikipedia")
            return {"question": question, "results": hits, "source": "wikipedia"}
        else:
            log.error(f"  [{index}/{total}] ❌ Both Tavily and Wikipedia failed")
            return {"question": question, "results": [], "source": "none", "error": str(tavily_exc)}


# ── Node ──────────────────────────────────────────────────────
def researcher_node(state: ResearchState) -> dict:
    questions = state["sub_questions"]
    log.info(f"RESEARCHER START | {len(questions)} questions")

    results = [
        _search_one(q, i, len(questions))
        for i, q in enumerate(questions[:MAX_SEARCHES], 1)
    ]

    success = sum(1 for r in results if r.get("results"))
    log.info(f"RESEARCHER DONE  | {success}/{len(results)} searches successful")

    return {"search_results": results, "current_step": "researcher_done"}