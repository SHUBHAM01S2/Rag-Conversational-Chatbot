
# Conversational AI Chatbot

A **Retrieval-Augmented Generation (RAG) powered Conversational Chatbot** that allows users to interact with AI, upload documents, and retrieve context-aware responses based on their uploaded files and chat history.

---

## Features

- **Context-Aware Conversations:** Maintains session-based chat history to provide coherent and relevant answers.
- **Document Upload & Indexing:** Supports PDF, DOCX, and HTML files for retrieval of relevant information.
- **Vector Search with ChromaDB:** Uses vector embeddings for fast and accurate document search.
- **Database Logging:** Logs all conversations and document uploads in SQLite.
- **FastAPI Backend:** High-performance API for real-time interactions.

---

## Tech Stack

- **Language & Framework:** Python, FastAPI  
- **AI & NLP:** LangChain, RAG (Retrieval-Augmented Generation)  
- **Database:** SQLite for logging, ChromaDB for vector storage  
- **Other Tools:** UUID, Shutil, Logging

---

## Setup & Installation

1. **Clone the repository:**

```bash
git clone https://github.com/SHUBHAM01S2/Rag-Conversational-Chatbot.git
cd your-repo
````

2. **Create a virtual environment and activate it:**

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Start the FastAPI server:**

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Access the API docs:**
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

---

## Usage

### 1. Chat Endpoint

* **POST** `/chat`
* **Body:** `QueryInput`
* **Response:** `QueryResponse`
* Maintains conversation history and returns AI-generated responses.

### 2. Upload Document

* **POST** `/upload-doc`
* **Body:** File (PDF, DOCX, HTML)
* Indexes documents for retrieval.

### 3. List Documents

* **GET** `/list-docs`
* Returns a list of uploaded documents.

### 4. Delete Document

* **POST** `/delete-doc`
* Deletes document from both database and Chroma vector store.

---

## Folder Structure

```
project-root/
│
├─ api/
│  ├─ main.py               # FastAPI entrypoint
│  ├─ db_utils.py           # SQLite DB operations
│  ├─ langchain_utils.py    # RAG chain integration
│  ├─ chroma_utils.py       # Chroma vector store utils
│  └─ pydantic_models.py    # Request/Response models
│
├─ requirements.txt         # Python dependencies
└─ README.md
```

---

## Future Improvements

* Multi-modal support (images, audio)
* Advanced conversational memory
* Deployment on cloud platforms with authentication

---

## License

This project is licensed under the MIT License.

