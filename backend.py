import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Updated Imports to fix ModuleNotFoundError
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()

# -- CONFIG --
VECTOR_STORE_DIR = "./chroma_db"
USER_MEMORY_FILE = "USER_MEMORY.md"
COMPANY_MEMORY_FILE = "COMPANY_MEMORY.md"

def get_llm():
    return ChatOpenAI(model="gpt-4o", temperature=0)

def ingest_file(uploaded_file):
    """Processes an uploaded file (PDF/TXT) into the Vector DB."""
    
    # Save temp file
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load
    if temp_path.endswith(".pdf"):
        loader = PyPDFLoader(temp_path)
    else:
        loader = TextLoader(temp_path)
    docs = loader.load()

    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Embed & Store
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=VECTOR_STORE_DIR
    )
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return len(splits)

def retrieve_context(query):
    """Retrieves relevant chunks from ChromaDB."""
    embeddings = OpenAIEmbeddings()
    if not os.path.exists(VECTOR_STORE_DIR):
        return []
        
    vectorstore = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings)
    results = vectorstore.similarity_search(query, k=3)
    return results

def write_to_memory(category, fact):
    """Writes high-signal facts to Markdown files."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = USER_MEMORY_FILE if category == "user" else COMPANY_MEMORY_FILE
    
    entry = f"\n- **[{timestamp}]**: {fact}"
    
    with open(filename, "a") as f:
        f.write(entry)
    return f"Saved to {filename}"

def query_agent(query):
    """
    Main Agent Loop:
    1. Retrieve Context
    2. Call LLM with Tools (Memory)
    """
    context_docs = retrieve_context(query)
    context_text = "\n\n".join([f"[Source: {d.metadata.get('source', 'Doc')}]\n{d.page_content}" for d in context_docs])

    # Construct System Prompt
    system_prompt = f"""
    You are a helpful assistant.
    
    1. Answer the user's question based ONLY on the following Context.
    2. CITATIONS: Always cite your sources using [Source: filename].
    
    MEMORY RULES:
    - If the user states a preference/role (e.g., "I am a Data Scientist"), save it to User Memory.
    - If you find an organizational fact (e.g., "Budget is $50k"), save it to Company Memory.
    
    CONTEXT:
    {context_text}
    """

    llm = get_llm()
    
    # Define Tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "save_memory",
                "description": "Save a fact to memory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "enum": ["user", "company"]},
                        "fact": {"type": "string", "description": "The fact to remember."}
                    },
                    "required": ["category", "fact"]
                }
            }
        }
    ]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    response = llm.invoke(messages, functions=[t['function'] for t in tools])
    
    memory_status = ""
    final_answer = response.content

    if response.additional_kwargs.get("function_call"):
        func_args = json.loads(response.additional_kwargs["function_call"]["arguments"])
        mem_result = write_to_memory(func_args["category"], func_args["fact"])
        memory_status = f"🧠 *Memory Updated: {mem_result}*"
        if not final_answer:
            final_answer = "I've noted that down in memory."

    return final_answer, context_docs, memory_status
