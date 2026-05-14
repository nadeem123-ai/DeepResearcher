import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

# ── LLM ─────────────────────────────────────────────────────
MODEL           = os.getenv("MODEL", "llama-3.3-70b-versatile")

# ── API keys ─────────────────────────────────────────────────
GROQ_API_KEY    = os.getenv("GROQ_API_KEY", "")
TAVILY_API_KEY  = os.getenv("TAVILY_API_KEY", "")

# ── Research ─────────────────────────────────────────────────
MAX_SEARCHES    = int(os.getenv("MAX_SEARCHES", "5"))

# ── Output ───────────────────────────────────────────────────
REPORT_OUTPUT   = Path(os.getenv("REPORT_OUTPUT", str(ROOT_DIR / "output")))
try:
    REPORT_OUTPUT.mkdir(parents=True, exist_ok=True)
except Exception as exc:
    print(f"⚠️  Config: could not create REPORT_OUTPUT directory {REPORT_OUTPUT!r}: {exc}")

def validate() -> None:
    issues = []
    if not GROQ_API_KEY:
        issues.append("GROQ_API_KEY is missing in .env")
    if not TAVILY_API_KEY:
        issues.append("TAVILY_API_KEY is missing in .env")
    for msg in issues:
        print(f"⚠️  Config: {msg}")

validate()