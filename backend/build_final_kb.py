from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
KB_PATH = BASE_DIR / "data" / "support_knowledge_base.csv"


ARTICLES = [
    {
        "kb_id": "KB149",
        "category": "Cards & Payments",
        "intent": "apple_pay_or_google_pay",
        "title": "Apple Pay and Google Pay",
        "problem": "The customer wants to know whether they can use the service with Apple Pay or Google Pay.",
        "symptoms": "Asks about adding a card to Apple Pay or Google Pay or using these mobile payment services.",
        "resolution_steps": "1. Check whether the card and account support the requested mobile payment service.\n2. Open the relevant wallet application.\n3. Follow the wallet's instructions to add the supported card.\n4. Complete any verification requested by the wallet.",
        "additional_information": "Availability can depend on the card, country, device, and supported wallet features.",
        "escalation_condition": "Escalate if an eligible card cannot be added to the supported mobile wallet after following the setup instructions.",
        "search_text": "Apple Pay Google Pay mobile wallet add card to Apple Pay add card to Google Pay use card with Apple Pay Google Wallet"
    },
    {
        "kb_id": "KB150",
        "category": "Cards & Cash",
        "intent": "atm_support",
        "title": "ATM Support",
        "problem": "The customer wants to know about ATM availability and cash withdrawal support.",
        "symptoms": "Asks whether they can withdraw cash from an ATM or which ATMs can be used.",
        "resolution_steps": "1. Use a supported ATM that accepts the card.\n2. Insert or tap the card as supported by the ATM.\n3. Select the cash withdrawal option.\n4. Follow the ATM instructions and complete the transaction.",
        "additional_information": "ATM availability, fees, and supported features can vary by location and ATM provider.",
        "escalation_condition": "Escalate if a supported ATM repeatedly rejects the card or a cash withdrawal issue cannot be resolved.",
        "search_text": "ATM support cash withdrawal ATM availability which ATM can I use withdraw cash cash machine supported ATM"
    },
    {
        "kb_id": "KB151",
        "category": "Account & Availability",
        "intent": "country_support",
        "title": "Supported Countries",
        "problem": "The customer wants to know whether the service is available in a particular country.",
        "symptoms": "Asks whether they can use the service from a specific country or which countries are supported.",
        "resolution_steps": "1. Check whether the customer's country is supported.\n2. Review the current supported-country information for the relevant service.\n3. If the country is unsupported, explain that the service is not currently available there.",
        "additional_information": "Availability can vary by product and may change over time.",
        "escalation_condition": "Escalate if a customer in a supported country cannot access a service that should be available to them.",
        "search_text": "country support supported countries service available country is my country supported countries where can I use the service availability by country"
    },
    {
        "kb_id": "KB152",
        "category": "Cards & Top Up",
        "intent": "supported_cards_and_currencies",
        "title": "Supported Cards and Currencies",
        "problem": "The customer wants to know which cards and currencies are supported for a card-related transaction or top-up.",
        "symptoms": "Asks which cards, card types, or currencies can be used.",
        "resolution_steps": "1. Check whether the customer's card type is supported.\n2. Check whether the selected currency is supported.\n3. Use a supported card and currency for the transaction.",
        "additional_information": "Supported cards and currencies can depend on the specific transaction or top-up method.",
        "escalation_condition": "Escalate if a card or currency that should be supported is rejected unexpectedly.",
        "search_text": "supported cards currencies supported card types supported currencies which cards can I use which currencies can I use card and currency support"
    },
    {
        "kb_id": "KB153",
        "category": "Account Funding",
        "intent": "transfer_into_account",
        "title": "Transfer Money Into the Account",
        "problem": "The customer wants to know how to transfer money into their account.",
        "symptoms": "Asks how to add money by bank transfer, make a transfer into their account, or find the details needed to receive a transfer.",
        "resolution_steps": "1. Open the account's bank transfer or add-money section.\n2. Obtain the account details required for the transfer.\n3. Initiate the bank transfer from the sending bank.\n4. Use the required reference or transfer information when instructed.\n5. Wait for the transfer to be processed.",
        "additional_information": "Transfer processing time depends on the sending bank, transfer type, and supported payment rails.",
        "escalation_condition": "Escalate if money was sent to the correct account details but has not arrived within the expected processing period.",
        "search_text": "transfer into account add money by bank transfer transfer money into my account receive bank transfer account transfer how to fund account"
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