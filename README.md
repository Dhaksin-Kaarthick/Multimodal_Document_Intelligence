# 🚀 Multimodal Document Intelligence Platform

> **Enterprise-grade AI-powered Document Intelligence System** built with **Retrieval-Augmented Generation (RAG)**, **Vision-Language Models (VLMs)**, and a modern asynchronous backend. The platform enables users to upload complex PDFs and standalone images, ask natural language questions, and receive grounded answers with contextual evidence.

Designed with production-oriented architecture rather than a simple proof-of-concept, the system combines OCR, document layout understanding, multimodal reasoning, vector search, and secure user management into a scalable full-stack application.

---

# ✨ Key Features

* 📄 Intelligent PDF and image understanding
* 🤖 Vision-Language Model (Gemma3:4B) integration
* 🔍 Hybrid Retrieval-Augmented Generation (RAG)
* 🧠 Dense semantic vector search using Qdrant
* 📊 Table, chart, and diagram understanding
* 👥 Multi-user isolated document collections
* 🔐 JWT Authentication with secure password hashing
* ⚡ Asynchronous FastAPI backend
* 🌙 Responsive Soft-UI dashboard
* 🌐 Cross-browser optimized (Chrome + Brave)

---

# 📌 Problem Statement

Enterprise documents rarely contain plain text alone. Most include:

* Complex layouts
* Multi-column pages
* Tables
* Charts
* Diagrams
* Embedded figures
* Scanned images

Traditional PDF parsers often lose document structure, resulting in inaccurate retrieval and hallucinated LLM responses.

This platform solves that problem by combining **layout-aware parsing**, **multimodal vision inference**, and **semantic retrieval**, allowing users to interact naturally with complex documents while maintaining contextual accuracy.

---

# 🏗 System Architecture

```text
                User Upload
                     │
          PDF / Image Document
                     │
     ┌───────────────┴────────────────┐
     │                                │
PyMuPDF                      pdfplumber
(Text + Layout)             (Tables)
     │                                │
     └───────────────┬────────────────┘
                     │
        Layout Reconstruction
                     │
      Embedded Images / Graphics
                     │
      Ollama (Gemma3:4B Vision)
                     │
      Visual Semantic Description
                     │
      Combined Document Context
                     │
     Intelligent Text Chunking
                     │
      Embedding Generation
                     │
          Qdrant Vector DB
                     │
      Semantic Similarity Search
                     │
      Retrieved Context Injection
                     │
          Large Language Model
                     │
        Grounded AI Response
```

---

# ⚙ Processing Pipeline

## Stage 1 — Document Ingestion

The platform accepts:

* PDF documents
* Images
* Scanned reports
* Technical manuals
* Research papers

Each upload is assigned to an authenticated user, ensuring complete tenant isolation.

---

## Stage 2 — Dual Extraction Engine

Instead of relying on a single parser, two specialized extraction engines run together.

### PyMuPDF

Responsible for:

* High-fidelity text extraction
* Font metadata
* Bounding box coordinates
* Reading order
* Document layout preservation

### pdfplumber

Responsible for:

* Table extraction
* Structured rows and columns
* Spreadsheet-like content
* Cell reconstruction

Running both engines simultaneously significantly improves extraction quality across diverse document formats.

---

## Stage 3 — Vision-Language Understanding

Many enterprise documents contain information that cannot be extracted as text alone.

Examples include:

* Flowcharts
* Architecture diagrams
* Graphs
* Engineering drawings
* Infographics
* Embedded images

These visual components are automatically routed to an isolated **Gemma3:4B Vision-Language Model** running locally through **Ollama**.

The model generates semantic descriptions that become part of the searchable knowledge base.

---

## Stage 4 — Context Normalization

All extracted information is merged into a unified representation containing:

* Plain text
* Tables
* Visual descriptions
* Metadata
* Layout information

The content is then cleaned and prepared for retrieval.

---

## Stage 5 — Intelligent Chunking

Instead of storing an entire document as one embedding, the platform splits information into semantically meaningful chunks.

Benefits include:

* Higher retrieval precision
* Reduced token usage
* Better contextual relevance
* Faster inference

---

## Stage 6 — Vector Embedding

Each chunk is converted into a high-dimensional dense vector representation.

Every vector stores:

* Document ID
* User ID
* Chunk metadata
* Source page
* Original text
* Visual descriptions

This enables secure multi-user retrieval.

---

## Stage 7 — Semantic Search

When a user asks a question:

1. The query is embedded.
2. Qdrant performs cosine similarity search.
3. Top relevant chunks are retrieved.
4. Matching context is injected into the LLM prompt.

