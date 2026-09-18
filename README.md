SupportAI

AI-Powered Customer Support Ticket Resolution System

An end-to-end AI customer-support automation system that understands customer tickets, detects unsupported requests, classifies customer intent, retrieves relevant knowledge, generates grounded responses using RAG, and intelligently routes uncertain or sensitive cases for human support.

77 Support Intents · 153 Knowledge Articles · 92.21% Intent Accuracy · 95.78% OOS Accuracy

Repository:
https://github.com/Jeye-suriya/AI-Powered-Customer-Support---Ticket-Resolution-System

Overview

SupportAI is an AI-powered customer-support ticket resolution system designed to automate the support workflow while maintaining a controlled path to human escalation.

Instead of sending every ticket directly to a generative AI model, the system uses a multi-stage pipeline:

Customer Ticket
      │
      ▼
Text Preprocessing
      │
      ▼
Out-of-Scope Detection
      │
      ├──────────────► OOS Response
      │
      ▼
Intent Classification
      │
      ▼
Knowledge Base Retrieval
      │
      ▼
Intent-Aware Reranking
      │
      ▼
RAG Response Generation
      │
      ▼
Escalation Decision
      │
      ├──────────────► Escalated
      │
      ▼
   Resolved
      │
      ▼
SQLite Ticket Storage

The project combines semantic machine learning, vector retrieval, retrieval-augmented generation, generative AI, confidence-based routing, and persistent ticket management.

Key Features

Intelligent Ticket Understanding

Supports 77 customer-support intents

Understands natural-language customer requests using semantic embeddings

Separates unsupported requests from supported customer-support tickets

Out-of-Scope Detection

Detects requests outside the supported support domain

Prevents unrelated requests from being incorrectly assigned to a support intent

Uses MiniLM embeddings with Logistic Regression

Knowledge-Grounded Retrieval

153 structured support articles

Semantic vector search using ChromaDB

Cosine similarity retrieval

Intent-aware reranking

Retrieval-Augmented Generation

Retrieves relevant support information before generation

Uses retrieved knowledge as context for Google Gemini

Produces customer-facing responses grounded in the knowledge base

Confidence-Based Escalation

Tickets can be escalated when:

Intent confidence is below the configured threshold

No sufficiently relevant knowledge article is found

A configured escalation condition applies

The AI generation service fails

Persistent Ticket Management

SQLite ticket storage

Ticket history

Individual ticket lookup

REST API access

Web Interface

The Streamlit application provides:

Dashboard

New Ticket

Ticket History

System Status

Architecture

┌─────────────────────────────┐
│       Customer / Agent      │
│           Ticket            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Streamlit UI         │
│  Ticket Submission/History  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│           FastAPI           │
│          REST API           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Ticket Pipeline       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     OOS Detection Model     │
│ MiniLM + Logistic Regression│
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Intent Classification    │
│ MiniLM + Logistic Regression│
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Semantic Retrieval      │
│          ChromaDB           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Intent-Aware Reranking  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│             RAG             │
│          Gemini             │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Escalation Service     │
│   Confidence + Rule Checks  │
└──────────────┬──────────────┘
               │
          ┌────┴─────┐
          ▼          ▼
     ┌─────────┐ ┌───────────┐
     │ Resolved│ │ Escalated │
     └────┬────┘ └─────┬─────┘
          │            │
          └─────┬──────┘
                ▼
┌─────────────────────────────┐
│            SQLite           │
│        Ticket History       │
└─────────────────────────────┘

AI Pipeline

1. Out-of-Scope Detection

The first stage determines whether an incoming request belongs to the supported customer-support domain.

Model

Component

Implementation

Embedding Model

all-MiniLM-L6-v2

Embedding Dimension

384

Classifier

Logistic Regression

Class Weight

Balanced

Evaluation Accuracy: 95.78%

Example:

Customer:
"What is the weather today?"

Result:
Out-of-Scope

2. Intent Classification

In-domain tickets are classified into one of 77 customer-support intents.

Model

Component

Implementation

Embedding Model

all-MiniLM-L6-v2

Classifier

Logistic Regression

Number of Intents

