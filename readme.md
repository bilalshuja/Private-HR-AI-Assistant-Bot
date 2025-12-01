# 🤖 Private Local Agentic HR Assistant

A **Secure, Local-First, Cloud-Enhanced Agentic RAG System** designed for HR operations. This project allows organizations to process sensitive HR policy queries using **Local LLMs via Ollama**, while leveraging **Pinecone Hybrid Search (Sparse + Dense)** for scalable cloud retrieval.

---

## 📌 Key Highlights

*  **Local LLM Reasoning** (Ollama) → Full privacy
*  **Hybrid RAG** → Dense + Sparse search for maximum accuracy
*  **Modular Architecture** → Clean and scalable
*  **Production Ready** → Designed for real HR environments
*  **PDF Knowledge Base** → Fully indexed HR policies

---

## 🏗️ System Architecture

The application follows a **Modular Monolith** design with clear separation of responsibilities.

### **Architecture Components**

| Component         | Technology          | Purpose                           |
| ----------------- | ------------------- | --------------------------------- |
| **LLM Engine**    | Ollama (Llama 3.2)  | Local inference—private and fast  |
| **Vector DB**     | Pinecone Serverless | Hybrid search (Sparse + Dense)    |
| **Embeddings**    | nomic-embed-text    | High‑quality 768‑dim text vectors |
| **Orchestration** | LangChain           | RAG pipeline + tools integration  |
| **Backend**       | Flask (Python)      | REST API + App Logic              |
| **Memory**        | Redis               | User session & chat history       |
| **Frontend**      | HTML / CSS / JS     | Modern, responsive UI             |

### **Directory Structure**

```
HR-Assistant-Chatbot
│
├── core/                  # 🧠 The Brain (Logic Layer)
│   ├── config.py          # Central Config & Env Variables
│   ├── rag_pipeline.py    # Hybrid RAG Logic
│   ├── chat_memory.py     # Redis-Based Memory Manager
│   └── ingest.py          # ETL + Hybrid Indexing
│
├── static/                # 🎨 Frontend Assets
│   ├── css/style.css
│   └── js/main.js
│
├── templates/             # 📄 HTML Templates
│   └── index.html
│
├── data/                  # 📂 Source Documents
│   └── *.pdf              # HR Policies
│
├── vectorstore/           # ⚙️ Sparse Values
│   └── bm25_values.json
│
├── app.py                 # 🚀 Application Entry Point
└── requirements.txt       # Dependency List
```

---

## ⚙️ Installation & Setup

### **1. Prerequisites**

* Python 3.9+
* Pinecone serverless index (dimension: 768, metric: `dotproduct`)
* Redis (run locally: `redis-server`)
* Ollama installed (`ollama.com`)

---

### **2. Clone Repository**

```bash
git clone https://github.com/yourusername/hr-assistant-chatbot.git
cd hr-assistant-chatbot
```

---

### **3. Download Required LLM Models (Ollama)**

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

---

### **4. Setup Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

### **5. Configure Environment Variables**

Create `.env` in project root:

```ini
# --- Flask Security ---
SECRET_KEY=your_super_secret_random_key

# --- Pinecone Vector DB ---
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=hr-policy-index  # Must use 'dotproduct' metric

# --- Redis Memory ---
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

---

## 🚀 Usage Guide

### **Step 1 — Ingest HR PDFs (Build Knowledge Base)**

This script reads all PDFs from `data/`, generates Hybrid (Dense + Sparse) vectors, and uploads them to Pinecone.

```bash
python -m core.ingest
```

**Output:**

```
🎉 Ingestion Complete! Vectors successfully uploaded.
```

---

### **Step 2 — Run the Application**

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

Try queries such as:

* *"What is the sick leave policy?"*
* *"How many annual leaves are allowed?"*
* *"Is there a travel allowance in the company?"*

---

## 🛠️ Troubleshooting

| Issue                        | Solution                                             |
| ---------------------------- | ---------------------------------------------------- |
| **Pinecone Metric Error**    | Use `dotproduct`, hybrid doesn’t work with `cosine`. |
| **Ollama not responding**    | Ensure `ollama serve` is running.                    |
| **BM25 params missing**      | Run ingestion script once to generate JSON.          |
| **Redis connection refused** | Start Redis: `redis-server`.                         |

---

## 🔮 Future Roadmap

* [ ] Docker containerization (Full stack)
* [ ] Multi-agent routing with LangGraph
* [ ] Voice Interface via Whisper
* [ ] Admin dashboard for PDF uploads

---

## 🤝 Contributing

1. Fork the repo
2. Create your branch: `git checkout -b feature/NewFeature`
3. Commit changes
4. Push: `git push origin feature/NewFeature`
5. Submit a Pull Request

---

## 📜 License

Licensed under the **MIT License**.

Built with ❤️ using Generative AI
