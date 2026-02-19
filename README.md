[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/P5MLsfQv)
# Agentic RAG Chatbot - Hackathon Challenge

## Overview
Build a chatbot (Web App or CLI) that demonstrates how you’d ship an AI-first product feature:
- **File-grounded Q&A (RAG)** with **citations**
- **Durable memory** written to markdown
- *(Optional)* **Safe compute** tool calling with Open-Meteo time series analysis

You may implement one feature or multiple. Partial implementations are acceptable.

---

## 1) Participant Info (Required)
- Full Name: TEJUS SANJAY SHARMA
- Email: tejus98sharma@gmail.com
- GitHub Username:tejus15

---
## 2) Video Walkthrough Link (Required)

---

## 3) Quick Start
Follow these exact steps to run the application locally.

**1. Clone and Enter Repository** <br/>
git clone https://github.com/Community-Dreams-Foundation/agentic-rag-chatbot-tejus15.git <br/>
cd agentic-rag-chatbot-tejus15

**2. Install Dependencies**<br/>
pip install -r requirements.txt

**3. Configure Environment** <br/>
Create a .env file in the root directory and add your OpenAI API Key:<br/>
OPENAI_API_KEY=sk-proj-xxxx...

**4. Run the App**<br/>
Launch the UI:<br/>
streamlit run app.py

**5. Run Sanity Check (For Judges)<br/>**
To verify the system works without opening the UI, run the automated test suite:<br/>

***Option A: Using Make (Recommended)<br/>***
make sanity

<br/>This will generate a success report at artifacts/sanity_output.json.

## FEATURES

### Feature A - File Upload + RAG (Core)
Users can:
- Upload files and add them to a RAG pipeline (parse → chunk → index)
- Ask questions later and receive answers grounded in uploaded content
- Provide **citations** pointing to source chunks/sections

**Minimum expectation:** working ingestion + retrieval + grounded response + citations.

Suggested test data: arXiv PDFs/HTML (open access).

Extra points:
- Hybrid retrieval (BM25 + embeddings), reranking, metadata filters
- Smart chunking (section-aware, semantic boundaries)
- Knowledge-graph flavored RAG

---

### Feature B - Persistent Memory (Core-ish)
Add a memory subsystem that writes selective, high-signal knowledge to:

- `USER_MEMORY.md`  
  Store user-specific facts worth remembering.  
  Example: “User is a Project Finance Analyst”, “Prefers weekly summaries on Mondays”.

- `COMPANY_MEMORY.md`  
  Store org-wide learnings useful to colleagues.  
  Example: “Asset Management interfaces often with Project Finance”, “Recurring workflow bottleneck is X”.

Rules:
- **Selective** (no transcript dumping)
- **High-signal and reusable**
- **Avoid storing secrets or sensitive information**

Implementation hint (optional):
Use an internal decision structure like:
`{should_write, target, summary, confidence}` and only append when confident.

---

### Feature C - Safe Python Sandbox + Open-Meteo (Optional)
Spin up a Python environment using llm-sandbox (or similar isolation) and allow the chatbot to execute an analysis task by calling a public time series API.

Use this API (no key required): Open-Meteo (historical + forecast weather time series).

- **https://open-meteo.com/**

The Chatbot should:
- Call Open-Meteo for a location/time range
- Retrieve time series data
- Compute basic analytics (rolling averages, volatility, missingness checks, anomaly flags, etc.)
- Return a clear explanation of findings

---
