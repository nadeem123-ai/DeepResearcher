# ============================================================
# nodes/summarizer.py  —  Node 3
#
# Robustness features:
#   ✅ Retry logic        — LLM call retried 3x
#   ✅ Graceful skip      — empty results get placeholder text
#   ✅ Context truncation — long results trimmed before LLM call
#   ✅ Logging            — every summary attempt logged
# ============================================================

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings  import MODEL
from graph.state      import ResearchState
from utils.logger     import get_logger
from utils.retry      import retry

from langchain_ollama       import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY
log  = get_logger(__name__)
_llm = ChatGroq(model=MODEL, groq_api_key=GROQ_API_KEY, temperature=0) # type: ignore

_PROMPT = PromptTemplate.from_template("""
You are a research summarizer. Write a factual prose paragraph (4–6 sentences)
summarizing the search results for the given question.

Topic    : {topic}
Question : {question}
Results  : {results}

Rules:
- Facts only, no opinions
- Prose only, no bullet points
- Stay focused on the question

Summary:
""")

MAX_RESULT_CHARS = 1500  # prevent context overflow


def _format_results(hits: list) -> str:
    parts = []
    for h in hits:
        title   = h.get("title", "")
        content = h.get("content", "")[:500]
        url     = h.get("url", "")
        parts.append(f"Title: {title}\nContent: {content}\nURL: {url}")
    combined = "\n\n".join(parts)
    # Truncate if too long for model context
    return combined[:MAX_RESULT_CHARS]


@retry(attempts=3, delay=2.0)
def _call_llm(topic: str, question: str, results_text: str) -> str:
    result = (_PROMPT | _llm).invoke({
        "topic":    topic,
        "question": question,
        "results":  results_text,
    })
    content = result.content
    if isinstance(content, list):
        content = content[0] if content else ""
    elif isinstance(content, dict):
        content = str(content)
    return str(content).strip()


def summarizer_node(state: ResearchState) -> dict:
    search_results = state["search_results"]
    topic          = state["topic"]
    log.info(f"SUMMARIZER START | {len(search_results)} batches")

    summaries = []

    for i, item in enumerate(search_results, 1):
        question = item["question"]
        hits     = item.get("results", [])
        source   = item.get("source", "unknown")
        log.info(f"  [{i}/{len(search_results)}] Summarizing (source={source})")

        if not hits:
            log.warning(f"  [{i}] No results — using placeholder")
            summaries.append(
                f"### {question}\n\n"
                f"No search results were available for this question."
            )
            continue

        try:
            summary = _call_llm(topic, question, _format_results(hits))
            summaries.append(f"### {question}\n\n{summary}")
            log.info(f"  [{i}] ✅ Summary ready ({len(summary)} chars)")

        except Exception as exc:
            log.error(f"  [{i}] ❌ Summarization failed: {exc}")
            # Graceful degradation — use raw snippet instead
            raw = hits[0].get("content", "No content available.")[:400]
            summaries.append(f"### {question}\n\n{raw}")

    log.info(f"SUMMARIZER DONE  | {len(summaries)} summaries")
    return {"summaries": summaries, "current_step": "summarizer_done"}