# ============================================================
# nodes/planner.py  —  Node 1
#
# Robustness features:
#   ✅ Retry logic    — LLM call retried 3x on failure
#   ✅ Logging        — every step logged to run.log
#   ✅ Format fix     — always returns exactly 5 questions
#   ✅ Graceful fail  — falls back to topic as single question
# ============================================================

import re
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

log  = get_logger(__name__)
_llm = ChatOllama(model=MODEL, temperature=0)

_PROMPT = PromptTemplate.from_template("""
You are a research planner. Decompose the topic into exactly 5 specific,
searchable research questions covering different angles.

Topic: {topic}

Output ONLY the 5 questions, numbered 1–5, one per line.
No preamble, no blank lines between questions.
""")


@retry(attempts=3, delay=2.0)
def _call_llm(topic: str) -> str:
    result = (_PROMPT | _llm).invoke({"topic": topic})
    content = result.content if isinstance(result.content, str) else "".join(str(c) for c in result.content)
    return content.strip()


def _parse_questions(raw: str, topic: str) -> list[str]:
    lines     = [l.strip() for l in raw.splitlines() if l.strip()]
    questions = [re.sub(r"^\d+[\.\)]\s*", "", l) for l in lines]
    questions = [q for q in questions if len(q) > 10][:5]

    # Pad to 5 if LLM returned fewer
    while len(questions) < 5:
        questions.append(f"Latest developments in {topic}")

    return questions


def planner_node(state: ResearchState) -> dict:
    topic = state["topic"]
    log.info(f"PLANNER START | topic='{topic}'")

    try:
        raw       = _call_llm(topic)
        questions = _parse_questions(raw, topic)

        for i, q in enumerate(questions, 1):
            log.debug(f"  Q{i}: {q}")

        log.info(f"PLANNER DONE  | {len(questions)} questions generated")
        return {"sub_questions": questions, "current_step": "planner_done"}

    except Exception as exc:
        log.error(f"PLANNER FAILED | {exc}")
        return {
            "sub_questions": [topic],
            "error":         str(exc),
            "current_step":  "planner_error",
        }