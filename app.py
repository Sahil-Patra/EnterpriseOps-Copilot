import streamlit as st
import json
import tempfile

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.document_loaders import PyPDFLoader

# ==========================================
# 1. UI & CONFIGURATION
# ==========================================
st.set_page_config(page_title="EnterpriseOps Copilot", page_icon="🌐", layout="wide")

st.title("🌐 EnterpriseOps: Universal Agentic Copilot")
st.caption("100% Free & Open Tech Stack: Powered by Google Gemini & LangChain")

with st.sidebar:
    st.header("🔑 Free Setup")
    api_key = st.text_input("Enter Free Gemini API Key", type="password", help="Get free key at aistudio.google.com")
    st.caption("[Get a Free Google AI Studio Key](https://aistudio.google.com/) (No credit card required)")
    
    st.divider()
    st.subheader("📄 Dynamic RAG Document Ingestion")
    st.write("Upload any PDF/TXT (SOP, Policy, Whitepaper) to vectorize on the fly:")
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "txt"])

# ==========================================
# 2. DEFAULT ENTERPRISE SOPs (Fallback)
# ==========================================
DEFAULT_DOCS = [
    Document(
        page_content="Enterprise Onboarding SOP: Standard team onboarding takes 2 weeks. All engineers undergo zero-trust security compliance training and 2FA setup before repository access is granted.",
        metadata={"source": "Enterprise IT SOP"}
    ),
    Document(
        page_content="Cloud Migration & DevOps Standard: Systems adhere to containerization standards (Docker/Kubernetes). Production deployments require automated CI/CD with zero-downtime blue/green rollouts.",
        metadata={"source": "Cloud Architecture Policy"}
    ),
    Document(
        page_content="Remote & Hybrid Work Policy: Engineers must connect via secure company VPNs. Client intellectual property and codebases must remain strictly isolated within approved cloud environments.",
        metadata={"source": "HR & Security Guidelines"}
    )
]

def process_uploaded_file(uploaded_file):
    """Processes uploaded PDF or TXT files into LangChain Documents."""
    if uploaded_file.name.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        loader = PyPDFLoader(tmp_path)
        return loader.load_and_split()
    else:
        text_content = uploaded_file.read().decode("utf-8")
        return [Document(page_content=text_content, metadata={"source": uploaded_file.name})]

# ==========================================
# 3. AGENT TOOLS & RAG ENGINE
# ==========================================
def run_agentic_workflow(user_query, api_key, active_docs):
    # Free Gemini 1.5 Flash Model & Free Embedding Model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=api_key
    )

    # In-memory vector store for RAG
    vector_store = InMemoryVectorStore.from_documents(active_docs, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    # --- Tool 1: RAG Knowledge Base / SOP Search ---
    @tool
    def search_knowledge_base(query: str) -> str:
        """Search the company knowledge base, uploaded documentation, internal SOPs, and operating standards."""
        results = retriever.invoke(query)
        if not results:
            return "No matching information found in the uploaded documents."
        return "\n\n".join([f"Source [{d.metadata.get('source', 'Doc')}]: {d.page_content}" for d in results])

    # --- Tool 2: Universal Talent / HR Search ---
    @tool
    def search_talent_directory(skill_or_role: str) -> str:
        """Search the enterprise talent pool and employee directory by skill, technology, or position."""
        talent_pool = [
            {"name": "Alex Chen", "role": "Senior Cloud/DevOps Engineer", "skills": "AWS, Kubernetes, Terraform, CI/CD", "status": "Available"},
            {"name": "Maria Rodriguez", "role": "Full-Stack AI Developer", "skills": "Python, LangChain, RAG, FastAPI, React", "status": "Available"},
            {"name": "Sarah Jenkins", "role": "Cybersecurity & Compliance Lead", "skills": "SOC2, ISO27001, Zero-Trust, DLP", "status": "On Assignment"},
            {"name": "Vikram Patel", "role": "Enterprise Data Architect", "skills": "Databricks, Snowflake, PySpark, PowerBI", "status": "Available"}
        ]
        matches = [
            t for t in talent_pool 
            if skill_or_role.lower() in t["skills"].lower() or skill_or_role.lower() in t["role"].lower()
        ]
        if not matches:
            return f"No direct match found for '{skill_or_role}'. Available domains: Cloud/DevOps, AI Developer, Cybersecurity, Data Architect."
        return json.dumps(matches, indent=2)

    # --- Tool 3: Workflow Automation ---
    @tool
    def trigger_workflow_action(action_name: str, target_person_or_system: str, details: str) -> str:
        """Dispatch enterprise workflows like scheduling meetings, logging tickets, or sending email notifications."""
        return (
            f"✅ WORKFLOW EXECUTED: Action '{action_name}' initiated for '{target_person_or_system}'. "
            f"Details: {details}. Successfully logged in enterprise management system."
        )

    tools = [search_knowledge_base, search_talent_directory, trigger_workflow_action]
    tool_map = {t.name: t for t in tools}

    # Bind tools natively to LLM
    llm_with_tools = llm.bind_tools(tools)

    system_instruction = (
        "You are the EnterpriseOps Copilot, an AI assistant for enterprise teams. "
        "You have tools for knowledge search (`search_knowledge_base`), HR/talent search (`search_talent_directory`), "
        "and workflow automation (`trigger_workflow_action`). "
        "If a tool is needed, call it. If no tool is needed, reply directly and professionally."
    )

    messages = [SystemMessage(content=system_instruction), HumanMessage(content=user_query)]
    
    # 1. Model evaluates query and decides if tools are required
    ai_response = llm_with_tools.invoke(messages)

    # 2. If tools are chosen, execute them and synthesize the response
    if hasattr(ai_response, "tool_calls") and ai_response.tool_calls:
        tool_results_summary = ""
        for tool_call in ai_response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            if tool_name in tool_map:
                executed_tool = tool_map[tool_name]
                raw_result = executed_tool.invoke(tool_args)
                tool_results_summary += f"\n[Executed {tool_name}]:\n{raw_result}\n"

        # Final synthesis call
        synthesis_prompt = f"""
        User Question: {user_query}
        Tool Execution Results: {tool_results_summary}
        
        Provide a concise, professional answer to the user based strictly on the executed results.
        """
        final_answer = llm.invoke(synthesis_prompt).content
        return final_answer
    else:
        return ai_response.content

# ==========================================
# 4. CHAT UI
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! I am your EnterpriseOps Copilot. You can ask me to search knowledge docs, find team talent, or trigger automated workflows."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Ask a policy question, search talent by skill, or trigger a task...")

with st.sidebar:
    st.divider()
    st.write("**Quick Demos to Try:**")
    st.caption("1. 📄 *RAG Lookup:* 'What is our policy on remote work security?'")
    st.caption("2. 👥 *Talent Search:* 'Find me someone with Kubernetes and Cloud skills.'")
    st.caption("3. ⚡ *Automation:* 'Schedule an interview with Alex Chen next Tuesday.'")

if user_query:
    if not api_key:
        st.warning("⚠️ Please enter your free Gemini API Key in the sidebar.")
    else:
        # Check if user uploaded a file
        active_docs = process_uploaded_file(uploaded_file) if uploaded_file else DEFAULT_DOCS

        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing intent & calling tools..."):
                try:
                    response_text = run_agentic_workflow(user_query, api_key, active_docs)
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")