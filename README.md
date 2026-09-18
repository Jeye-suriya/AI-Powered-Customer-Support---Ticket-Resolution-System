# SupportAI

### AI-Powered Customer Support Ticket Resolution System

> An intelligent customer-support automation system that understands customer tickets, identifies their intent, retrieves relevant knowledge, generates grounded RAG responses, and routes uncertain or sensitive cases to human support.

<p align="center">

**77 Support Intents** · **153 Knowledge Articles** · **92.21% Intent Accuracy** · **95.78% OOS Accuracy**

</p>

---

## Overview

SupportAI is an end-to-end AI customer-support system designed to automate the ticket-resolution workflow while maintaining a controlled path to human support.

Instead of sending every ticket directly to a generative AI model, SupportAI uses a multi-stage pipeline:

```text
Customer Ticket
      ↓
Text Preprocessing
      ↓
Out-of-Scope Detection
      ↓
Intent Classification
      ↓
Knowledge Base Retrieval
      ↓
Intent-Aware Reranking
      ↓
RAG Response Generation
      ↓
Escalation Decision
      ↓
Resolved / Escalated
      ↓
Ticket Storage
```

The system combines **semantic machine learning, vector retrieval, RAG, generative AI, confidence-based decisions, and persistent ticket management**.

---

## Architecture

```text
┌──────────────────────┐
│   Customer / Agent   │
│      Ticket          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     Streamlit UI     │
│ Ticket Submission &  │
│    Ticket History    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       FastAPI        │
│      REST API        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Ticket Pipeline   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   OOS Detection      │
│ MiniLM + Logistic    │
│     Regression       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Intent Classification│
│ MiniLM + Logistic    │
│     Regression       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Semantic Retrieval  │
│      ChromaDB        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Intent-Aware        │
│     Reranking        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       RAG            │
│      Gemini          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Escalation Service   │
│ Confidence + Rules   │
└──────────┬───────────┘
           │
       ┌───┴────┐
       ▼        ▼
   Resolved  Escalated
       │        │
       └───┬────┘
           ▼
┌──────────────────────┐
│        SQLite        │
│    Ticket History    │
└──────────────────────┘
```

---

# Key Features

### Intelligent Ticket Understanding

- Detects out-of-scope requests before intent classification.
- Supports **77 customer-support intents**.
- Uses semantic embeddings to understand variations in customer language.

### Knowledge-Grounded Retrieval

- **153 structured support articles**.
- Semantic vector search using ChromaDB.
- Cosine-similarity based retrieval.
- Intent-aware reranking using the predicted support intent.

### RAG Response Generation

- Retrieves relevant support information before response generation.
- Provides retrieved knowledge as context to Gemini.
- Generates customer-facing responses grounded in application-specific support information.

### Confidence-Aware Escalation

Tickets can be escalated when:

- Intent confidence is below the configured threshold.
- No sufficiently relevant knowledge article is found.
- A configured escalation condition applies.
- The AI generation service encounters an error.

### Persistent Ticket Management

- SQLite-based ticket storage.
- Ticket history.
- Individual ticket lookup.
- REST API access.

### Web Interface

The Streamlit application provides:

- Dashboard
- New Ticket
- AI Resolution
- Ticket History
- System Status

---

# AI Pipeline

## 1. Out-of-Scope Detection

The first stage determines whether an incoming request belongs to the supported customer-support domain.

### Model

| Component | Implementation |
|---|---|
| Embedding Model | `all-MiniLM-L6-v2` |
| Embedding Size | 384 |
| Classifier | Logistic Regression |
| Class Weight | Balanced |

**Evaluation Accuracy: 95.78%**

Example:

```text
"What is the weather today?"
```

The system identifies the request as outside the supported support domain.

---

## 2. Intent Classification

In-domain tickets are classified into one of **77 customer-support intents**.

The taxonomy covers areas including:

- Cards
- Card Payments
- Transfers
- Top-ups
- Cash Withdrawals
- Identity Verification
- Account Management
- Virtual Cards
- Currency and Exchange
- Refunds
- Security

### Model

| Component | Implementation |
|---|---|
| Embedding Model | `all-MiniLM-L6-v2` |
| Classifier | Logistic Regression |
| Intent Classes | 77 |

**Test Accuracy: 92.21%**

Example:

```text
"My card payment is still pending."
```

Prediction:

```text
pending_card_payment
```

