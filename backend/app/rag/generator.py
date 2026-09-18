import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from sentence_transformers import SentenceTransformer

from backend.app.retrieval.knowledge_base import KnowledgeBase

BASE_DIR = Path(__file__).resolve().parents[3]

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class RAGGenerator:
    def __init__(self, encoder=None):
        self.encoder = encoder or SentenceTransformer(
            EMBEDDING_MODEL
        )

        self.knowledge_base = KnowledgeBase(
            encoder=self.encoder
        )

    def generate(self, ticket, intent):
        results = self.knowledge_base.search(
            query=ticket,
            intent=intent,
            top_k=3
        )

        if not results:
            return {
                "response": (
                    "I’m unable to find a relevant support article "
                    "for this issue. Please contact support for "
                    "further assistance."
                ),
                "sources": [],
                "requires_escalation": True
            }

        context = "\n\n".join(
            [
                f"KB ID: {result['kb_id']}\n"
                f"Intent: {result['intent']}\n"
                f"Title: {result['title']}\n"
                f"Information:\n{result['document']}\n"
                f"Escalation condition:\n"
                f"{result['escalation_condition']}"
                for result in results
            ]
        )

        prompt = f"""
You are a customer support assistant.

Your task is to answer the customer's support ticket using ONLY
the information provided in the knowledge base context.

Customer ticket:
{ticket}

Predicted intent:
{intent}

Knowledge base context:
{context}

Rules:
1. Use only information from the knowledge base context.
2. Do not invent troubleshooting steps, policies, fees, timelines,
   or guarantees.
3. Give clear and concise instructions to the customer.
4. If an escalation condition clearly applies to the customer's
   specific situation, explain that the issue needs to be
   escalated to support.
5. Do not say that escalation is required merely because an
   escalation condition exists. The condition must actually apply
   to the customer's situation.
6. Do not mention embeddings, vector databases, retrieval, or the
   knowledge base to the customer.
7. If the provided context does not contain enough information,
   say that further support is required.
8. Do not claim that an action has been completed unless the
   context explicitly says it has been completed.

Return ONLY the customer-facing response.
"""

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
        except errors.APIError as error:
            print(
                f"Gemini API error while generating response: "
                f"{error}"
            )

            return {
                "response": (
                    "Our automated support service is temporarily "
                    "unavailable. Please contact support for "
                    "further assistance."
                ),
                "sources": [],
                "requires_escalation": True
            }

        response_text = response.text.strip()

        escalation_condition = results[0].get(
            "escalation_condition"
        )

        requires_escalation = False

        if escalation_condition:
            escalation_check_prompt = f"""
Determine whether the escalation condition applies to the
customer's specific ticket.

Customer ticket:
{ticket}

Escalation condition:
{escalation_condition}

Respond with exactly one word:
YES
or
NO
"""

            try:
                escalation_check = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=escalation_check_prompt
                )

                requires_escalation = (
                    escalation_check.text.strip().upper() == "YES"
                )

            except errors.APIError as error:
                print(
                    f"Gemini API error while checking escalation: "
                    f"{error}"
                )

                return {
                    "response": (
                        "Our automated support service is unable "
                        "to complete this request right now. "
                        "Please contact support for further "
                        "assistance."
                    ),
                    "sources": [],
                    "requires_escalation": True
                }

        return {
            "response": response_text,
            "sources": [
                {
                    "kb_id": result["kb_id"],
                    "intent": result["intent"],
                    "title": result["title"],
                    "escalation_condition": result.get(
                        "escalation_condition"
                    ),
                    "similarity": result.get(
                        "similarity"
                    )
                }
                for result in results
            ],
            "requires_escalation": requires_escalation
        }


if __name__ == "__main__":
    generator = RAGGenerator()

    ticket = "I forgot my password and cannot log in."
    intent = "passcode_forgotten"

    result = generator.generate(
        ticket=ticket,
        intent=intent
    )

    print("\nGenerated Response:\n")
    print(result["response"])

    print(
        f"\nRequires escalation: "
        f"{result['requires_escalation']}"
    )

    print("\nSources:\n")

    for source in result["sources"]:
        print(
            f"{source['kb_id']} - "
            f"{source['intent']} - "
            f"{source['title']}"
        )

        print(
            f"Similarity: "
            f"{source.get('similarity')}"
        )

        print(
            f"Escalation condition: "
            f"{source['escalation_condition']}"
        )