77

Training Dataset

data/train.csv

Test Dataset

data/test.csv

Test Accuracy: 92.21%

Example:

Customer:
"My card payment is still pending."

Prediction:
pending_card_payment

3. Knowledge Base

SupportAI uses a structured knowledge base as the information source for retrieval and response generation.

Current size: 153 support articles

Each article contains:

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

Source:

data/support_knowledge_base.csv

4. Semantic Retrieval

Knowledge-base articles are converted into semantic embeddings using:

all-MiniLM-L6-v2

The embeddings are stored in:

ChromaDB

Retrieval workflow:

Customer Ticket
      ↓
Semantic Embedding
      ↓
ChromaDB Vector Search
      ↓
Candidate Knowledge Articles

The system uses cosine similarity to identify semantically related support articles.

5. Intent-Aware Reranking

Semantic similarity alone can return articles that are linguistically similar but belong to a different support intent.

SupportAI therefore combines semantic similarity with the predicted intent:

Semantic Similarity
        +
Predicted Intent Match
        ↓
Final Ranking

The predicted intent receives an additional ranking bonus when it matches the intent associated with a knowledge-base article.

Retrieval Evaluation

Metric

Result

Retrieval Coverage

85.42%

Top-1 Intent Accuracy

71.59%

Top-3 Intent Recall

74.29%

Mean Reciprocal Rank

85.27%

Average Top Similarity

59.74%

6. Retrieval-Augmented Generation

After retrieval, relevant knowledge-base content is provided to Google Gemini as context.

Customer Ticket
       │
       ▼
Predicted Intent
       │
       ▼
Relevant KB Articles
       │
       ▼
Context Construction
       │
       ▼
Google Gemini
       │
       ▼
Customer Response

The generation stage is designed to:

Use retrieved support information

Generate a clear customer-facing response

Avoid unsupported claims

Follow available resolution information

Consider applicable escalation conditions

7. Escalation

SupportAI does not force every ticket into automatic resolution.

The escalation layer considers:

Low Intent Confidence
        OR
No Relevant KB Article
        OR
Configured Escalation Condition
        OR
AI Service Failure

Current intent confidence threshold:

0.60

Example:

Ticket:
"I want to delete my account permanently."

Intent:
terminate_account

Result:
Escalated according to configured escalation rules.

Technology Stack

Layer

Technology

Language

Python 3.12

Backend

FastAPI

Frontend

Streamlit

API Validation

Pydantic

Machine Learning

Scikit-learn

Embeddings

Sentence Transformers

Embedding Model

all-MiniLM-L6-v2

Classifier

Logistic Regression

Vector Database

ChromaDB

Generative AI

Google Gemini

Database

SQLite

Package Manager

uv

Version Control

Git / GitHub

Project Structure

AI-Powered-Customer-Support---Ticket-Resolution-System/
│
├── backend/
│   ├── app/
│   │   ├── data/
│   │   │   ├── __init__.py
│   │   │   ├── audit.py
│   │   │   ├── database.py
│   │   │   └── preprocess.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── intent_classifier.py
│   │   │   └── oos_detector.py
│   │   │
│   │   ├── retrieval/
│   │   │   └── knowledge_base.py
│   │   │
│   │   ├── rag/
│   │   │   └── generator.py
│   │   │
│   │   ├── services/
│   │   │   ├── escalation.py
│   │   │   └── ticket_pipeline.py
│   │   │
│   │   ├── api/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── evaluate_pipeline.py
│   ├── analyze_kb_coverage.py
│   ├── analyze_kb_intents.py
│   ├── analyze_kb_taxonomy.py
│   ├── analyze_intent_examples.py
│   ├── analyze_topup_intents.py
│   ├── analyze_intent_confidence.py
│   ├── analyze_intent_threshold.py
│   │
│   ├── build_card_kb.py
│   ├── build_transfer_kb.py
│   ├── build_topup_cash_kb.py
│   ├── build_payment_kb.py
│   ├── build_identity_kb.py
│   ├── build_exchange_kb.py
│   ├── build_virtual_card_kb.py
│   └── build_final_kb.py
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
│   ├── oos/
│   │   ├── oos_detector.joblib
│   │   └── threshold.json
│   └── vector_db/
│
├── frontend/
│   └── app.py
│
├── src/
│   └── ai_powered_customer_support_ticket_resolution_system/
│       └── __init__.py
│
├── .streamlit/
│   └── config.toml
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md

