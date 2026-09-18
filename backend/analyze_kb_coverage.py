import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer

from backend.app.retrieval.knowledge_base import KnowledgeBase


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3


# ============================================================
# LOAD TEST DATA
# ============================================================

def load_test_data():
    path = DATA_DIR / "test.csv"

    df = pd.read_csv(path)
    df = df.dropna(subset=["text", "category"])

    return df


# ============================================================
# ANALYZE KB COVERAGE
# ============================================================

def analyze_coverage(knowledge_base, df):
    total = len(df)

    retrieved = 0
    not_retrieved = 0

    results = []

    for index, row in df.iterrows():
        ticket = row["text"]
        intent = row["category"]

        matches = knowledge_base.search(
            query=ticket,
            top_k=TOP_K
        )

        if matches:
            retrieved += 1

            top_match = matches[0]

            results.append({
                "ticket": ticket,
                "classifier_intent": intent,
                "kb_id": top_match["kb_id"],
                "kb_intent": top_match["intent"],
                "kb_title": top_match["title"],
                "similarity": top_match["similarity"],
                "retrieved": True
            })

        else:
            not_retrieved += 1

            results.append({
                "ticket": ticket,
                "classifier_intent": intent,
                "kb_id": None,
                "kb_intent": None,
                "kb_title": None,
                "similarity": None,
                "retrieved": False
            })

    result_df = pd.DataFrame(results)

    print("\n" + "=" * 70)
    print("KB COVERAGE ANALYSIS")
    print("=" * 70)

    print(f"\nTotal test tickets: {total}")
    print(f"Retrieved: {retrieved}")
    print(f"Not retrieved: {not_retrieved}")

    coverage = retrieved / total if total else 0.0

    print(f"Coverage: {coverage:.4f}")

    # --------------------------------------------------------
    # Similarity distribution
    # --------------------------------------------------------

    retrieved_df = result_df[result_df["retrieved"]]

    if not retrieved_df.empty:
        print("\n" + "-" * 70)
        print("SIMILARITY DISTRIBUTION")
        print("-" * 70)

        print(
            retrieved_df["similarity"]
            .describe()
            .to_string()
        )

    # --------------------------------------------------------
    # Most common classifier intents with no KB result
    # --------------------------------------------------------

    missing_df = result_df[~result_df["retrieved"]]

    if not missing_df.empty:
        print("\n" + "-" * 70)
        print("INTENTS WITH NO KB RESULT")
        print("-" * 70)

        missing_intents = (
            missing_df["classifier_intent"]
            .value_counts()
            .head(20)
        )

        print(missing_intents.to_string())

    # --------------------------------------------------------
    # Show low-similarity successful results
    # --------------------------------------------------------

    if not retrieved_df.empty:
        print("\n" + "-" * 70)
        print("LOWEST-SIMILARITY RETRIEVED RESULTS")
        print("-" * 70)

        lowest = (
            retrieved_df
            .sort_values("similarity")
            .head(20)
        )

        for _, row in lowest.iterrows():
            print(
                f"\nTicket: {row['ticket']}"
                f"\nClassifier intent: {row['classifier_intent']}"
                f"\nKB ID: {row['kb_id']}"
                f"\nKB intent: {row['kb_intent']}"
                f"\nKB title: {row['kb_title']}"
                f"\nSimilarity: {row['similarity']:.4f}"
            )

    # --------------------------------------------------------
    # Show examples with no result
    # --------------------------------------------------------

    if not missing_df.empty:
        print("\n" + "-" * 70)
        print("EXAMPLES WITH NO SUFFICIENTLY RELEVANT KB RESULT")
        print("-" * 70)

        examples = missing_df.head(30)

        for _, row in examples.iterrows():
            print(
                f"\nTicket: {row['ticket']}"
                f"\nClassifier intent: {row['classifier_intent']}"
            )

    return result_df


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 70)
    print("SUPPORTAI KNOWLEDGE BASE COVERAGE ANALYSIS")
    print("=" * 70)

    print("\nLoading test data...")
    test_df = load_test_data()
    print(f"Test samples: {len(test_df)}")

    print("\nLoading embedding model...")
    encoder = SentenceTransformer(EMBEDDING_MODEL)

    print("Loading knowledge base...")
    knowledge_base = KnowledgeBase(
        encoder=encoder
    )

    analyze_coverage(
        knowledge_base,
        test_df
    )

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()