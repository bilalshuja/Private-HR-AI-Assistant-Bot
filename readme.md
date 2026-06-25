# 🤖 Private Local Agentic HR Assistant (Multi-Tenant Edition)

A Secure, Local-First, Cloud-Enhanced Agentic RAG System designed for HR operations. This upgraded version features full Docker containerization, Role-Based Access Control (RBAC), and a Multi-Tenant architecture allowing different companies to securely manage their independent HR knowledge bases.

## 📌 Key Highlights

* **Fully Dockerized** → Zero setup hassle; Flask, PostgreSQL, and Redis run in isolated containers.
* **Role-Based Access Control (RBAC)** → Three distinct tiers: Super Admin, Company Admin, and Employee.
* **Multi-Tenant Architecture** → Data segregation ensures employees only interact with their respective company's policies.
* **Local LLM Reasoning (Ollama)** → Maximum privacy for sensitive HR queries.
* **Hybrid RAG** → Pinecone Serverless integration for Dense + Sparse search accuracy.

## 🏗️ System Architecture

The application is deployed using Docker Compose with a modular structure.

| Component         | Technology          | Purpose                           |
| ----------------- | ------------------- | --------------------------------- |
| **LLM Engine**    | Ollama (Llama 3.2)  | Local inference—private and fast  |
| **Vector DB**     | Pinecone Serverless | Hybrid search (Sparse + Dense)    |
| **Relational DB** | PostgreSQL          | Secure storage for Users,Tenants  |
| **Embeddings**    | nomic-embed-text    | High‑quality 768‑dim text vectors |
| **Orchestration** | LangChain           | RAG pipeline + tools integration  |
| **Backend**       | Flask (Python)      | REST API + App Logic              |
| **Memory**        | Redis               | User session & chat history       |
| **Deployment**    | Docker & Docker Compose| Container orchestration & isolated environments |

## 📂 Directory Structure

```text
AI-project-v4
│
├── core/                  # 🧠 Core Business Logic (DB, Models, Processors)
├── data/                  # 📂 Source Documents (e.g., PDFs)
├── routes/                # 🛣️ Application Routes
│   ├── admin_routes.py    # Admin Dashboard & Super Admin Logic
│   └── auth.py            # Login, Registration, Session Management
│
├── static/                # 🎨 Frontend Assets
│   ├── css/style.css
│   └── js/main.js
│
├── templates/             # 📄 Jinja2 HTML Templates
│   ├── company_admin.html # Company Admin Dashboard
│   ├── index.html         # Main Chat Interface
│   ├── login.html         # Authentication UI
│   ├── register.html      # New User Registration UI
│   └── super_admin.html   # Super Admin Control Panel
│
├── vectorstore/           # ⚙️ Sparse Values (BM25)
│   └── bm25_values.json
│
├── app.py                 # 🚀 Flask Application Entry Point
├── Dockerfile             # 🐳 App Container Image Instructions
├── docker-compose.yml     # 🐳 Multi-container Orchestration
├── init_db.py             # 🗄️ Database Table Initialization Script
└── requirements.txt       # Python Dependencies

---
```

```text
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


---

### **3. Download Required LLM Models (Ollama)**

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

⚙️ Installation & Setup (Dockerized)
   1. Prerequisites
Docker & Docker Desktop installed and running.

Ollama installed on your host machine (ollama.com).

Pinecone Serverless index (dimension: 768, metric: dotproduct).

   2. Download Required LLM Models (Ollama)
Ensure Ollama is running on your host machine, then pull the required models:


ollama pull llama3.2
ollama pull nomic-embed-text

3. Configure Environment Variables
Create a .env file in the project root:
```text

# --- Security ---
SECRET_KEY=your_super_secret_random_key

# --- Pinecone Vector DB ---
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=hr-policy-index

# --- Redis Memory ---
REDIS_HOST=redis_db
REDIS_PORT=6379

# --- Database ---
DATABASE_URL=postgresql://postgres:postgres@db:5432/ai_hr_db

# --- Ollama Connection (Docker to Host) ---
OLLAMA_BASE_URL=[http://host.docker.internal:11434](http://host.docker.internal:11434)

```

4. Build and Run the System
Execute the following commands in your terminal to launch the system:

```text
# 1. Ensure a clean slate (removes old containers and volumes)
docker-compose down -v

# 2. Build and start all services in the background
docker-compose up --build -d

# 3. Wait ~5 seconds, then initialize the database tables
docker-compose exec web python init_db.py
```


## 🚀 Usage Guide & Roles
Once the containers are running, access the application at: http://localhost:5000

System Roles
Super Admin (/super-admin)


Creation: Visit http://localhost:5000/create-super-admin to seed the initial Super Admin account.

Capabilities: Can create new Company Admins and manage system-wide tenants.

Company Admin (/dashboard)

Capabilities: Manages their specific company profile. (Future: PDF Knowledge Base upload and versioning).

Employee / User (/)

Capabilities: Standard chat interface. Can only interact with the AI assistant regarding their respective company's policies.
---

 ## 🛠️ Development & Hot-Reloading

This environment is configured for active development. You do not need to restart Docker for standard code changes.

HTML/CSS/JS Changes: Save the file and refresh your browser.

Python (.py) Changes: Gunicorn will auto-reload the Flask server. Save and refresh.

When to restart Docker: Only run docker-compose up --build -d if you add new dependencies to requirements.txt or modify the Dockerfile/docker-compose.yml.

---

## 🔮 Future Roadmap

* [x] Docker containerization (Full stack)
* [x] Admin dashboard & RBAC
  [ ] Dynamic PDF Upload & Auto-Pinecone Ingestion
  [ ] Multi-agent routing with LangGraph
  [ ] Voice Interface via Whisper
---

## 🤝 Contributing

1. Fork the repo
2. Create your branch: `git checkout -b feature/NewFeature`
3. Commit changes
4. Push: `git push origin feature/NewFeature`
5. Submit a Pull Request

---

🔮 Future Roadmap


📜 License
Licensed under the MIT License.
Built with ❤️ using Generative AI

```
