from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
KB_PATH = BASE_DIR / "data" / "support_knowledge_base.csv"


ARTICLES = [
    {
        "kb_id": "KB145",
        "category": "Cards",
        "intent": "getting_virtual_card",
        "title": "Getting a Virtual Card",
        "problem": "The customer wants to know how to obtain a virtual card.",
        "symptoms": "Asks how to get, create, or access a virtual card.",
        "resolution_steps": "1. Open the cards section in the app.\n2. Select the option to create or access a virtual card.\n3. Follow the instructions shown in the app.",
        "additional_information": "Virtual card availability depends on the customer's account and supported features.",
        "escalation_condition": "Escalate if the virtual card option is unavailable despite the account being eligible.",
        "search_text": "getting virtual card get virtual card create virtual card obtain virtual card access virtual card how to get a virtual card"
    },
    {
        "kb_id": "KB146",
        "category": "Cards",
        "intent": "get_disposable_virtual_card",
        "title": "Getting a Disposable Virtual Card",
        "problem": "The customer wants to obtain a disposable virtual card.",
        "symptoms": "Asks how to get, create, or use a disposable virtual card.",
        "resolution_steps": "1. Open the cards section in the app.\n2. Select the disposable virtual card option if available.\n3. Follow the instructions to create or access the disposable card.",
        "additional_information": "Disposable virtual card availability depends on the account and supported features.",
        "escalation_condition": "Escalate if the disposable virtual card option should be available but cannot be accessed.",
        "search_text": "get disposable virtual card disposable card create disposable virtual card obtain disposable virtual card access disposable virtual card how to get disposable card"
    },
    {
        "kb_id": "KB147",
        "category": "Cards",
        "intent": "disposable_card_limits",
        "title": "Disposable Virtual Card Limits",
        "problem": "The customer wants to know about limitations or usage restrictions for disposable virtual cards.",
        "symptoms": "Asks about disposable card limits, restrictions, number of transactions, or where disposable cards can be used.",
        "resolution_steps": "1. Explain that disposable virtual cards have usage restrictions.\n2. Check the limits and supported transaction types shown for the disposable card.\n3. If a transaction is rejected, review whether it falls within the supported usage.",
        "additional_information": "Some merchants or transaction types may not support disposable virtual cards.",
        "escalation_condition": "Escalate if a customer reports an unexpected restriction or repeated rejection that is not explained by the documented limits.",
        "search_text": "disposable card limits disposable virtual card limitations restrictions usage limit transaction limit disposable card not supported merchant"
    },
    {
        "kb_id": "KB148",
        "category": "Cards",
        "intent": "virtual_card_not_working",
        "title": "Virtual Card Not Working",
        "problem": "The customer's virtual card is not working for a transaction.",
        "symptoms": "Virtual card is declined, does not work, or cannot be used for a payment.",
        "resolution_steps": "1. Check that the virtual card is active.\n2. Confirm that the merchant accepts the card type.\n3. Check for transaction restrictions or limits.\n4. Retry the transaction if appropriate.\n5. If the problem continues, review the transaction details.",
        "additional_information": "Some merchants or transaction types may not support virtual cards.",
        "escalation_condition": "Escalate if the virtual card remains unusable after checking activation, merchant support, and applicable restrictions.",
        "search_text": "virtual card not working virtual card declined virtual card does not work virtual card payment failed cannot use virtual card"
    },
]


def main():
    df = pd.read_csv(KB_PATH)

    existing_intents = set(df["intent"].astype(str))

    new_articles = [
        article
        for article in ARTICLES
        if article["intent"] not in existing_intents
    ]

    if not new_articles:
        print("No new articles to add.")
        return

    new_df = pd.DataFrame(new_articles)

    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(KB_PATH, index=False)

    print(f"Added {len(new_articles)} articles.")
    print(f"Total KB articles: {len(df)}")

    for article in new_articles:
        print(f"{article['kb_id']} -> {article['intent']}")


if __name__ == "__main__":
    main()