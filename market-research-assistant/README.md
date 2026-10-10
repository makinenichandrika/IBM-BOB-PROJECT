# Intelligent Market Research Assistant (IMRA)
**Powered by IBM Granite LLM | Agentic AI**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![IBM Granite](https://img.shields.io/badge/IBM-Granite_3.3-purple)](https://watsonx.ai)
[![Flask](https://img.shields.io/badge/Flask-3.x-green)](https://flask.palletsprojects.com)

---

## What is IMRA?

IMRA is an intelligent, web-based market research assistant that uses IBM Granite LLM to:
- 📈 Analyze market trends and growth forecasts
- ⚔️ Conduct balanced competitor analysis
- 👥 Build detailed customer personas
- 💡 Identify strategic business opportunities
- 📄 Generate professional executive reports
- 💬 Answer market research questions via chat

---

## Quick Start (Windows)

### Option 1 — One-Click Launch
```
Double-click run.bat
```
The launcher will:
1. Verify Python is installed
2. Create a virtual environment
3. Install all dependencies
4. Start the Flask server
5. Open your browser at `http://localhost:5000`

### Option 2 — Manual Setup
```bash
# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure credentials (optional — for live IBM Granite mode)
copy .env.example .env
# Edit .env with your IBM watsonx credentials

# 4. Run the application
python app.py
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your IBM watsonx.ai credentials:

```env
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

### Getting IBM watsonx Credentials
1. Sign up at [IBM watsonx.ai](https://dataplatform.cloud.ibm.com)
2. Create a project and note your **Project ID**
3. Generate an **API Key** from IBM Cloud → Manage → Access → API Keys
4. Paste both values into your `.env` file

> **Demo Mode:** If credentials are not set, IMRA runs in Demo Mode with rich sample responses — perfect for testing the UI and agent workflow.

---

## Application Structure

```
market-research-assistant/
├── app.py                   Flask application entry point
├── agent/
│   ├── orchestrator.py      ReAct-style agentic loop + IBM Granite client
│   ├── tools.py             5 specialized agent tools
│   ├── prompts.py           HAM-tone system prompts
│   └── guardrails.py        Ethics, privacy, and safety filters
├── static/
│   ├── index.html           Single-page application
│   ├── style.css            Professional UI styles
│   └── app.js               Frontend logic
├── PROJECT_PLAN.md          Agentic AI SDLC project plan
├── requirements.txt         Python dependencies
├── run.bat                  Windows one-click launcher
└── .env.example             Credentials template
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Server health + mode check |
| `POST` | `/api/research` | Full market research report |
| `POST` | `/api/query` | Single Q&A response |

### Example: Full Research Request
```bash
curl -X POST http://localhost:5000/api/research \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "EdTech",
    "product": "AI tutoring app",
    "target_audience": "K-12 students",
    "location": "India",
    "competitors": "BYJU'\''S, Unacademy"
  }'
```

### Example: Q&A Query
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a Blue Ocean Strategy?"}'
```

---

## Ethical AI Framework

| Principle | Implementation |
|-----------|---------------|
| **Data Privacy** | No PII stored; session-only context; `.env` for credentials |
| **Bias Reduction** | Multi-perspective prompts; diverse audience consideration |
| **Transparency** | Agent reasoning steps visible in UI |
| **Fairness** | Balanced competitor analysis enforced |
| **Content Safety** | Input/output guardrails active on every request |
| **HAM Tone** | Helpful, Authoritative, Measured tone via system prompt |

---

## Agent Tools

| Tool | Purpose |
|------|---------|
| `MarketTrendAnalyzer` | Market size, growth, drivers, 5-year outlook |
| `CompetitorAnalyzer` | Porter's Five Forces; balanced competitor review |
| `CustomerInsightEngine` | Customer personas, pain points, acquisition channels |
| `OpportunityFinder` | Blue ocean areas, go-to-market strategy, risk mitigation |
| `ReportGenerator` | Synthesizes all analyses into executive report |

---

## Requirements

- Python 3.10+
- Windows 10/11 (for `run.bat`; cross-platform otherwise)
- IBM watsonx.ai account (optional — runs in Demo Mode without it)

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| `Python not found` | Install Python 3.10+ and check "Add to PATH" |
| `pip install fails` | Run `pip install -r requirements.txt` manually |
| Server starts but browser won't open | Navigate to `http://localhost:5000` manually |
| Port 5000 in use | Set `FLASK_PORT=5001` in `.env` |
| IBM Granite errors | Verify `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` in `.env` |

Logs are written to `logs/app.log` for debugging.

---

*IMRA v1.0 | Agentic AI SDLC | IBM Granite 3.3*
