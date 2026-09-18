from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "support_knowledge_base.csv"

START_KB_ID = 123


PAYMENT_KB = [
    {
        "category": "Card Payments",
        "intent": "Refund_not_showing_up",
        "title": "Refund has not arrived",
        "problem": "A customer is waiting for a card payment refund that has not appeared in their account.",
        "symptoms": "Refund missing; refund has not arrived; waiting for a refund; refunded payment not showing.",
        "resolution_steps": "1. Check the original payment and refund details.\n2. Confirm that the refund was actually issued.\n3. Allow the expected processing time for the refund to appear.\n4. Contact support if the refund remains missing after the expected period.",
        "additional_information": "A refund may take time to appear after it has been issued.",
        "escalation_condition": "Escalate if a confirmed refund has not appeared after the expected processing period.",
    },
    {
        "category": "Card Payments",
        "intent": "declined_card_payment",
        "title": "Card payment was declined",
        "problem": "A customer attempted to make a card payment but the payment was declined.",
        "symptoms": "Card payment declined; card payment rejected; payment did not go through.",
        "resolution_steps": "1. Check the payment status and available transaction information.\n2. Confirm that the card is active and can be used for payments.\n3. Check the available balance and payment details.\n4. Retry the payment if appropriate or use another supported payment method.",
        "additional_information": "Card payments can be declined for different card, balance, merchant, or transaction reasons.",
        "escalation_condition": "Escalate repeated unexplained card payment declines or cases requiring transaction investigation.",
    },
    {
        "category": "Card Payments",
        "intent": "extra_charge_on_statement",
        "title": "Extra charge on statement",
        "problem": "A customer sees an additional or unexpected charge on their account statement.",
        "symptoms": "Extra charge; unexpected charge; additional amount on statement; charged more than expected.",
        "resolution_steps": "1. Check the transaction details and charged amount.\n2. Compare the charge with the original purchase or transaction.\n3. Check whether the additional amount is an applicable fee or adjustment.\n4. Contact support if the charge cannot be explained.",
        "additional_information": "An additional statement amount may represent a fee, adjustment, or other transaction-related charge.",
        "escalation_condition": "Escalate disputed or unexplained charges after the transaction details have been reviewed.",
    },
    {
        "category": "Card Payments",
        "intent": "pending_card_payment",
        "title": "Card payment is pending",
        "problem": "A card payment is still showing as pending.",
        "symptoms": "Card payment pending; payment still processing; card transaction has not completed.",
        "resolution_steps": "1. Check the payment transaction status.\n2. Confirm the merchant and payment amount.\n3. Allow the normal processing time for the card payment.\n4. Contact support if the payment remains pending beyond the expected period.",
        "additional_information": "A card payment can remain pending while the merchant or payment network completes processing.",
        "escalation_condition": "Escalate if the card payment remains pending beyond the expected processing period or requires transaction investigation.",
    },
    {
        "category": "Card Payments",
        "intent": "request_refund",
        "title": "Request a card payment refund",
        "problem": "A customer wants to request a refund for a card payment.",
        "symptoms": "I want a refund; request refund; get my money back from a card purchase; refund a card payment.",
        "resolution_steps": "1. Identify the card payment and merchant.\n2. Check whether the transaction is eligible for a refund.\n3. Follow the applicable refund process.\n4. Contact support if the refund cannot be requested through the available process.",
        "additional_information": "Refund availability can depend on the transaction and applicable merchant or support process.",
        "escalation_condition": "Escalate disputed refund requests or cases where a refund cannot be requested through the normal process.",
    },
    {
        "category": "Card Payments",
        "intent": "reverted_card_payment?",
        "title": "Card payment was reverted",
        "problem": "A card payment was reversed or returned after initially appearing as completed or authorised.",
        "symptoms": "Card payment reverted; payment reversed; payment returned; card payment disappeared or was reversed.",
        "resolution_steps": "1. Check the card payment transaction status and history.\n2. Confirm the original payment amount and merchant.\n3. Check whether the payment was reversed or reverted.\n4. Contact support if the reversal is unexpected or the transaction remains incorrect.",
        "additional_information": "A card payment can be reverted after initially appearing as authorised or completed.",
        "escalation_condition": "Escalate unexpected payment reversals or cases where the transaction outcome remains unclear.",
    },
    {
        "category": "Card Payments",
        "intent": "transaction_charged_twice",
        "title": "Transaction charged twice",
        "problem": "A customer believes the same transaction was charged more than once.",
        "symptoms": "Charged twice; duplicate transaction; same payment appears twice; duplicate card charge.",
        "resolution_steps": "1. Compare the duplicated transactions and their amounts.\n2. Check whether both transactions are completed or whether one is still pending.\n3. Allow temporary duplicate authorisations to resolve when applicable.\n4. Contact support if both charges remain completed and appear duplicated.",
        "additional_information": "Two similar card transactions can sometimes include a temporary authorisation and a completed payment.",
        "escalation_condition": "Escalate when duplicate completed charges remain after the normal processing period.",
    },
    {
        "category": "Direct Debit",
        "intent": "direct_debit_payment_not_recognised",
        "title": "Unrecognised direct debit payment",
        "problem": "A customer sees a direct debit payment they do not recognise.",
        "symptoms": "Unknown direct debit; unrecognised direct debit payment; direct debit I did not authorise.",
        "resolution_steps": "1. Check the direct debit transaction details.\n2. Confirm the merchant or organisation associated with the payment.\n3. Report the payment if the customer does not recognise or authorise it.\n4. Contact support for investigation of the unrecognised direct debit.",
        "additional_information": "An unrecognised direct debit may require investigation to determine its origin and authorisation.",
        "escalation_condition": "Escalate all reported unauthorised or unrecognised direct debit payments.",
    },
]


def build():
    print("SUPPORTAI PAYMENT KB BUILDER")
    print("Loading existing knowledge base...")

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Knowledge base not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print(f"Existing articles: {len(df)}")

    existing_intents = set(df["intent"].dropna().astype(str))

    new_rows = []
    next_id = START_KB_ID

    for article in PAYMENT_KB:
        intent = article["intent"]

        if intent in existing_intents:
            print(f"Skipping existing intent: {intent}")
            continue

        search_text = "\n".join(
            [
                article["title"],
                article["problem"],
                article["symptoms"],
                article["resolution_steps"],
                article["additional_information"],
                article["escalation_condition"],
            ]
        )

        new_rows.append(
            {
                "kb_id": f"KB{next_id:03d}",
                "category": article["category"],
                "intent": article["intent"],
                "title": article["title"],
                "problem": article["problem"],
                "symptoms": article["symptoms"],
                "resolution_steps": article["resolution_steps"],
                "additional_information": article["additional_information"],
                "escalation_condition": article["escalation_condition"],
                "search_text": search_text,
            }
        )

        next_id += 1

    if not new_rows:
        print("No new payment articles to add.")
        return

    updated_df = pd.concat(
        [df, pd.DataFrame(new_rows)],
        ignore_index=True,
    )

    updated_df.to_csv(DATA_PATH, index=False)

    print(f"Payment articles added: {len(new_rows)}")
    print(f"Updated articles: {len(updated_df)}")
    print("PAYMENT KB UPDATE COMPLETED")


if __name__ == "__main__":
    build()