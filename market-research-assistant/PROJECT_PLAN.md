# Intelligent Market Research Assistant — Project Plan
**Powered by IBM Granite LLM | Agentic AI SDLC**

---

## 1. Project Overview

| Field | Details |
|-------|---------|
| **Project Name** | Intelligent Market Research Assistant (IMRA) |
| **Model** | IBM Granite 3.3 via IBM watsonx.ai |
| **Stack** | Python (Flask), HTML/CSS/JavaScript, IBM watsonx SDK |
| **Platform** | Windows (web-based, localhost) |
| **Version** | 1.0.0 |
| **Author** | Chandrika |
| **Date** | 2025 |

---

## 2. Agentic AI SDLC Phases

### Phase 1 — Requirements & Planning
- Define agent goals: collect inputs, analyze markets, generate reports
- Identify stakeholders: business analysts, entrepreneurs, product managers
- Define KPIs: report quality, response time < 30s, accuracy of insights
- Ethical constraints: data privacy, bias reduction, transparent reasoning
- Guardrails: no PII storage, content moderation, source attribution

### Phase 2 — Architecture Design
- **Agent Architecture:** ReAct-style (Reason + Act) single-agent loop
- **Tools/Skills:** MarketTrendAnalyzer, CompetitorAnalyzer, CustomerInsightEngine, OpportunityFinder, ReportGenerator
- **LLM:** IBM Granite 3.3-8b-instruct via watsonx.ai
- **Memory:** Session-based context (no persistent PII storage)
- **UI:** Single-page application (SPA) with chat + form interface

```
User → Web UI → Flask API → Agentic Orchestrator → IBM Granite LLM
                                    ↓
                   [Tool 1] MarketTrendAnalyzer
                   [Tool 2] CompetitorAnalyzer
                   [Tool 3] CustomerInsightEngine
                   [Tool 4] OpportunityFinder
                   [Tool 5] ReportGenerator
                                    ↓
                          Structured Report + Insights
```

### Phase 3 — Environment Setup
- Python 3.10+ virtual environment
- Flask 3.x web framework
- ibm-watsonx-ai SDK
- Dependencies: flask, flask-cors, ibm-watsonx-ai, python-dotenv, markdown2

### Phase 4 — Development
- **Backend:** Flask REST API (`/api/research`, `/api/query`, `/api/health`)
- **Agent:** Multi-tool orchestration with IBM Granite
- **Frontend:** Responsive SPA with form inputs and report display
- **Guardrails:** Input sanitization, output validation, ethics layer

### Phase 5 — Ethics & Guardrails Implementation
- **Data Privacy:** No user data stored beyond session; .env for credentials
- **Bias Reduction:** Balanced prompts, multi-perspective analysis
- **Transparency:** Agent reasoning steps shown to user
- **Content Safety:** Blocked topics list, output moderation
- **HAM Tone:** Helpful, professional, non-alarmist language enforced via system prompt

### Phase 6 — Testing & Validation
- Unit tests for each agent tool
- Integration tests for Flask API endpoints
- UI/UX walkthrough testing
- Ethics compliance review

### Phase 7 — Deployment
- Windows local deployment via `.bat` launcher
- Environment variable configuration via `.env`
- Browser auto-launch on startup

### Phase 8 — Maintenance & Monitoring
- Logging to `logs/app.log`
- Session tracking (anonymous)
- Model version pinning

---

## 3. Project Directory Structure

```
market-research-assistant/
├── PROJECT_PLAN.md          ← This file
├── README.md                ← Setup and usage guide
├── requirements.txt         ← Python dependencies
├── run.bat                  ← Windows launcher
├── .env.example             ← Environment variable template
├── app.py                   ← Flask application entry point
├── agent/
│   ├── __init__.py
│   ├── orchestrator.py      ← Agentic orchestration loop
│   ├── tools.py             ← Agent tools/skills
│   ├── prompts.py           ← System prompts & templates
│   └── guardrails.py        ← Ethics, bias, safety filters
├── static/
│   ├── index.html           ← Main SPA
│   ├── style.css            ← Styling
│   └── app.js               ← Frontend logic
└── logs/
    └── .gitkeep
```

---

## 4. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/research` | Full market research report generation |
| POST | `/api/query` | Single market research Q&A |
| GET | `/api/health` | Health check |

### Request — `/api/research`
```json
{
  "industry": "EdTech",
  "product": "AI tutoring app",
  "target_audience": "K-12 students",
  "location": "India",
  "competitors": "BYJU'S, Unacademy, Khan Academy"
}
```

### Response
```json
{
  "status": "success",
  "report": { ... },
  "reasoning_steps": [ ... ],
  "ethics_check": { "passed": true }
}
```

---

## 5. Ethical AI Framework

| Principle | Implementation |
|-----------|---------------|
| **Privacy** | No PII collected or stored; session-only context |
| **Bias Reduction** | Prompts require multi-demographic perspectives |
| **Transparency** | Agent reasoning steps exposed in UI |
| **Fairness** | Competitor analysis is balanced, not disparaging |
| **Safety** | Blocked keywords list; output content moderation |
| **Accountability** | All agent decisions logged with timestamps |

---

## 6. Timeline

| Week | Milestone |
|------|-----------|
| Week 1 | Planning, architecture, environment setup |
| Week 2 | Backend API + Agent core development |
| Week 3 | Frontend UI + Guardrails integration |
| Week 4 | Testing, documentation, deployment |

---

## 7. Risk Register

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| IBM watsonx API quota exceeded | Medium | Rate limiting + caching |
| LLM hallucination in reports | Medium | Structured prompts + output validation |
| User data privacy breach | Low | No data persistence; HTTPS recommended |
| Biased market analysis | Medium | Prompt engineering + diverse perspectives |

---

## 8. Success Criteria

- [x] Agent collects all 5 user inputs
- [x] Generates structured market report with ≥5 sections
- [x] Ethics guardrails active on every request
- [x] Response delivered within 60 seconds
- [x] UI is responsive and professional
- [x] .bat launcher works on Windows without manual setup
- [x] README documents all setup steps

---

*Document version 1.0 | IBM Granite Agentic AI SDLC*
