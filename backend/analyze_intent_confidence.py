from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score

from backend.app.models.intent_classifier import IntentClassifier


BASE_DIR = Path(__file__).resolve().parents[1]
TEST_PATH = BASE_DIR / "data" / "test.csv"


def main():
    print("=" * 60)
    print("INTENT CONFIDENCE ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(TEST_PATH)

    print(f"Test samples: {len(df)}")
    print("Loading intent classifier...")

    classifier = IntentClassifier(load_model=True)

    texts = df["text"].astype(str).tolist()
    true_intents = df["category"].astype(str).tolist()

    predictions = []
    confidences = []

    print("Running predictions...")

    for text in texts:
        result = classifier.predict(text)

        predictions.append(result["intent"])
        confidences.append(result["confidence"])

    df["predicted_intent"] = predictions
    df["confidence"] = confidences
    df["correct"] = df["predicted_intent"] == df["category"]

    bins = [0.0, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.01]
    labels = [
        "0.00-0.29",
        "0.30-0.39",
        "0.40-0.49",
        "0.50-0.59",
        "0.60-0.69",
        "0.70-0.79",
        "0.80-0.89",
        "0.90-1.00",
    ]

    df["confidence_range"] = pd.cut(
        df["confidence"],
        bins=bins,
        labels=labels,
        right=False
    )

    summary = (
        df.groupby("confidence_range", observed=False)
        .agg(
            samples=("correct", "size"),
            correct=("correct", "sum"),
            accuracy=("correct", "mean"),
        )
        .reset_index()
    )

    print()
    print("=" * 60)
    print("CONFIDENCE DISTRIBUTION")
    print("=" * 60)

    for _, row in summary.iterrows():
        print(
            f"{row['confidence_range']}: "
            f"{int(row['samples'])} samples | "
            f"{int(row['correct'])} correct | "
            f"accuracy={row['accuracy']:.4f}"
        )

    print()
    print("=" * 60)
    print("CURRENT ESCALATION THRESHOLD: 0.60")
    print("=" * 60)

    low_confidence = df[df["confidence"] < 0.60]

    print(f"Low-confidence samples: {len(low_confidence)}")
    print(f"Correct predictions: {int(low_confidence['correct'].sum())}")

    if len(low_confidence) > 0:
        print(
            f"Low-confidence accuracy: "
            f"{accuracy_score(low_confidence['category'], low_confidence['predicted_intent']):.4f}"
        )

    print()
    print("=" * 60)
    print("LOW-CONFIDENCE INTENT BREAKDOWN")
    print("=" * 60)

    breakdown = (
        low_confidence
        .groupby("category")
        .agg(
            samples=("correct", "size"),
            correct=("correct", "sum"),
            accuracy=("correct", "mean"),
            avg_confidence=("confidence", "mean"),
        )
        .sort_values("samples", ascending=False)
    )

    print(breakdown.to_string())

    print()
    print("=" * 60)
    print("CONFIDENCE ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()