---

## 3. Knowledge Base

SupportAI uses a structured knowledge base as the information source for retrieval and response generation.

### Current Knowledge Base

**153 support articles**

Each article contains structured fields including:

```text
KB ID
Category
Intent
Title
Problem
Symptoms
Resolution Steps
Additional Information
Escalation Condition
Search Text
```

Source:

```text
data/support_knowledge_base.csv
```

---

## 4. Semantic Retrieval

Knowledge-base articles are converted into semantic embeddings using:

```text
all-MiniLM-L6-v2
```

The embeddings are stored in:

```text
ChromaDB
```

Retrieval workflow:

```text
Customer Ticket
      ↓
Semantic Embedding
      ↓
Vector Search
      ↓
Relevant KB Articles
```

The system uses cosine similarity to retrieve semantically related support articles.

---

## 5. Intent-Aware Reranking

Semantic similarity alone can return articles belonging to closely related support issues.

SupportAI therefore combines semantic similarity with the predicted intent:

```text
Semantic Similarity
        +
Predicted Intent Match
        ↓
Final Ranking
```

This improves the ranking of articles that match the detected support intent while preserving semantic retrieval.

### Retrieval Evaluation

| Metric | Result |
|---|---:|
| Retrieval Coverage | **85.42%** |
| Top-1 Intent Accuracy | **71.59%** |
| Top-3 Intent Recall | **74.29%** |
| Mean Reciprocal Rank | **85.27%** |
| Average Top Similarity | **59.74%** |

---

## 6. Retrieval-Augmented Generation

After retrieval, relevant knowledge-base content is provided to Gemini as context.

```text
Ticket
  ↓
Intent
  ↓
Relevant KB Articles
  ↓
Context Construction
  ↓
Gemini
  ↓
Customer Response
```

The generation stage is designed to:

- Use retrieved support information.
- Produce a clear customer-facing response.
- Avoid unsupported claims.
- Follow available resolution information.
- Consider applicable escalation conditions.

---

## 7. Escalation

SupportAI does not force every ticket into automatic resolution.

The escalation layer considers:

```text
Low Intent Confidence
        OR
No Relevant KB Article
        OR
Escalation Condition
        OR
AI Service Failure
```

Current intent confidence threshold:

```text
0.60
```

This provides a controlled path for uncertain or sensitive support cases.

---

# Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Backend | FastAPI |
| Frontend | Streamlit |
| Validation | Pydantic |
| Machine Learning | Scikit-learn |
| Embeddings | Sentence Transformers |
| Embedding Model | `all-MiniLM-L6-v2` |
| Classifier | Logistic Regression |
| Vector Database | ChromaDB |
| Generative AI | Google Gemini |
| Database | SQLite |
| Package Management | uv |
| Version Control | Git / GitHub |

---

# Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── data/
│   │   │   ├── audit.py
│   │   │   ├── database.py
│   │   │   └── preprocess.py
│   │   │
│   │   ├── models/
│   │   │   ├── intent_classifier.py
│   │   │   └── oos_detector.py
│   │   │
│   │   ├── rag/
│   │   │   └── generator.py
│   │   │
│   │   ├── retrieval/
│   │   │   └── knowledge_base.py
│   │   │
│   │   ├── services/
│   │   │   ├── escalation.py
│   │   │   └── ticket_pipeline.py
│   │   │
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── evaluate_pipeline.py
│   ├── analyze_*.py
│   └── build_*_kb.py
│
├── data/
│   ├── train.csv
│   ├── test.csv
│   ├── categories.json
│   ├── data_full.json
│   ├── support_knowledge_base.csv
│   └── tickets.db
│
├── models/
│   ├── intent/
│   │   └── intent_classifier.joblib
│   │
│   ├── oos/
│   │   ├── oos_detector.joblib
│   │   └── threshold.json
│   │
│   └── vector_db/
│
├── frontend/
│   └── app.py
│
├── src/
├── .streamlit/
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# API

SupportAI exposes a REST API through FastAPI.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | API health check |
| `POST` | `/api/tickets` | Process a support ticket |
| `GET` | `/api/tickets` | Retrieve ticket history |
| `GET` | `/api/tickets/{ticket_id}` | Retrieve a specific ticket |

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Example Request

```http
POST /api/tickets
```

```json
{
  "ticket": "I forgot my password and cannot log in."
}
```

