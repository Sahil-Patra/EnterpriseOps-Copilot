# 🌐 EnterpriseOps Copilot — Universal Agentic AI & RAG Platform

An enterprise-ready AI Copilot that combines **Dynamic Retrieval-Augmented Generation (RAG)** with **Autonomous Tool Calling** to automate knowledge discovery, talent allocation, and operational workflows.

Powered by **LangChain**, **Google Gemini 1.5 Flash**, and **Streamlit**.

---

## 🚀 Key Features

- 📄 **Dynamic RAG Engine**: Ingests, chunks, and indexes uploaded enterprise PDFs or TXT documents (SOPs, security policies, playbooks) on the fly using in-memory vector embeddings for grounded, zero-hallucination answers.
- 🤖 **Agentic Tool Calling (`bind_tools`)**: Uses native LLM function routing to inspect user intent and autonomously choose between knowledge retrieval, database lookups, or direct conversation.
- 👥 **Talent & Staffing Sourcing Tool**: Autonomously parses and queries internal engineering directories to match staff by technical competencies, cloud proficiencies, and availability.
- ⚡ **Workflow Automation Tool**: Dispatches simulated enterprise operational actions (scheduling interviews, technical screenings, logging CRM records) with zero manual intervention.
- 💬 **Interactive Streamlit UI**: Multi-turn conversation management with real-time feedback on agent execution and tool selection.

---

## 🛠️ Architecture Overview

```text
User Query
    │
    ▼
LLM with Native Tool Binding (`bind_tools`)
    │
    ├──► [Tool: RAG Vector Store] ──► Query Dynamic Document/SOP Embeddings
    ├──► [Tool: Talent Directory]  ──► Query Candidate/Staff Database
    ├──► [Tool: Workflow Engine]   ──► Dispatch Calendar & CRM Events
    │
    ▼
Context Synthesis & Grounded Response
```

## 📦 Tech Stack
- Framework: LangChain (langchain-core, langchain-google-genai)
- LLM & Embeddings: Google Gemini 1.5 Flash & text-embedding-004
- User Interface: Streamlit
- Document Processing: PyPDFLoader
- Vector Store: In-Memory Vector Store
##⚡ Quick Start
1. Clone the Repository
```
git clone https://github.com/YOUR_USERNAME/enterprise-ops-copilot.git
cd enterprise-ops-copilot
```
2. Install Dependencies
```
pip install -r requirements.txt
```
3. Run the Application
```
streamlit run app.py
```
4. Provide API Key
Open the app in your browser (http://localhost:8501).
Enter your free Google Gemini API Key in the sidebar (get one free at Google AI Studio).

## 💡 Example Queries to Test

| Capability | Example Prompt |
| :--- | :--- |
| **RAG / Policy Search** | *"What is our policy regarding remote work network security?"* |
| **Dynamic Document RAG** | Upload any PDF in sidebar and ask: *"Summarize section 2 of the uploaded document."* |
| **Talent Sourcing** | *"Find an engineer with Kubernetes and Cloud infrastructure skills."* |
| **Workflow Automation** | *"Schedule a technical interview with Alex Chen for Thursday at 2 PM."* |
