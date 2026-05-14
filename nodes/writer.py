# ============================================================
# nodes/writer.py  —  Node 4
#
# Two-pass writing strategy:
#   Pass 1 → write full structure with all sections
#   Pass 2 → expand each section for depth and detail
#
# This forces mistral to produce 4-5 page reports
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

from langchain_core.prompts import PromptTemplate

from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY
log  = get_logger(__name__)
_llm = ChatGroq(model=MODEL, groq_api_key=GROQ_API_KEY, temperature=0) # type: ignore

REQUIRED_SECTIONS = [
    "Executive Summary",
    "Introduction",
    "Key Findings",
    "Conclusion",
]

MIN_REPORT_CHARS = 4000

# ── Pass 1 — Write full structure ────────────────────────────
_WRITE_PROMPT = PromptTemplate.from_template("""
You are an expert research writer. Write a detailed research report using the summaries below.

Topic             : {topic}
Questions covered : {questions}
Research summaries: {summaries}

Write using this exact Markdown structure:

# Research Report: {topic}

## Executive Summary
Write 4 sentences summarizing the most important findings.

## Introduction
Write 2 paragraphs explaining background and why this topic matters.

## Key Findings

### Finding 1: [title from first summary]
Write 5 sentences about this finding using the first summary.

### Finding 2: [title from second summary]
Write 5 sentences about this finding using the second summary.

### Finding 3: [title from third summary]
Write 5 sentences about this finding using the third summary.

### Finding 4: [title from fourth summary]
Write 5 sentences about this finding using the fourth summary.

### Finding 5: [title from fifth summary]
Write 5 sentences about this finding using the fifth summary.

## Analysis
Write 3 paragraphs analyzing patterns and implications across findings.

## Practical Applications
Write 2 paragraphs on how to apply these findings in practice.

## Future Outlook
Write 2 paragraphs on where this field is heading.

## Conclusion
Write 3 sentences with final takeaways.

## References
List all sources from the summaries.

RULES: Use only the research summaries. Be specific and factual. No placeholder text.
""")

# ── Pass 2 — Expand for depth ────────────────────────────────
_EXPAND_PROMPT = PromptTemplate.from_template("""
You are expanding a research report to make it more detailed and comprehensive.

Take the report below and expand EVERY section by adding more depth:
- Add more specific details and examples to each paragraph
- Expand each Key Finding to at least 8 sentences
- Add more analysis to the Analysis section
- Make Introduction and Practical Applications longer

Original report:
{report}

Return the complete expanded report keeping all the same Markdown headers.
Do NOT add new sections — only expand existing ones.
RULES: Only use information already in the report. Write in professional English.
""")

# ── Pass 3 — Repair missing sections ─────────────────────────
_REPAIR_PROMPT = PromptTemplate.from_template("""
The research report is missing these sections: {missing}
Add them based on the existing content.

Report:
{report}

Return the complete fixed report.
""")


@retry(attempts=3, delay=2.0)
def _write(topic: str, questions: str, summaries: str) -> str:
    result = (_WRITE_PROMPT | _llm).invoke({
        "topic": topic, "questions": questions, "summaries": summaries,
    })
    return str(result.content).strip()


@retry(attempts=2, delay=2.0)
def _expand(report: str) -> str:
    result = (_EXPAND_PROMPT | _llm).invoke({"report": report})
    return str(result.content).strip()


@retry(attempts=2, delay=2.0)
def _repair(report: str, missing: list) -> str:
    result = (_REPAIR_PROMPT | _llm).invoke({
        "report": report, "missing": ", ".join(missing),
    })
    return str(result.content).strip()


def _quality_check(report: str) -> list:
    return [s for s in REQUIRED_SECTIONS if s.lower() not in report.lower()]


def writer_node(state: ResearchState) -> dict:
    topic     = state["topic"]
    summaries = state["summaries"]
    questions = state["sub_questions"]
    log.info(f"WRITER START | topic='{topic}'")

    questions_str = "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions))
    summaries_str = "\n\n".join(summaries)

    try:
        # Pass 1 — write structure
        log.info("WRITER PASS 1 | writing structure...")
        report = _write(topic, questions_str, summaries_str)
        log.info(f"WRITER PASS 1 | {len(report):,} chars")

        # Pass 2 — expand for depth
        log.info("WRITER PASS 2 | expanding for depth...")
        report = _expand(report)
        log.info(f"WRITER PASS 2 | {len(report):,} chars")

        # Quality gate
        missing = _quality_check(report)
        if missing:
            log.warning(f"QUALITY GATE  | missing: {missing} — repairing...")
            report = _repair(report, missing)
            log.info(f"QUALITY GATE  | repaired — {len(report):,} chars")
        else:
            log.info("QUALITY GATE  | all sections present")

        if len(report) < MIN_REPORT_CHARS:
            log.warning(f"WRITER WARN   | {len(report)} chars below {MIN_REPORT_CHARS} minimum")

        log.info(f"WRITER DONE   | {len(report):,} chars")
        return {"report": report, "current_step": "writer_done"}

    except Exception as exc:
        log.error(f"WRITER FAILED | {exc}")
        return {
            "report":       f"Report generation failed: {exc}",
            "error":        str(exc),
            "current_step": "writer_error",
        }