This Retrieval-Augmented Generation (RAG) workflow minimizes hallucinations while improving answer quality.

---

# 🔒 Multi-Tenant Security

Every uploaded document belongs exclusively to its owner.

The retrieval pipeline automatically filters vectors using:

```
user_id
```

This guarantees that:

* User A cannot retrieve User B's documents.
* Context isolation is enforced at the vector database level.
* Authentication and retrieval remain tightly coupled.

---

# 🛠 Technology Stack

## Backend

| Technology  | Purpose                                     |
| ----------- | ------------------------------------------- |
| Python 3.11 | Core programming language                   |
| FastAPI     | High-performance asynchronous API framework |
| SQLAlchemy  | ORM for relational database management      |
| SQLite      | Persistent storage                          |
| Pydantic    | Request validation and serialization        |
| JWT         | Stateless authentication                    |
| scrypt      | Secure password hashing                     |

---

## AI & Retrieval

| Technology        | Purpose                        |
| ----------------- | ------------------------------ |
| Ollama            | Local LLM/VLM inference engine |
| Gemma3:4B         | Vision-Language Model          |
| Qdrant            | Vector database                |
| Dense Embeddings  | Semantic retrieval             |
| Cosine Similarity | Nearest-neighbor search        |

---

## Document Processing

| Library    | Purpose                               |
| ---------- | ------------------------------------- |
| PyMuPDF    | Text extraction with layout awareness |
| pdfplumber | Table extraction                      |
| Pillow     | Image preprocessing                   |

---

## Frontend

* HTML5
* CSS3
* JavaScript
* Soft-UI Dashboard
* Responsive Design
* Dark / Light Theme
* Hardware-accelerated image rendering

---

# 🔐 Authentication Flow

```
User Login
      │
Password
      │
scrypt Hash Verification
      │
JWT Token Issued
      │
Protected API Routes
      │
Authenticated Upload
      │
User-Isolated Retrieval
```

---

# 🌐 Cross-Browser Engineering

One of the project's engineering challenges involved browser rendering inconsistencies.

Issues addressed include:

* Chrome rendering behavior
* Brave Shields restrictions
* Scroll event inconsistencies
* Image transform limitations
* Browser sandbox isolation

The solution migrated client-side state management into a centralized server cache, ensuring synchronized sessions and consistent rendering across browsers.

---

# 📂 Project Structure

```text
project/
│
├── backend/
│   ├── api/
│   ├── auth/
│   ├── database/
│   ├── models/
│   ├── services/
│   ├── rag/
│   ├── embeddings/
│   ├── vector_db/
│   └── main.py
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── assets/
│   └── index.html
│
├── uploads/
│
├── qdrant_storage/
│
├── docker-compose.yml
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

* Docker Engine
* Docker Compose
* Python 3.11
* Ollama

---

## 1. Install Ollama

```bash
ollama pull gemma3:4b
```

---

## 2. Clone Repository

```bash
git clone <repository-url>

cd multimodal-document-intelligence
```

---

## 3. Start Services

```bash
docker compose up --build
```

---

## 4. Run Backend

```bash
uvicorn main:app --reload
```

---

## 5. Open Application

```
http://localhost:8000
```

---

# 📈 Future Enhancements

* Hybrid BM25 + Dense Retrieval
* OCR fallback using PaddleOCR
* Streaming LLM responses
* Redis distributed caching
* PostgreSQL production deployment
* Kubernetes orchestration
* GPU inference optimization
* Role-based access control (RBAC)
* Multi-document conversations
* Citation highlighting
* Knowledge graph integration

---

# 💼 Why This Project Stands Out

Unlike typical academic RAG demonstrations, this project emphasizes production engineering principles:

* Multimodal document understanding
* Layout-aware extraction
* Local Vision-Language inference
* Secure multi-tenant retrieval
* Asynchronous backend architecture
* Cross-browser compatibility engineering
* Retrieval-grounded AI responses
* Modular and scalable system design

The platform showcases practical skills across **Generative AI**, **Retrieval-Augmented Generation**, **Computer Vision**, **Backend Engineering**, **Vector Databases**, **Authentication**, and **Full-Stack Development**, making it a strong portfolio project for **AI Engineer**, **Machine Learning Engineer**, **LLM Engineer**, and **Generative AI Developer** roles.

---

# 👨‍💻 Author

**Dhaksin Kaarthick**

If you found this project interesting, feel free to ⭐ the repository and connect for discussions on AI, Large Language Models, Retrieval-Augmented Generation, and Multimodal Intelligence.
