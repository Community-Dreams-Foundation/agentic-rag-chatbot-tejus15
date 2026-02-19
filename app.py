import streamlit as st
import os
from backend import ingest_file, query_agent

st.set_page_config(page_title="RAG & Memory Agent", layout="wide")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🗄️ Knowledge Base")
    uploaded_file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt"])
    
    if uploaded_file and st.button("Ingest File"):
        with st.spinner("Processing..."):
            try:
                chunks = ingest_file(uploaded_file)
                st.success(f"Ingested {chunks} chunks!")
            except Exception as e:
                st.error(f"Error: {e}")
            
    st.markdown("---")
    st.subheader("🧠 Persistent Memory")
    
    tab1, tab2 = st.tabs(["User", "Company"])
    with tab1:
        if os.path.exists("USER_MEMORY.md"):
            with open("USER_MEMORY.md", "r") as f:
                st.markdown(f.read())
        else:
            st.info("No user memories yet.")
    with tab2:
        if os.path.exists("COMPANY_MEMORY.md"):
            with open("COMPANY_MEMORY.md", "r") as f:
                st.markdown(f.read())
        else:
            st.info("No company memories yet.")

# Main Chat
st.title("🤖 Agentic RAG Chatbot")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer, docs, mem_status = query_agent(prompt)
                st.markdown(answer)
                
                if docs:
                    with st.expander("📚 Sources"):
                        for d in docs:
                            st.caption(f"**Source:** {d.metadata.get('source')} | {d.page_content[:150]}...")
                
                if mem_status:
                    st.info(mem_status)
                    
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"An error occurred: {e}")
