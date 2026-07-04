# Multimodal Document Intelligence Platform

An enterprise-grade, high-performance Retrieval-Augmented Generation (RAG) engine designed to ingest unstructured PDFs and complex standalone image layouts. The platform processes raw files through an optical layout-extraction pipeline, builds optimized sparse/dense multi-tenant vector structures, and conducts local neural semantic inference using an isolated `Gemma3:4b` Vision-Language Model (VLM).

Developed as a modern full-stack application, the platform solves real-world cross-browser rendering inconsistencies (Chrome vs. Brave Shields) and decouples isolated client browser sandbox limitations by migrating state management to a unified central server cache database.

---

## 🏗️ Architecture & Processing Pipeline

The platform departs from traditional single-threaded PDF parsers by implementing a multi-stage, parallelized document routing pipeline:

1. **Dual-Engine Text Extraction**: Raw PDF streams are simultaneously handled by `PyMuPDF` for high-fidelity text/font-bounding layout mapping and `pdfplumber` for robust structural table sheet extraction.
2. **VLM Graphics Recognition**: Non-text elements, chart vectors, diagrams, and embedded image layers are isolated and routed natively to an `Ollama` multimodal VLM sub-process for natural language visual semantic mapping.
3. **High-Density Vector Tokenization**: Context structures are normalized, parsed via customized text-chunk layers, transformed into 768-dimensional dense vector embeddings, and indexed with strong multi-tenant (`user_id`) metadata bounds.
4. **Isolated Memory Retrieval**: Qdrant vector databases execute geometric cosine-similarity intersection lookups, injecting the top context blocks into the targeted LLM prompt context payload window.

---

## 🛠️ Tech Stack & Production Tooling

### Core Backend (High-Concurrency Async Architecture)

- **Framework**: `FastAPI` (Python 3.11 Execution Engine) utilizing explicit type-hinting, structured Pydantic input models, and asynchronous task workers.
- **Database Mapping & Persistence**: `SQLAlchemy` ORM driving a local SQLite instance for persistent user profile schemas, coupled with an in-memory `global_chats_db` map matrix for real-time web session synchronization.
- **Vector Database Client**: `Qdrant DB` running in high-performance local disk-storage mode.
- **Security Layer**: Native Cryptographic `scrypt` salt matrix password hashing paired with stateless `JSON Web Token (JWT)` Bearer authentication guard routes.

### Premium Frontend (Soft-UI Analytics Control Room)

- **Interface Layer**: Semantic HTML5 / CSS3 compiled via standard utility configurations.
- **Styling Paradigm**: Neo-brutalist / Soft-UI Fluid Canvas design system with custom hardware-accelerated dark/light theme properties.
- **Cross-Browser Hardening**: Hard-coded transformation matrices over native DOM scroll logic, enabling unbounded image panning (left, right, up, down) and UI rendering consistency across Chrome and strict Brave privacy shields.

---

## ⚙️ Local Development Quickstart

### Prerequisites

- Docker Engine & Docker Compose installed on your host system.
- Local Ollama engine daemon running on your host machine.

### 1. Setup Local AI Inference Node

Pull down the targeted vision-language model locally on your machine:

```bash
ollama pull gemma3:4b
```
