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