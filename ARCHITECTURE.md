Architecture Overview
Goal
This project implements an Agentic RAG (Retrieval Augmented Generation) system designed to solve the "amnesia" problem common in LLMs.

The system performs two parallel functions:

Document Intelligence: It ingests user documents (PDF/TXT), chunks them, and retrieves relevant context to answer questions with citations.
Persistent Memory: It uses an LLM Agent to listen for high-signal facts about the User (role, preferences) or the Company (budgets, deadlines) and writes them to persistent storage.
The architecture is built on Streamlit (UI), LangChain (Orchestration), ChromaDB (Vector Storage), and OpenAI GPT-4o (Reasoning).

High-Level Flow
1) Ingestion (Upload → Parse → Chunk)
Supported inputs: .pdf, .txt.
Parsing approach:
PyPDFLoader for PDF extraction.
TextLoader for plain text.
Chunking strategy:
Method: RecursiveCharacterTextSplitter.
Chunk Size: 1000 characters.
Overlap: 200 characters (to preserve semantic continuity across breaks).
Metadata captured per chunk:
source: The original filename.
chunk_id: Implicitly handled via vector index position.
2) Indexing / Storage
Vector store choice: ChromaDB (running in local persistence mode).
Persistence: Embeddings are saved to the ./chroma_db directory on disk.
Embedding Model: OpenAIEmbeddings (text-embedding-3-small or similar).
Optional lexical index: Not implemented (Pure dense retrieval used for simplicity).
3) Retrieval + Grounded Answering
Retrieval method: Semantic Similarity Search (Top-k = 3).
How citations are built:
The LLM receives the page_content and metadata (source) of the top 3 retrieved chunks.
The prompt instructs the model to cite the specific filename when referencing facts.
UI Display: The specific text chunks used for the answer are displayed in an expander ("Sources") below the chat response.
Failure behavior:
If retrieval confidence is low or chunks are irrelevant, the System Prompt instructs the model to admit it doesn't know rather than hallucinating facts.
4) Memory System (Selective)
What counts as "high-signal" memory:
User Facts: Name, job title, specific formatting instructions (e.g., "Answer in JSON").
Company Facts: Project names, deadlines, internal codes, budget figures.
What you explicitly do NOT store:
Conversational filler ("Hi", "How are you").
Ephemeral questions ("What time is it?").
How you decide when to write:
The LLM functions as a Router/Agent. It evaluates the user's input against available Tools.
If the input contains a factual statement, the Agent triggers the save_memory tool.
Format written to:
USER_MEMORY.md: Appends bullet points for user-specific context.
COMPANY_MEMORY.md: Appends bullet points for organizational context.
5) Optional: Safe Tooling
Tool interface shape:
Tools are defined using @tool decorators in LangChain.
Current implementation focuses on Memory Tools (save_memory).
Safety boundaries:
Restricted Scope: The LLM can only write to the specific Markdown files defined in the backend; it cannot overwrite system code.
Human-in-the-loop (Implicit): The UI notifies the user when a memory is saved via the sidebar updates.
Tradeoffs & Next Steps
Why this design?
Simplicity & Portability: Storing memory in Markdown files allows for easy inspection, debugging, and git-versioning without needing a complex SQL setup.
Transparency: The user can literally read the "brain" of the agent in the sidebar.
Cost-Efficiency: ChromaDB runs locally, avoiding cloud vector DB costs for this prototype.
What you would improve with more time:
Structured Database: Migrate memory from Markdown to a Relational DB (PostgreSQL) or Graph DB to handle complex relationships between entities.
Hybrid Search: Implement a connection to BM25 (Lexical Search) alongside Vector Search to better handle specific keyword queries (like exact ID numbers).
Memory Management: Add tools to "Forget" or "Edit" specific memories via the UI, rather than just appending new ones.
Reranking: Add a Cross-Encoder step after retrieval to re-rank the top 10 chunks for higher precision before sending to the LLM.
