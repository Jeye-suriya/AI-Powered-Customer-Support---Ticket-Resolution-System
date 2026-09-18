from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
KB_PATH = BASE_DIR / "data" / "support_knowledge_base.csv"


ARTICLES = [
    {
        "kb_id": "KB141",
        "category": "Currency & Exchange",
        "intent": "exchange_rate",
        "title": "Exchange Rate",
        "problem": "The customer wants to know the current exchange rate or the rate that will be applied to a currency exchange.",
        "symptoms": "Asks about exchange rates, conversion rates, or how much one currency is worth in another currency.",
        "resolution_steps": "1. Explain that exchange rates vary over time.\n2. Ask the customer to check the current rate shown in the app before confirming an exchange.\n3. Explain that the displayed rate is the applicable rate for the transaction.",
        "additional_information": "The exact rate depends on the currencies and the time of the exchange.",
        "escalation_condition": "Escalate if the customer disputes the applied exchange rate after providing transaction details.",
        "search_text": "exchange rate current exchange rate currency conversion rate rate for converting money how much one currency is worth another currency"
    },
    {
        "kb_id": "KB142",
        "category": "Currency & Exchange",
        "intent": "exchange_charge",
        "title": "Exchange Fees",
        "problem": "The customer wants to know whether a fee or charge applies when exchanging currencies.",
        "symptoms": "Asks about exchange fees, currency conversion charges, or being charged for exchanging currencies.",
        "resolution_steps": "1. Explain that applicable exchange charges depend on the transaction and currencies involved.\n2. Ask the customer to review the exchange details shown before confirming the transaction.\n3. If a charge has already appeared, review the transaction details.",
        "additional_information": "Charges should be checked against the exchange transaction details shown in the app.",
        "escalation_condition": "Escalate if the customer disputes an exchange charge that cannot be explained from the transaction details.",
        "search_text": "exchange charge exchange fee currency conversion fee charged for exchanging money currency exchange cost conversion charge"
    },
    {
        "kb_id": "KB143",
        "category": "Currency & Exchange",
        "intent": "exchange_via_app",
        "title": "Exchange Currency in the App",
        "problem": "The customer wants to know how to exchange one currency for another using the app.",
        "symptoms": "Asks how to exchange currencies, convert money, or perform a currency exchange in the app.",
        "resolution_steps": "1. Open the currency or exchange section in the app.\n2. Select the currency to exchange from and the currency to receive.\n3. Enter the amount.\n4. Review the exchange rate and transaction details.\n5. Confirm the exchange.",
        "additional_information": "The available currencies and applicable rate are shown during the exchange process.",
        "escalation_condition": "Escalate if the customer cannot complete an exchange because of an account or technical problem.",
        "search_text": "exchange currency via app how to exchange currencies convert money in app currency conversion exchange currencies using application"
    },
    {
        "kb_id": "KB144",
        "category": "Currency & Exchange",
        "intent": "fiat_currency_support",
        "title": "Supported Fiat Currencies",
        "problem": "The customer wants to know which fiat currencies are supported by the service.",
        "symptoms": "Asks whether a particular currency is supported or which currencies are available.",
        "resolution_steps": "1. Check whether the requested fiat currency is supported.\n2. Review the supported currency list in the app.\n3. If the currency is not available, explain that it cannot currently be used through the relevant feature.",
        "additional_information": "Supported fiat currencies can depend on the specific service or transaction.",
        "escalation_condition": "Escalate if the customer believes a supported currency is incorrectly unavailable in their account.",
        "search_text": "fiat currency support supported currencies supported fiat currencies available currency is my currency supported which currencies are supported"
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