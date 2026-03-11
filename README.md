# DeepResearcher

I built this to understand pure LangGraph — no AgentExecutor, no ReAct loops — just a clean 5-node pipeline that autonomously researches any topic and generates a professional PDF report.

Part of my Deep Series where I build every AI system from the ground up before using any framework.

---

## 📌 What Is This Project?

After building 6 projects with LangChain and agents, I wanted to understand LangGraph properly. Not the agent wrapper — the actual StateGraph with nodes, edges, and shared state.

- First I studied how LangGraph StateGraph differs from AgentExecutor
- Then I built 5 nodes — each doing one job cleanly
- Then I added production features — retry, fallback, validation, quality gate, PDF export

---

## 🧠 What Is Pure LangGraph?

AgentExecutor (old way):
```
LLM decides → call tool → observe → repeat
Problem: unpredictable, hard to control, can loop forever
```

LangGraph StateGraph (new way):
```
You define exactly:
  - What nodes exist
  - What order they run
  - What data flows between them
Result: predictable, debuggable, production-ready
```

How state flows:
```
START
  │
  ▼
📋 Planner       receives: topic
                 returns:  sub_questions
  │
  ▼
🔍 Researcher    receives: sub_questions
                 returns:  search_results
  │
  ▼
📝 Summarizer    receives: search_results
                 returns:  summaries
  │
  ▼
✍️  Writer        receives: summaries
                 returns:  report
  │
  ▼
📄 PDF Generator receives: report
                 returns:  pdf_path
  │
  ▼
END
```

Every node reads from and writes to the same `ResearchState` TypedDict — like a shared backpack that travels through the pipeline.

---

## 📁 Project Structure

```
DeepResearcher/
├── config/
│   └── settings.py           ← all config from .env
├── graph/
│   ├── state.py              ← ResearchState TypedDict
│   └── research_graph.py     ← pure LangGraph StateGraph
├── nodes/
│   ├── planner.py            ← Node 1: 5 sub-questions
│   ├── researcher.py         ← Node 2: Tavily + Wikipedia
│   ├── summarizer.py         ← Node 3: condense results
│   ├── writer.py             ← Node 4: two-pass writing
│   └── pdf_generator.py      ← Node 5: professional PDF
├── utils/
│   ├── logger.py             ← logs every run to run.log
│   ├── retry.py              ← @retry decorator
│   └── validator.py          ← input validation
├── ui/
│   └── app.py                ← Streamlit dark-theme UI
├── output/                   ← PDFs saved here
├── logs/                     ← run.log saved here
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔧 What I Built

### 5 LangGraph Nodes

| Node | Input | Output | Key Feature |
|------|-------|--------|-------------|
| Planner | topic | 5 sub-questions | Retry 3x, always returns exactly 5 |
| Researcher | sub-questions | search results | Tavily first, Wikipedia fallback |
| Summarizer | search results | summaries | Graceful skip if no results |
| Writer | summaries | full report | Two-pass: write then expand |
| PDF Generator | report | pdf file | Cover + table + chart + callouts |

### PDF Features
```
Page 1 → Cover page      (dark branded, topic, date)
Page 2 → Summary table   (all 5 findings in a table)
         Bar chart        (research depth per finding)
Page 3+ → Full report    (section bands, callouts, typography)
```

### Robustness Features
```
Retry logic        → every node retries 3x automatically
Wikipedia fallback → if Tavily fails, uses Wikipedia
Input validation   → rejects empty or bad topics early
Quality gate       → checks all report sections present
Auto-repair        → fixes missing sections automatically
Run logging        → every run saved to logs/run.log
Report versioning  → timestamped PDFs, never overwrites
```

---

## 📊 Test Results

| Test | Result | Notes |
|------|--------|-------|
| Pipeline runs end to end | ✅ Works | 3-4 minutes total |
| Planner generates 5 questions | ✅ Works | Always exactly 5 |
| Tavily search | ✅ Works | 5/5 searches successful |
| Wikipedia fallback | ✅ Works | Tested with broken API key |
| Summarizer condenses | ✅ Works | 5 summaries generated |
| Writer two-pass | ✅ Works | 6000+ chars report |
| Quality gate | ✅ Works | All sections present |
| PDF cover page | ✅ Works | Dark branded design |
| PDF summary table | ✅ Works | All 5 findings shown |
| PDF bar chart | ✅ Works | Real depth values |
| PDF callout boxes | ✅ Works | Key insights highlighted |
| Long URL crash | ✅ Fixed | _break_long_words() fix |
| Special chars crash | ✅ Fixed | Latin-1 encoding fix |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Ollama installed and running
- mistral model: `ollama pull mistral`
- Tavily API key from app.tavily.com

### Installation
```bash
git clone https://github.com/nadeem123-ai/DeepResearcher.git
cd DeepResearcher
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### Setup .env
```env
MODEL=mistral
TAVILY_API_KEY=your_tavily_key_here
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

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Core language |
| Ollama + Mistral | Latest | Local LLM |
| LangGraph | 1.0.10 | Pipeline orchestration |
| LangChain Core | 0.3.59 | LLM abstractions |
| Tavily | Latest | Web search |
| Wikipedia | Latest | Fallback search |
| fpdf2 | 2.8.3 | PDF generation |
| matplotlib | 3.10.1 | Bar chart in PDF |
| Streamlit | 1.43.2 | Web UI |

---

## 💡 Key Lessons Learned

1. **LangGraph gives you control that AgentExecutor never had**
   → You define every step. Nothing runs that you did not put in the graph.

2. **State TypedDict is the backbone of the whole system**
   → Design it carefully first — every node depends on it.

3. **Two-pass writing produces much better reports**
   → Pass 1 = structure. Pass 2 = depth. One pass is never enough for small LLMs.

4. **PDF generation has hidden edge cases**
   → Long URLs crash fpdf2. Smart quotes crash latin-1 encoding. Test with real data.

5. **Retry logic is not optional in production**
   → LLM calls fail. API calls fail. Without retry, your pipeline fails silently.

6. **Wikipedia is a surprisingly good fallback**
   → When Tavily fails, Wikipedia covers most topics well enough to continue.

7. **Logging is what makes debugging possible**
   → Without logs/run.log, you cannot see which node failed and why.

---

## 🗺️ My Deep Series

| Project | Description | Status |
|---------|-------------|--------|
| DeepRAG | RAG from scratch | ✅ Done |
| MemoryRAG | RAG with memory | ✅ Done |
| MemoryRAG-LlamaIndex | Multi-PDF RAG | ✅ Done |
| AdvancedRAG-LlamaIndex | Production RAG | ✅ Done |
| DeepAgent | AI Agent with tools | ✅ Done |
| DeepAgenticRAG | RAG + Agent + graders | ✅ Done |
| **DeepResearcher** | **Pure LangGraph pipeline** | ✅ Done |

---

## 👤 Author

**Muhammad Nadeem**

- GitHub: [@nadeem123-ai](https://github.com/nadeem123-ai)
- LinkedIn: [muhammad-nadeem](https://www.linkedin.com/in/muhammad-nadeem-a6912325b)

⭐ If this helped you understand LangGraph, give it a star!