Dataset

The project uses multiple data sources for model development, evaluation, and knowledge-base construction.

Customer Support Intent Dataset

Training Dataset

data/train.csv

10,003 samples

77 intents

Columns:

text

category

Test Dataset

data/test.csv

3,080 samples

77 intents

Columns:

text

category

The test set is kept separate from training and validation analysis.

OOS Dataset

Dedicated out-of-scope and in-domain data are used for OOS detection.

OOS Training Samples: 100
OOS Validation Samples: 100
OOS Test Samples: 1,000

In-Domain Training Samples: 10,003
In-Domain Test Samples: 3,080

The OOS detector is evaluated using the held-out OOS test set.

Knowledge Base Dataset

data/support_knowledge_base.csv

Current size:

153 knowledge articles

The knowledge base provides coverage across the 77 supported customer-support intents.

Model Artifacts

Trained model artifacts are stored under:

models/

Intent Classifier

models/intent/intent_classifier.joblib

Pipeline:

Sentence Transformer
        ↓
all-MiniLM-L6-v2
        ↓
384-dimensional embeddings
        ↓
Logistic Regression

OOS Detector

models/oos/oos_detector.joblib

Pipeline:

Sentence Transformer
        ↓
all-MiniLM-L6-v2
        ↓
384-dimensional embeddings
        ↓
Logistic Regression

Vector Database

models/vector_db/

Contains the persistent ChromaDB vector store used for knowledge-base retrieval.

Shared Embedding Model

The pipeline uses a single shared instance of:

all-MiniLM-L6-v2

The same encoder is passed to:

OOS Detector

Intent Classifier

Knowledge Base Retriever

RAG Generator

This avoids repeatedly loading the same embedding model during application startup.

REST API

SupportAI exposes a REST API through FastAPI.

Health Check

GET /api/health

Example response:

{
  "status": "healthy"
}

Process Ticket

POST /api/tickets

Request:

{
  "ticket": "I forgot my password and cannot log in."
}

The API returns information including:

Ticket ID

Predicted intent

Intent confidence

AI-generated response

Retrieved sources

Escalation status

Escalation reasons

Ticket status

Ticket History

GET /api/tickets

Returns previously processed tickets stored in SQLite.

Individual Ticket

GET /api/tickets/{ticket_id}

Returns a specific stored ticket.

API Documentation

When the backend is running:

http://127.0.0.1:8000/docs

FastAPI provides interactive API documentation through Swagger UI.

Frontend

The web interface is built with Streamlit.

The application provides:

Dashboard

New Ticket

Ticket History

System Status

The New Ticket interface allows users to submit customer-support requests and view:

Detected intent

Confidence

AI response

Knowledge sources

Escalation status

Ticket ID

Ticket History retrieves previously processed tickets from the SQLite database.

Database

SupportAI uses SQLite for persistent ticket storage.

Database:

data/tickets.db

Processed tickets remain available after restarting the backend or frontend.

Evaluation

The system evaluates individual components rather than reporting a single combined accuracy.

Component

Metric

Result

OOS Detector

Accuracy

95.78%

Intent Classifier

Accuracy

92.21%

KB Retrieval

Coverage

85.42%

KB Retrieval

Top-1 Intent Accuracy

71.59%

KB Retrieval

Top-3 Intent Recall

74.29%

KB Retrieval

Mean Reciprocal Rank

85.27%

KB Retrieval

Average Top Similarity

59.74%

Pipeline Routing

Accuracy

91.46%

These metrics represent different stages of the system and should not be interpreted as one overall end-to-end response-quality score.

Running the Evaluation

From the project root:

uv run python -m backend.evaluate_pipeline

The evaluation covers:

OOS Detection
Intent Classification
Knowledge-Base Retrieval
Pipeline Routing

Getting Started

