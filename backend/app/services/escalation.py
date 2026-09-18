from typing import Optional


INTENT_CONFIDENCE_THRESHOLD = 0.60


class EscalationService:
    def __init__(
        self,
        intent_confidence_threshold=INTENT_CONFIDENCE_THRESHOLD
    ):
        self.intent_confidence_threshold = intent_confidence_threshold

    def check(
        self,
        ticket: str,
        intent: str,
        intent_confidence: float,
        escalation_condition: Optional[str] = None
    ):
        reasons = []

        # 1. Escalate when intent confidence is low
        if intent_confidence < self.intent_confidence_threshold:
            reasons.append(
                f"Low intent confidence: {intent_confidence:.2f}"
            )

        # 2. Escalate when a KB escalation condition applies
        if escalation_condition:
            if self._condition_applies(
                ticket,
                escalation_condition
            ):
                reasons.append(
                    f"KB escalation condition met: "
                    f"{escalation_condition}"
                )

        return {
            "should_escalate": len(reasons) > 0,
            "reasons": reasons,
            "intent": intent,
            "intent_confidence": intent_confidence,
            "escalation_condition": escalation_condition
        }

    def _condition_applies(self, ticket, condition):
        ticket_text = ticket.lower()
        condition_text = condition.lower()

        # Registered email access
        if "registered email" in condition_text:
            email_access_phrases = [
                "can't access my registered email",
                "cannot access my registered email",
                "can't access the registered email",
                "cannot access the registered email",
                "can't access my email",
                "cannot access my email",
                "lost access to my email",
                "don't have access to my email",
                "do not have access to my email",
                "no access to my email",
                "no longer have access to my email"
            ]

            if any(
                phrase in ticket_text
                for phrase in email_access_phrases
            ):
                return True

        # Account compromise
        if "account compromise" in condition_text:
            compromise_phrases = [
                "account hacked",
                "account compromised",
                "someone accessed my account",
                "someone has access to my account",
                "someone got into my account"
            ]

            if any(
                phrase in ticket_text
                for phrase in compromise_phrases
            ):
                return True

        # Unauthorized transaction/payment
        if (
            "unauthorized transaction" in condition_text
            or "unauthorized payment" in condition_text
        ):
            unauthorized_phrases = [
                "unauthorized transaction",
                "unauthorized payment",
                "payment wasn't mine",
                "payment was not mine",
                "someone used my card",
                "someone made a payment"
            ]

            if any(
                phrase in ticket_text
                for phrase in unauthorized_phrases
            ):
                return True

        return False


if __name__ == "__main__":
    service = EscalationService()

    test_cases = [
        {
            "ticket": "I forgot my password",
            "intent": "password_reset",
            "confidence": 0.90,
            "condition": (
                "Escalate if the customer cannot access "
                "the registered email or repeated resets fail."
            )
        },
        {
            "ticket": (
                "I forgot my password and I can't access "
                "my registered email."
            ),
            "intent": "password_reset",
            "confidence": 0.90,
            "condition": (
                "Escalate if the customer cannot access "
                "the registered email or repeated resets fail."
            )
        },
        {
            "ticket": "My card payment wasn't mine",
            "intent": "declined_card_payment",
            "confidence": 0.34,
            "condition": None
        }
    ]

    print("\nEscalation Validation\n")

    for case in test_cases:
        result = service.check(
            ticket=case["ticket"],
            intent=case["intent"],
            intent_confidence=case["confidence"],
            escalation_condition=case["condition"]
        )

        print(f"Ticket: {case['ticket']}")
        print(f"Intent: {result['intent']}")
        print(f"Confidence: {result['intent_confidence']:.2f}")
        print(f"Escalate: {result['should_escalate']}")

        if result["reasons"]:
            print("Reasons:")

            for reason in result["reasons"]:
                print(f"- {reason}")

        print("-" * 60)