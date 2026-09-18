import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from backend.app.retrieval.knowledge_base import KnowledgeBase


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3


# ============================================================
# LOAD DATA
# ============================================================

def load_classifier_intents():
    path = DATA_DIR / "train.csv"

    df = pd.read_csv(path)
    df = df.dropna(subset=["text", "category"])

    return sorted(df["category"].unique())


def load_knowledge_base():
    path = DATA_DIR / "support_knowledge_base.csv"

    df = pd.read_csv(path)
    df = df.dropna(
        subset=[
            "kb_id",
            "category",
            "intent",
            "title",
            "search_text"
        ]
    )

    df = df.drop_duplicates(subset=["kb_id"])

    return df


# ============================================================
# SEMANTIC INTENT COMPARISON
# ============================================================

def compare_intents(classifier_intents, kb_df, encoder):
    kb_intents = kb_df["intent"].tolist()

    classifier_embeddings = encoder.encode(
        classifier_intents,
        normalize_embeddings=True
    )

    kb_embeddings = encoder.encode(
        kb_intents,
        normalize_embeddings=True
    )

    similarities = cosine_similarity(
        classifier_embeddings,
        kb_embeddings
    )

    rows = []

    for i, classifier_intent in enumerate(classifier_intents):
        top_indices = similarities[i].argsort()[::-1][:TOP_K]

        for rank, kb_index in enumerate(top_indices, start=1):
            kb_row = kb_df.iloc[kb_index]

            rows.append({
                "classifier_intent": classifier_intent,
                "rank": rank,
                "kb_id": kb_row["kb_id"],
                "kb_intent": kb_row["intent"],
                "kb_title": kb_row["title"],
                "similarity": float(similarities[i][kb_index])
            })

    return pd.DataFrame(rows)


# ============================================================
# PRINT COVERAGE MATRIX
# ============================================================

def print_coverage_matrix(results):
    print("\n" + "=" * 80)
    print("CLASSIFIER → KB INTENT COVERAGE")
    print("=" * 80)

    top_results = results[results["rank"] == 1].copy()

    top_results = top_results.sort_values(
        "similarity",
        ascending=False
    )

    for _, row in top_results.iterrows():
        print(
            f"\nClassifier intent : {row['classifier_intent']}"
            f"\nClosest KB intent : {row['kb_intent']}"
            f"\nKB ID             : {row['kb_id']}"
            f"\nKB title          : {row['kb_title']}"
            f"\nSimilarity        : {row['similarity']:.4f}"
        )


# ============================================================
# COVERAGE SUMMARY
# ============================================================

def print_summary(results):
    top_results = results[results["rank"] == 1].copy()

    print("\n" + "=" * 80)
    print("COVERAGE SUMMARY")
    print("=" * 80)

    print(f"\nClassifier intents: {len(top_results)}")
    print(
        f"KB intents: "
        f"{top_results['kb_intent'].nunique()}"
    )

    print("\nSemantic similarity groups:")

    high = (top_results["similarity"] >= 0.70).sum()
    medium = (
        (top_results["similarity"] >= 0.50)
        & (top_results["similarity"] < 0.70)
    ).sum()
    low = (top_results["similarity"] < 0.50).sum()

    print(f"  Strong match   (>= 0.70): {high}")
    print(f"  Possible match (0.50-0.69): {medium}")
    print(f"  Weak match     (< 0.50): {low}")

    print("\nWeakest classifier → KB matches:")

    weakest = (
        top_results
        .sort_values("similarity")
        .head(20)
    )

    for _, row in weakest.iterrows():
        print(
            f"  {row['classifier_intent']}"
            f" -> {row['kb_intent']}"
            f" ({row['similarity']:.4f})"
        )


# ============================================================
# EXACT INTENT OVERLAP
# ============================================================

def print_exact_overlap(classifier_intents, kb_df):
    kb_intents = set(kb_df["intent"])

    exact_matches = [
        intent
        for intent in classifier_intents
        if intent in kb_intents
    ]

    missing = [
        intent
        for intent in classifier_intents
        if intent not in kb_intents
    ]

    print("\n" + "=" * 80)
    print("EXACT INTENT OVERLAP")
    print("=" * 80)

    print(
        f"\nExact matching intents: "
        f"{len(exact_matches)}"
    )

    print(
        f"Classifier intents without exact KB intent: "
        f"{len(missing)}"
    )

    if exact_matches:
        print("\nExact matches:")

        for intent in sorted(exact_matches):
            print(f"  {intent}")

    print("\nClassifier intents without exact KB match:")

    for intent in sorted(missing):
        print(f"  {intent}")


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 80)
    print("SUPPORTAI KB INTENT COVERAGE ANALYSIS")
    print("=" * 80)

    print("\nLoading classifier intents...")
    classifier_intents = load_classifier_intents()

    print(
        f"Classifier intents loaded: "
        f"{len(classifier_intents)}"
    )

    print("\nLoading knowledge base...")
    kb_df = load_knowledge_base()

    print(
        f"KB articles loaded: "
        f"{len(kb_df)}"
    )

    print(
        f"Unique KB intents: "
        f"{kb_df['intent'].nunique()}"
    )

    print("\nLoading embedding model...")
    encoder = SentenceTransformer(EMBEDDING_MODEL)

    print("\nComparing classifier and KB intents...")
    results = compare_intents(
        classifier_intents,
        kb_df,
        encoder
    )

    print_exact_overlap(
        classifier_intents,
        kb_df
    )

    print_coverage_matrix(results)

    print_summary(results)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()