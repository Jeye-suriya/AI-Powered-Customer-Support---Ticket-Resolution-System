from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[1]
TRAIN_PATH = BASE_DIR / "data" / "train.csv"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VALIDATION_SIZE = 0.20
RANDOM_STATE = 42


def main():
    print("=" * 60)
    print("INTENT ESCALATION THRESHOLD ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(TRAIN_PATH)

    texts = df["text"].astype(str).tolist()
    labels = df["category"].astype(str).tolist()

    print(f"Total training samples: {len(df)}")

    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts,
        labels,
        test_size=VALIDATION_SIZE,
        random_state=RANDOM_STATE,
        stratify=labels,
    )

    print(f"Temporary training samples: {len(train_texts)}")
    print(f"Validation samples: {len(val_texts)}")

    print()
    print("Loading embedding model...")

    encoder = SentenceTransformer(EMBEDDING_MODEL)

    print("Encoding temporary training set...")

    train_embeddings = encoder.encode(
        train_texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    print("Encoding validation set...")

    val_embeddings = encoder.encode(
        val_texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    print()
    print("Training temporary validation classifier...")

    classifier = LogisticRegression(
        max_iter=3000,
        class_weight="balanced",
        C=2.0,
    )

    classifier.fit(train_embeddings, train_labels)

    probabilities = classifier.predict_proba(val_embeddings)
    predictions = classifier.classes_[probabilities.argmax(axis=1)]
    confidences = probabilities.max(axis=1)

    validation_accuracy = accuracy_score(
        val_labels,
        predictions,
    )

    print()
    print("=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)

    print(f"Validation accuracy: {validation_accuracy:.4f}")

    validation_df = pd.DataFrame({
        "category": val_labels,
        "predicted_intent": predictions,
        "confidence": confidences,
    })

    validation_df["correct"] = (
        validation_df["category"]
        == validation_df["predicted_intent"]
    )

    print()
    print("=" * 60)
    print("THRESHOLD ANALYSIS")
    print("=" * 60)

    print(
        f"{'Threshold':<12}"
        f"{'Escalated':<12}"
        f"{'Escalation %':<15}"
        f"{'Auto-resolved':<15}"
        f"{'Auto accuracy':<15}"
    )

    thresholds = [
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.65,
        0.70,
    ]

    for threshold in thresholds:
        escalated = validation_df["confidence"] < threshold
        auto_resolved = ~escalated

        escalated_count = int(escalated.sum())
        auto_resolved_count = int(auto_resolved.sum())

        if auto_resolved_count > 0:
            auto_accuracy = accuracy_score(
                validation_df.loc[auto_resolved, "category"],
                validation_df.loc[auto_resolved, "predicted_intent"],
            )
        else:
            auto_accuracy = 0.0

        escalation_percentage = (
            escalated_count / len(validation_df)
        )

        print(
            f"{threshold:<12.2f}"
            f"{escalated_count:<12}"
            f"{escalation_percentage:<15.2%}"
            f"{auto_resolved_count:<15}"
            f"{auto_accuracy:<15.4f}"
        )

    print()
    print("=" * 60)
    print("CONFIDENCE DISTRIBUTION")
    print("=" * 60)

    bins = [
        0.0,
        0.30,
        0.40,
        0.50,
        0.60,
        0.70,
        0.80,
        0.90,
        1.01,
    ]

    labels_range = [
        "0.00-0.29",
        "0.30-0.39",
        "0.40-0.49",
        "0.50-0.59",
        "0.60-0.69",
        "0.70-0.79",
        "0.80-0.89",
        "0.90-1.00",
    ]

    validation_df["confidence_range"] = pd.cut(
        validation_df["confidence"],
        bins=bins,
        labels=labels_range,
        right=False,
    )

    summary = (
        validation_df
        .groupby("confidence_range", observed=False)
        .agg(
            samples=("correct", "size"),
            correct=("correct", "sum"),
            accuracy=("correct", "mean"),
        )
        .reset_index()
    )

    for _, row in summary.iterrows():
        print(
            f"{row['confidence_range']}: "
            f"{int(row['samples'])} samples | "
            f"{int(row['correct'])} correct | "
            f"accuracy={row['accuracy']:.4f}"
        )

    print()
    print("=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()