# ============================================================
# nodes/pdf_generator.py  —  Node 5
#
# Professional PDF features:
#   ✅ Cover page        — title, topic, date, branding
#   ✅ Summary table     — key findings overview table
#   ✅ Bar chart         — actual finding body lengths
#   ✅ Callout boxes     — highlighted insight boxes
#   ✅ Section dividers  — colored header bands
#   ✅ Safe rendering    — handles special chars and long URLs
#   ✅ Versioning        — timestamped filenames
#   ✅ Retry logic       — retries on transient errors
# ============================================================

import re
import sys
import tempfile
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings  import REPORT_OUTPUT
from graph.state      import ResearchState
from utils.logger     import get_logger
from utils.retry      import retry

from fpdf import FPDF
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

log = get_logger(__name__)

# ── Brand colors ─────────────────────────────────────────────
C_DARK       = (15,  25,  40)
C_ACCENT     = (0,   140, 200)
C_LIGHT      = (240, 245, 252)
C_MID        = (80,  100, 130)
C_CALLOUT_BG = (232, 244, 252)
C_CALLOUT_BD = (0,   140, 200)

MAX_WORD = 55


# ── Text safety ───────────────────────────────────────────────
def _safe(text: str) -> str:
    replacements = {
        "\u2018": "'",  "\u2019": "'",
        "\u201c": '"',  "\u201d": '"',
        "\u2013": "-",  "\u2014": "--",
        "\u2026": "...","\u2022": "-",
        "\u00b7": "-",  "\u00a0": " ",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _break_long_words(text: str) -> str:
    words = text.split(" ")
    result = []
    for word in words:
        while len(word) > MAX_WORD:
            result.append(word[:MAX_WORD] + "-")
            word = word[MAX_WORD:]
        result.append(word)
    return " ".join(result)


def _clean(text: str) -> str:
    text = re.sub(r"\*{1,2}(.*?)\*{1,2}", r"\1", text)
    text = _break_long_words(text)
    return _safe(text)


# ── PDF class ─────────────────────────────────────────────────
class ReportPDF(FPDF):

    def __init__(self, topic: str):
        super().__init__()
        self.topic = topic
        self.set_margins(15, 20, 15)
        self.set_auto_page_break(auto=True, margin=22)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*C_MID)
        self.cell(0, 6, "DeepResearcher  -  AI Research Report", align="L")
        self.set_draw_color(220, 225, 235)
        self.line(15, self.get_y() + 7, 195, self.get_y() + 7)
        self.ln(11)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*C_MID)
        date = datetime.now().strftime("%d %B %Y")
        self.cell(0, 8, f"Generated {date}   -   Page {self.page_no() - 1}", align="C")

    def add_cover(self) -> None:
        self.add_page()
        self.set_fill_color(*C_DARK)
        self.rect(0, 0, 210, 297, "F")
        self.set_fill_color(*C_ACCENT)
        self.rect(0, 0, 210, 6, "F")

        self.set_y(55)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*C_ACCENT)
        self.cell(0, 8, "DEEPRESEARCHER", align="C")
        self.ln(4)
        self.set_draw_color(*C_ACCENT)
        self.set_line_width(0.3)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(12)

        self.set_font("Helvetica", "B", 20)
        self.set_text_color(240, 245, 255)
        self.multi_cell(0, 12, _clean(f"Research Report:\n{self.topic}"), align="C")
        self.ln(8)

        self.set_font("Helvetica", "", 10)
        self.set_text_color(*C_MID)
        self.cell(0, 6, "AI-Powered Research  -  LangGraph + Ollama + Tavily", align="C")
        self.ln(20)

        date_str = datetime.now().strftime("%B %d, %Y")
        x = 70
        self.set_fill_color(30, 50, 75)
        self.set_draw_color(*C_ACCENT)
        self.set_line_width(0.4)
        self.rect(x, self.get_y(), 70, 10, "FD")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*C_ACCENT)
        self.set_xy(x, self.get_y() + 2)
        self.cell(70, 6, _safe(date_str), align="C")

        self.set_fill_color(*C_ACCENT)
        self.rect(0, 291, 210, 6, "F")

    def section_band(self, title: str) -> None:
        self.ln(4)
        y = self.get_y()
        self.set_fill_color(*C_DARK)
        self.rect(0, y, 210, 12, "F")
        self.set_fill_color(*C_ACCENT)
        self.rect(0, y, 4, 12, "F")
        self.set_xy(10, y + 2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(240, 245, 255)
        self.cell(0, 8, _clean(title.upper()))
        self.ln(14)

    def callout(self, text: str) -> None:
        self.ln(3)
        y        = self.get_y()
        lines_n  = max(2, len(text) // 75 + 1)
        box_h    = lines_n * 6 + 10

        self.set_fill_color(*C_CALLOUT_BG)
        self.set_draw_color(*C_CALLOUT_BD)
        self.set_line_width(0.4)
        self.rect(15, y, 180, box_h, "FD")
        self.set_fill_color(*C_ACCENT)
        self.rect(15, y, 3, box_h, "F")

        self.set_xy(22, y + 4)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*C_DARK)
        self.multi_cell(171, 6, _clean(text))
        self.ln(4)

    def summary_table(self, findings: list) -> None:
        self.section_band("Key Findings at a Glance")
        col_w = [10, 80, 90]
        row_h = 8

        self.set_fill_color(*C_DARK)
        self.set_text_color(240, 245, 255)
        self.set_font("Helvetica", "B", 9)
        for w, h in zip(col_w, ["#", "Finding", "Summary"]):
            self.cell(w, row_h, h, border=1, fill=True, align="C")
        self.ln()

        for i, (title, summary) in enumerate(findings, 1):
            fill = C_ACCENT if i % 2 == 0 else C_LIGHT
            self.set_fill_color(*fill)
            self.set_text_color(*C_DARK)
            self.set_font("Helvetica", "B", 8)
            self.cell(col_w[0], row_h, str(i), border=1, fill=True, align="C")
            self.cell(col_w[1], row_h, _clean(title[:45]), border=1, fill=True)
            self.set_font("Helvetica", "", 8)
            self.cell(col_w[2], row_h, _clean(summary[:55]), border=1, fill=True)
            self.ln()
        self.ln(5)

    def bar_chart(self, findings: list) -> None:
        self.section_band("Research Depth by Finding")

        labels = [f"Finding {i+1}" for i in range(len(findings))]
        # FIX: use full body length not first sentence
        values = [f[2] for f in findings]

        fig, ax = plt.subplots(figsize=(7, 2.8))
        fig.patch.set_facecolor("#f0f5fc")
        ax.set_facecolor("#f0f5fc")

        colors = ["#008cc8", "#00aad4", "#00c4b4", "#10b981", "#0077aa"]
        bars = ax.barh(labels, values, color=colors, height=0.5,
                       edgecolor="white", linewidth=0.5)

        ax.set_xlabel("Characters", fontsize=8, color="#506480")
        ax.set_title("Research Content Depth per Finding", fontsize=9,
                     color="#0f1928", fontweight="bold")
        ax.tick_params(labelsize=7, colors="#506480")
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["left", "bottom"]:
            ax.spines[spine].set_color("#d0d8e8")

        for bar, val in zip(bars, values):
            ax.text(val + max(values) * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    str(val), va="center", fontsize=7, color="#506480")

        plt.tight_layout()
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        plt.savefig(tmp.name, dpi=140, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        plt.close(fig)
        self.image(tmp.name, x=20, w=170)
        self.ln(6)
        try:
            Path(tmp.name).unlink()
        except Exception:
            pass


# ── Parse findings — returns (title, summary, body_length) ───
def _extract_findings(report: str) -> list:
    findings = []
    pattern  = re.compile(r"###\s+(?:Finding\s+\d+[:\-]?\s*)?(.+?)$", re.MULTILINE)
    sections = list(pattern.finditer(report))

    for i, match in enumerate(sections[:5]):
        title = match.group(1).strip()
        start = match.end()
        end   = sections[i + 1].start() if i + 1 < len(sections) else len(report)
        body  = report[start:end].strip()

        # First sentence as summary
        first = re.split(r"(?<=[.!?])\s", body)[0][:120] if body else ""
        # Full body length for chart
        body_len = len(body)

        findings.append((title, first, body_len))

    while len(findings) < 5:
        findings.append((f"Finding {len(findings)+1}", "See full report.", 0))

    return findings[:5]


# ── Render body ───────────────────────────────────────────────
def _render_body(pdf: ReportPDF, report: str) -> None:
    para_count = 0

    for raw_line in report.splitlines():
        line = raw_line.strip()

        if not line:
            pdf.ln(3)
            continue

        if re.match(r"^# [^#]", line):
            pdf.set_font("Helvetica", "B", 17)
            pdf.set_text_color(*C_DARK)
            pdf.multi_cell(0, 10, _clean(line[2:].strip()))
            pdf.ln(3)

        elif re.match(r"^## [^#]", line):
            pdf.section_band(line[3:].strip())
            para_count = 0

        elif re.match(r"^### [^#]", line):
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(*C_ACCENT)
            pdf.multi_cell(0, 7, _clean(line[4:].strip()))
            pdf.ln(2)

        elif re.match(r"^[-*] ", line):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(*C_MID)
            pdf.multi_cell(0, 6, _clean("  -  " + line[2:].strip()))

        else:
            para_count += 1
            # Every 2nd paragraph → callout box
            if para_count % 2 == 0 and len(line) > 80:
                snippet = line[:280] + ("..." if len(line) > 280 else "")
                pdf.callout(snippet)
            else:
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(55, 65, 75)
                pdf.multi_cell(0, 6, _clean(line))


# ── Node ─────────────────────────────────────────────────────
def _unique_path(topic: str) -> Path:
    safe  = re.sub(r"[^\w\s-]", "", topic).strip().replace(" ", "_")[:50]
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return REPORT_OUTPUT / f"report_{safe}_{stamp}.pdf"


@retry(attempts=2, delay=1.0)
def _build_pdf(report: str, topic: str, path: Path) -> None:
    findings = _extract_findings(report)
    pdf      = ReportPDF(topic=topic)

    pdf.add_cover()

    pdf.add_page()
    pdf.summary_table(findings)
    pdf.bar_chart(findings)

    pdf.add_page()
    _render_body(pdf, report)

    pdf.output(str(path))


def pdf_generator_node(state: ResearchState) -> dict:
    report = state["report"]
    topic  = state["topic"]
    path   = _unique_path(topic)

    log.info(f"PDF START  | path={path.name}")

    try:
        _build_pdf(report, topic, path)
        size_kb = path.stat().st_size // 1024
        log.info(f"PDF DONE   | {path.name} ({size_kb} KB)")
        return {"pdf_path": str(path), "current_step": "pdf_done"}

    except Exception as exc:
        log.error(f"PDF FAILED | {exc}")
        return {"pdf_path": "", "error": str(exc), "current_step": "pdf_error"}