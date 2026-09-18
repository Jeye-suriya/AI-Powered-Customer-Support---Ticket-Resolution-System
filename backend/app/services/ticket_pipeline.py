from sentence_transformers import SentenceTransformer

from backend.app.data.database import TicketDatabase
from backend.app.models.intent_classifier import IntentClassifier
from backend.app.models.oos_detector import OOSDetector
from backend.app.rag.generator import RAGGenerator
from backend.app.services.escalation import EscalationService

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
INTENT_CONFIDENCE_THRESHOLD = 0.60


class TicketPipeline:

    def __init__(self):
        print("Loading ticket resolution pipeline...")
        print("Loading shared embedding model...")

        self.encoder = SentenceTransformer(
            EMBEDDING_MODEL
        )

        self.oos_detector = OOSDetector(
            load_model=True,
            encoder=self.encoder
        )

        self.intent_classifier = IntentClassifier(
            load_model=True,
            encoder=self.encoder
        )

        self.rag_generator = RAGGenerator(
            encoder=self.encoder
        )

        self.escalation_service = EscalationService(
            intent_confidence_threshold=INTENT_CONFIDENCE_THRESHOLD
        )

        self.database = TicketDatabase()

        print("Pipeline loaded successfully.")

    def _save_result(self, result):
        ticket_id = self.database.save_ticket(result)
        result["ticket_id"] = ticket_id
        return result

    def process(self, ticket: str):

        if not ticket or not ticket.strip():
            return {
                "ticket": ticket,
                "status": "error",
                "message": "Ticket cannot be empty."
            }

        ticket = ticket.strip()

        # 1. OOS Detection

        oos_result = self.oos_detector.predict(ticket)

        if oos_result["is_oos"]:
            result = {
                "ticket": ticket,
                "status": "out_of_domain",
                "oos": {
                    "is_oos": True,
                    "confidence": oos_result["confidence"]
                },
                "intent": None,
                "response": (
                    "This request is outside the supported customer "
                    "support domain. Please contact the appropriate "
                    "support team for further assistance."
                ),
                "sources": [],
                "escalation": {
                    "should_escalate": False,
                    "reasons": []
                }
            }

            return self._save_result(result)

        # 2. Intent Classification

        intent_result = self.intent_classifier.predict(ticket)

        intent = intent_result["intent"]
        intent_confidence = intent_result["confidence"]

        # 3. Low-confidence intent

        if intent_confidence < INTENT_CONFIDENCE_THRESHOLD:

            escalation_result = self.escalation_service.check(
                ticket=ticket,
                intent=intent,
                intent_confidence=intent_confidence,
                escalation_condition=None
            )

            result = {
                "ticket": ticket,
                "status": "escalate",
                "oos": {
                    "is_oos": False,
                    "confidence": oos_result["confidence"]
                },
                "intent": {
                    "name": intent,
                    "confidence": intent_confidence
                },
                "response": (
                    "I’m unable to confidently determine the "
                    "specific issue. Please contact support for "
                    "further assistance."
                ),
                "sources": [],
                "escalation": escalation_result
            }

            return self._save_result(result)

        # 4. RAG Response Generation

        rag_result = self.rag_generator.generate(
            ticket=ticket,
            intent=intent
        )

        # 5. Validate retrieved KB sources

        sources = rag_result["sources"]

        if not sources:

            escalation_result = self.escalation_service.check(
                ticket=ticket,
                intent=intent,
                intent_confidence=intent_confidence,
                escalation_condition=None
            )

            escalation_result["reasons"].append(
                "No sufficiently relevant knowledge base article found."
            )

            escalation_result["should_escalate"] = True

            result = {
                "ticket": ticket,
                "status": "escalate",
                "oos": {
                    "is_oos": False,
                    "confidence": oos_result["confidence"]
                },
                "intent": {
                    "name": intent,
                    "confidence": intent_confidence
                },
                "response": (
                    "I’m unable to find a sufficiently relevant "
                    "support solution for this issue. Please "
                    "contact support for further assistance."
                ),
                "sources": [],
                "escalation": escalation_result
            }

            return self._save_result(result)

        # 6. KB/RAG escalation decision

        requires_escalation = rag_result.get(
            "requires_escalation",
            False
        )

        escalation_condition = sources[0].get(
            "escalation_condition"
        )

        # 7. Escalation Check

        escalation_result = self.escalation_service.check(
            ticket=ticket,
            intent=intent,
            intent_confidence=intent_confidence,
            escalation_condition=(
                escalation_condition
                if requires_escalation
                else None
            )
        )

        # Ensure the RAG escalation decision is reflected
        # in the final pipeline status.

        if requires_escalation:
            escalation_result["should_escalate"] = True

            if not escalation_result["reasons"]:
                escalation_result["reasons"].append(
                    "Knowledge base escalation condition applies."
                )

        # 8. Final status

        status = (
            "escalate"
            if escalation_result["should_escalate"]
            else "resolved"
        )

        result = {
            "ticket": ticket,
            "status": status,
            "oos": {
                "is_oos": False,
                "confidence": oos_result["confidence"]
            },
            "intent": {
                "name": intent,
                "confidence": intent_confidence
            },
            "response": rag_result["response"],
            "sources": sources,
            "escalation": escalation_result
        }

        return self._save_result(result)


if __name__ == "__main__":

    pipeline = TicketPipeline()

    test_cases = [
        "I forgot my password and cannot log in.",
        "My card payment wasn't mine.",
        "My transfer is still pending.",
        "I want to delete my account.",
        "What is the weather today?"
    ]

    print("\nTicket Pipeline Validation\n")

    for ticket in test_cases:

        print(f"Ticket: {ticket}")

        result = pipeline.process(ticket)

        print(
            f"Ticket ID: "
            f"{result.get('ticket_id', 'N/A')}"
        )

        print(
            f"Status: "
            f"{result['status']}"
        )

        if result.get("intent"):
            print(
                f"Intent: "
                f"{result['intent']['name']}"
            )

            print(
                f"Intent confidence: "
                f"{result['intent']['confidence']:.4f}"
            )

        print(
            f"Response: "
            f"{result.get('response')}"
        )

        print(
            f"Escalate: "
            f"{result['escalation']['should_escalate']}"
        )

        if result["escalation"]["reasons"]:
            print("Reasons:")

            for reason in result["escalation"]["reasons"]:
                print(f"- {reason}")

        print("-" * 70)