The API returns the ticket result, including the detected intent, confidence, response, sources, status, and escalation information where applicable.

---

# Database

Processed tickets are persisted using SQLite:

```text
data/tickets.db
```

This allows ticket history to remain available across application restarts.

---

# Evaluation

The current evaluation was performed using the held-out in-domain test set.

| Component | Metric | Result |
|---|---|---:|
| OOS Detector | Accuracy | **95.78%** |
| Intent Classifier | Accuracy | **92.21%** |
| KB Retrieval | Coverage | **85.42%** |
| KB Retrieval | Top-1 Intent Accuracy | **71.59%** |
| KB Retrieval | Top-3 Intent Recall | **74.29%** |
| KB Retrieval | MRR | **85.27%** |
| Pipeline Routing | Accuracy | **91.46%** |

These metrics represent different stages of the system and are **not combined into a single overall accuracy score**.

### Run Evaluation

```powershell
uv run python -m backend.evaluate_pipeline
```

---

# Getting Started

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Google Gemini API access

## 1. Clone

```powershell
git clone <your-repository-url>
cd AI-Powered-Customer-Support-Ticket-Resolution-System
```

## 2. Install Dependencies

```powershell
uv sync
```

## 3. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit API keys or other secrets to GitHub.

## 4. Start the Backend

```powershell
uv run uvicorn backend.app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

## 5. Start the Frontend

Open another terminal:

```powershell
uv run streamlit run frontend/app.py
```

Open the Streamlit URL displayed in the terminal.

---

# Example Tickets

### Password Issue

```text
I forgot my password and cannot log in.
```

```text
Intent → passcode_forgotten
```

### Pending Payment

```text
My card payment is still pending. How long will it take?
```

```text
Intent → pending_card_payment
```

### Duplicate Transaction

```text
I was charged twice for the same transaction.
```

```text
Intent → transaction_charged_twice
```

### Lost Card

```text
I lost my card. What should I do?
```

```text
Intent → lost_or_stolen_card
```

### Account Deletion

```text
I want to delete my account permanently.
```

```text
Intent → terminate_account
```

This type of request can be escalated according to the configured escalation rules.

### Out-of-Scope Request

```text
What is the weather today?
```

```text
Result → Out-of-Scope
```

---

# Design Decisions

### Semantic Embeddings

Customer tickets can express the same issue using very different wording.

For example:

```text
"My payment hasn't completed."

"The payment is still processing."

"My transaction is stuck."
```

Semantic embeddings allow the system to capture the relationship between these expressions without depending only on exact keywords.

### Separate OOS Detection

An unsupported request should not be forced into one of the supported customer-support intents.

```text
Customer Ticket
      │
 ┌────┴────┐
 ▼         ▼
In-Domain  OOS
 │         │
 ▼         ▼
Intent     OOS
Model      Handling
```

### RAG

The generative model receives application-specific information retrieved from the knowledge base.

```text
Ticket
  ↓
Retrieve
  ↓
Relevant Knowledge
  ↓
Generate
```

This creates a more controlled response-generation workflow.

### Escalation

The system provides a human-support path when confidence is low, relevant knowledge is unavailable, or configured escalation conditions apply.

---

# Limitations

- Some closely related support intents remain difficult to distinguish.
- Retrieval does not always return a sufficiently relevant knowledge article.
- Response quality depends partly on the configured generative AI service.
- The system is designed around a fixed 77-intent support taxonomy.
- The current implementation is a portfolio/demonstration system rather than a production deployment connected to a real customer-support platform.

---

# Future Improvements

- Advanced retrieval and reranking models
- Automated regression testing
- Human-based response-quality evaluation
- Production monitoring and observability
- Authentication and role-based access control
- Cloud deployment
- Integration with real customer-support platforms

---

# Project Highlights

| | |
|---|---|
| **77** | Supported customer-support intents |
| **153** | Knowledge-base articles |
| **95.78%** | OOS detection accuracy |
| **92.21%** | Intent classification accuracy |
| **85.42%** | KB retrieval coverage |
| **91.46%** | Pipeline routing accuracy |

---

# Author

**Jeye Suriya**

AI / Software Engineering Project

---

## License

This project is intended for educational, portfolio, and demonstration purposes.#   A I - P o w e r e d - C u s t o m e r - S u p p o r t - - - T i c k e t - R e s o l u t i o n - S y s t e m  
 