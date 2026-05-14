# 🔬 DeepResearcher

<p align="center">
  <img src="https://img.shields.io/badge/LangGraph-1.0.10-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange?style=for-the-badge&logo=lightning&logoColor=white" />
  <img src="https://img.shields.io/badge/Tavily-Search-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-1.43.2-red?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" />
</p>

<p align="center">
  <b>Autonomous AI research pipeline built with pure LangGraph — no AgentExecutor, no ReAct loops.</b><br/>
  Enter any topic → get a professional PDF research report in minutes. 100% free to run.
</p>

## 📌 What Is This?

After building 6 projects with LangChain agents, I wanted to understand **LangGraph properly** — not the agent wrapper, but the actual `StateGraph` with nodes, edges, and shared state.

So I built a **5-node research pipeline** from scratch:

- Studied how `StateGraph` differs from `AgentExecutor`
- Built each node to do exactly one job
- Added production features: retry logic, Wikipedia fallback, quality gate, PDF export

**Result:** A fully autonomous research assistant that takes any topic and produces a structured PDF report — powered entirely by free APIs.

---

## ⚡ Quick Demo

```
Topic: "Impact of AI on software engineering jobs in 2025"

Pipeline:
  📋 Planner      → generates 5 targeted research questions
  🔍 Researcher   → searches Tavily (Wikipedia fallback)
  📝 Summarizer   → condenses all findings
  ✍️  Writer       → two-pass report generation
  📄 PDF          → cover page + table + chart + full report

Output: professional_report_20260514.pdf  ✅
```

---

## 🧠 Pure LangGraph vs AgentExecutor

```
AgentExecutor (old way):
  LLM decides → call tool → observe → repeat
  ❌ Unpredictable   ❌ Hard to debug   ❌ Can loop forever

LangGraph StateGraph (new way):
  You define exactly what nodes exist, what order they run,
  and what data flows between them.
  ✅ Predictable   ✅ Debuggable   ✅ Production-ready
```

**State flow:**
```
START → 📋 Planner → 🔍 Researcher → 📝 Summarizer → ✍️ Writer → 📄 PDF → END
```

Every node reads from and writes to the same `ResearchState` TypedDict — a shared backpack traveling through the pipeline.

---

## 🔧 5 LangGraph Nodes

| Node | Input | Output | Key Feature |
|------|-------|--------|-------------|
| 📋 Planner | topic | 5 sub-questions | Retry 3x, always returns exactly 5 |
| 🔍 Researcher | sub-questions | search results | Tavily first, Wikipedia fallback |
| 📝 Summarizer | search results | summaries | Graceful skip if no results |
| ✍️ Writer | summaries | full report | Two-pass: structure then depth |
| 📄 PDF Generator | report | pdf file | Cover + table + chart + callouts |

### Production Features
```
✅ Retry logic        — every node retries 3x automatically
✅ Wikipedia fallback — if Tavily fails, Wikipedia takes over
✅ Input validation   — rejects bad topics early
✅ Quality gate       — checks all report sections present
✅ Auto-repair        — fixes missing sections automatically
✅ Run logging        — every run saved to logs/run.log
✅ Report versioning  — timestamped PDFs, never overwrites
```

---

## 📄 PDF Output

```
Page 1  →  Cover page       dark branded, topic, date
Page 2  →  Summary table    all 5 findings in a table
           Bar chart         research depth per finding
Page 3+ →  Full report      section bands, callouts, typography
```

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Core language |
| **Groq + LLaMA 3.3 70B** | Latest | **Free cloud LLM** |
| LangGraph | 1.0.10 | Pipeline orchestration |
| LangChain Core | 0.3.59 | LLM abstractions |
| LangChain Groq | 0.2.4 | Groq integration |
| Tavily | Latest | Web search |
| Wikipedia | Latest | Fallback search |
| fpdf2 | 2.8.3 | PDF generation |
| matplotlib | 3.10.1 | Bar chart in PDF |
| Streamlit | 1.43.2 | Web UI |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Free [Groq API key](https://console.groq.com) — takes 30 seconds
- Free [Tavily API key](https://app.tavily.com)

### Installation

```bash
git clone https://github.com/nadeem123-ai/DeepResearcher.git
cd DeepResearcher
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### Setup `.env`

```env
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
MODEL=llama-3.3-70b-versatile
MAX_SEARCHES=5
REPORT_OUTPUT=./output
```

### Run

```bash
# Streamlit UI
streamlit run ui/app.py

# CLI
python graph/research_graph.py
```

---

## 📊 Test Results

| Test | Result | Notes |
|------|--------|-------|
| Pipeline end to end | ✅ | 1-2 min with Groq |
| Planner — 5 questions | ✅ | Always exactly 5 |
| Tavily search | ✅ | 5/5 successful |
| Wikipedia fallback | ✅ | Tested with broken key |
| Summarizer | ✅ | 5 summaries generated |
| Writer two-pass | ✅ | 6000+ chars report |
| Quality gate | ✅ | All sections present |
| PDF cover page | ✅ | Dark branded design |
| PDF summary table | ✅ | All 5 findings |
| PDF bar chart | ✅ | Real depth values |
| Long URL crash | ✅ Fixed | `_break_long_words()` |
| Special chars crash | ✅ Fixed | Latin-1 encoding fix |

---

## 💡 Key Lessons Learned

1. **LangGraph gives you control AgentExecutor never had** — you define every step; nothing runs that you didn't put in the graph.
2. **State TypedDict is the backbone** — design it carefully first; every node depends on it.
3. **Two-pass writing produces far better reports** — pass 1 = structure, pass 2 = depth.
4. **PDF generation has hidden edge cases** — long URLs crash fpdf2; smart quotes crash latin-1. Test with real data.
5. **Retry logic is not optional in production** — LLM calls fail; without retry your pipeline fails silently.
6. **Wikipedia is a surprisingly good fallback** — covers most topics well when Tavily fails.
7. **Logging is what makes debugging possible** — without `run.log` you cannot see which node failed and why.

---

## 🗺️ Deep Series — My AI Portfolio

| # | Project | Description | Status |
|---|---------|-------------|--------|
| 1 | DeepRAG | RAG from scratch | ✅ Done |
| 2 | MemoryRAG | RAG with memory | ✅ Done |
| 3 | MemoryRAG-LlamaIndex | Multi-PDF RAG | ✅ Done |
| 4 | AdvancedRAG-LlamaIndex | Production RAG | ✅ Done |
| 5 | DeepAgent | AI Agent with tools | ✅ Done |
| 6 | DeepAgenticRAG | RAG + Agent + graders | ✅ Done |
| 7 | **DeepResearcher** | **Pure LangGraph pipeline** | ✅ **Live** |

---

## 👤 Author

**Muhammad Nadeem — AI · ML · Agentic Engineer**

---

⭐ **If this helped you understand LangGraph, give it a star — it means a lot!**