Requirements

Python 3.12+

uv

Google Gemini API access

1. Clone the Repository

git clone https://github.com/Jeye-suriya/AI-Powered-Customer-Support---Ticket-Resolution-System.git
cd AI-Powered-Customer-Support---Ticket-Resolution-System

2. Install Dependencies

uv sync

3. Configure Gemini API

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here

Never commit API keys or other secrets to GitHub.

4. Start the Backend

uv run uvicorn backend.app.main:app --reload

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

5. Start the Frontend

Open another terminal in the project root:

uv run streamlit run frontend/app.py

Open the Streamlit URL displayed in the terminal.

Example Tickets

Password Issue

I forgot my password and cannot log in.

Intent → passcode_forgotten

Pending Payment

My card payment is still pending. How long will it take?

Intent → pending_card_payment

Duplicate Transaction

I was charged twice for the same transaction.

Intent → transaction_charged_twice

Lost Card

I lost my card. What should I do?

Intent → lost_or_stolen_card

Account Deletion

I want to delete my account permanently.

Intent → terminate_account

This type of request can be escalated according to the configured escalation rules.

Out-of-Scope Request

What is the weather today?

Result → Out-of-Scope

Design Decisions

Semantic Embeddings

Customer-support tickets can express the same issue using very different wording.

For example:

"My payment hasn't completed."

"The payment is still processing."

"My transaction is stuck."

Semantic embeddings allow these variations to be represented in a shared semantic space.

Separate OOS Detection

An unsupported request should not be forced into a known support category.

Ticket
  │
  ├── OOS ──────────► OOS Handling
  │
  └── In-Domain
          │
          ▼
      Intent Model

Knowledge-Grounded RAG

The generative model receives application-specific information retrieved from the knowledge base.

Ticket
  ↓
Retrieve
  ↓
Relevant Knowledge
  ↓
Generate

This provides a more controlled response-generation workflow.

Intent-Aware Retrieval

Semantic similarity and intent classification provide complementary information.

Semantic Similarity
        +
Intent Match
        ↓
Reranked Results

Human Escalation

The system provides a human-support path when:

Intent confidence is low

Relevant knowledge cannot be found

Configured escalation conditions apply

AI generation fails

Production-Oriented Considerations

The project includes several controls intended to make the architecture closer to a real support automation system:

Input validation using Pydantic

Maximum ticket length validation

REST API separation

Persistent ticket storage

Confidence-based routing

Out-of-scope detection

Knowledge-grounded generation

Escalation rules

Shared embedding model instance

Persistent vector database

Separate training and test datasets

Validation-based threshold analysis

Structured model artifacts

Limitations

The current system is a portfolio and demonstration implementation rather than a production deployment connected to a real customer-support platform.

Current limitations include:

Closely related support intents can still be difficult to distinguish.

Retrieval coverage is not 100%.

Some tickets may not have sufficiently relevant knowledge articles.

Generated response quality depends partly on the configured Gemini service.

The system uses a fixed 77-intent support taxonomy.

The current evaluation does not include human-rated response quality.

Authentication and role-based access control are not implemented.

Production observability and monitoring are not included.

Future Improvements

Potential future extensions include:

Advanced cross-encoder reranking

Improved retrieval evaluation

Automated regression testing

Human-based response-quality evaluation

Response hallucination evaluation

Production monitoring

Logging and observability

Authentication

Role-based access control

Cloud deployment

Customer-support platform integration

Human-agent feedback loops

Continuous model evaluation

Project Highlights

Capability

Result

Supported Intents

77

Knowledge Articles

153

OOS Detection Accuracy

95.78%

Intent Classification Accuracy

92.21%

KB Retrieval Coverage

85.42%

KB Top-1 Intent Accuracy

71.59%

KB Top-3 Intent Recall

74.29%

KB MRR

85.27%

Pipeline Routing Accuracy

91.46%

Repository

https://github.com/Jeye-suriya/AI-Powered-Customer-Support---Ticket-Resolution-System

Author

Jeye Suriya

AI / Software Engineering Project

License

This project is intended for educational, portfolio, and demonstration purposes.
