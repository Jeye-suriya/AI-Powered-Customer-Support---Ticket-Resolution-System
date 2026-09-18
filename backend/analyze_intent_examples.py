import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "train.csv"

EXAMPLES_PER_INTENT = 5


# ============================================================
# LOAD DATA
# ============================================================

def load_training_data():
    df = pd.read_csv(DATA_PATH)

    df = df.dropna(
        subset=["text", "category"]
    )

    return df


# ============================================================
# EXTRACT REPRESENTATIVE EXAMPLES
# ============================================================

def extract_examples(df):
    grouped = (
        df.groupby("category", sort=True)
        .head(EXAMPLES_PER_INTENT)
    )

    return grouped


# ============================================================
# DISPLAY EXAMPLES
# ============================================================

def print_examples(grouped):
    intents = grouped["category"].unique()

    print("\n" + "=" * 80)
    print("CLASSIFIER INTENT → REPRESENTATIVE TRAINING EXAMPLES")
    print("=" * 80)

    for intent in intents:
        print("\n" + "-" * 80)
        print(f"INTENT: {intent}")
        print("-" * 80)

        intent_df = grouped[
            grouped["category"] == intent
        ]

        for number, text in enumerate(
            intent_df["text"],
            start=1
        ):
            print(f"{number}. {text}")


# ============================================================
# INTENT STATISTICS
# ============================================================

def print_statistics(df):
    counts = (
        df["category"]
        .value_counts()
        .sort_index()
    )

    print("\n" + "=" * 80)
    print("INTENT DATASET STATISTICS")
    print("=" * 80)

    print(f"\nTotal training samples: {len(df)}")
    print(f"Total intents: {df['category'].nunique()}")

    print("\nSamples per intent:")

    for intent, count in counts.items():
        print(
            f"{intent:<50} {count}"
        )


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 80)
    print("SUPPORTAI INTENT EXAMPLE ANALYSIS")
    print("=" * 80)

    print("\nLoading training data...")

    df = load_training_data()

    print(
        f"Training samples loaded: {len(df)}"
    )

    print_statistics(df)

    grouped = extract_examples(df)

    print_examples(grouped)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()