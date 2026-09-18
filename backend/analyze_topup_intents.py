from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
TRAIN_PATH = BASE_DIR / "data" / "train.csv"


KEYWORDS = [
    "top_up",
    "topping_up",
    "cash_withdrawal",
    "cash_or_cheque",
    "cash",
    "automatic_top_up",
]


def main():
    df = pd.read_csv(TRAIN_PATH)

    intents = sorted(df["category"].dropna().unique())

    selected = [
        intent
        for intent in intents
        if any(keyword in intent.lower() for keyword in KEYWORDS)
    ]

    print(f"Total intents in training data: {len(intents)}")
    print(f"Matching intents: {len(selected)}")
    print()

    for intent in selected:
        examples = (
            df.loc[df["category"] == intent, "text"]
            .dropna()
            .astype(str)
            .head(5)
            .tolist()
        )

        print("=" * 70)
        print(f"INTENT: {intent}")
        print("=" * 70)

        for index, example in enumerate(examples, start=1):
            print(f"{index}. {example}")

        print()


if __name__ == "__main__":
    main()