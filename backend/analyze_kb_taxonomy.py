import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "support_knowledge_base.csv"


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

def load_knowledge_base():
    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "kb_id",
        "category",
        "intent",
        "title",
        "problem",
        "symptoms",
        "resolution_steps",
        "additional_information",
        "escalation_condition",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing KB columns: {missing_columns}"
        )

    df = df.dropna(
        subset=[
            "kb_id",
            "category",
            "intent",
            "title",
        ]
    )

    return df.drop_duplicates(subset=["kb_id"])


# ============================================================
# DISPLAY ARTICLE
# ============================================================

def print_article(row):
    print("\n" + "-" * 80)

    print(f"KB ID: {row['kb_id']}")
    print(f"Category: {row['category']}")
    print(f"Intent: {row['intent']}")
    print(f"Title: {row['title']}")

    print("\nProblem:")
    print(str(row["problem"]).strip())

    print("\nSymptoms:")
    print(str(row["symptoms"]).strip())

    print("\nResolution:")
    print(str(row["resolution_steps"]).strip())

    print("\nAdditional information:")
    print(str(row["additional_information"]).strip())

    print("\nEscalation condition:")
    print(str(row["escalation_condition"]).strip())


# ============================================================
# CATEGORY SUMMARY
# ============================================================

def print_category_summary(df):
    print("\n" + "=" * 80)
    print("KB CATEGORY SUMMARY")
    print("=" * 80)

    category_counts = (
        df.groupby("category")
        .agg(
            articles=("kb_id", "count"),
            intents=("intent", "nunique"),
        )
        .sort_values(
            ["articles", "intents"],
            ascending=False
        )
    )

    print(category_counts.to_string())


# ============================================================
# INTENT SUMMARY
# ============================================================

def print_intent_summary(df):
    print("\n" + "=" * 80)
    print("KB INTENT SUMMARY")
    print("=" * 80)

    for _, row in (
        df[
            [
                "kb_id",
                "category",
                "intent",
                "title",
            ]
        ]
        .sort_values(["category", "intent"])
        .iterrows()
    ):
        print(
            f"{row['kb_id']:>6} | "
            f"{str(row['category']):<25} | "
            f"{str(row['intent']):<35} | "
            f"{row['title']}"
        )


# ============================================================
# DOMAIN GROUPING
# ============================================================

def print_domain_groups(df):
    print("\n" + "=" * 80)
    print("KB DOMAIN GROUPS")
    print("=" * 80)

    categories = sorted(df["category"].unique())

    for category in categories:
        category_df = df[df["category"] == category]

        print(f"\n[{category}]")

        for _, row in category_df.iterrows():
            print(
                f"  {row['kb_id']} - "
                f"{row['intent']} - "
                f"{row['title']}"
            )


# ============================================================
# POSSIBLY UNRELATED ARTICLES
# ============================================================

def print_technical_or_non_customer_articles(df):
    keywords = [
        "api",
        "workspace",
        "browser",
        "mobile",
        "pagination",
        "guest",
        "nonprofit",
        "rate limit",
        "admin",
        "developer",
    ]

    matches = []

    for _, row in df.iterrows():
        text = " ".join(
            [
                str(row["category"]),
                str(row["intent"]),
                str(row["title"]),
                str(row["problem"]),
            ]
        ).lower()

        if any(keyword in text for keyword in keywords):
            matches.append(row)

    print("\n" + "=" * 80)
    print("ARTICLES REQUIRING DOMAIN REVIEW")
    print("=" * 80)

    if not matches:
        print("\nNo obvious articles found.")
        return

    for row in matches:
        print(
            f"\n{row['kb_id']} | "
            f"{row['category']} | "
            f"{row['intent']} | "
            f"{row['title']}"
        )


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 80)
    print("SUPPORTAI KNOWLEDGE BASE TAXONOMY ANALYSIS")
    print("=" * 80)

    print("\nLoading knowledge base...")

    df = load_knowledge_base()

    print(f"Articles loaded: {len(df)}")
    print(f"Unique categories: {df['category'].nunique()}")
    print(f"Unique intents: {df['intent'].nunique()}")

    print_category_summary(df)

    print_intent_summary(df)

    print_domain_groups(df)

    print_technical_or_non_customer_articles(df)

    print("\n" + "=" * 80)
    print("TAXONOMY ANALYSIS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()