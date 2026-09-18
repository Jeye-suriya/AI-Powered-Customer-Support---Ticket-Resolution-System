from pathlib import Path
import pandas as pd


# Project paths
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"


def load_banking_data():
    """Load the Banking77 training and test datasets."""

    train_path = DATA_DIR / "train.csv"
    test_path = DATA_DIR / "test.csv"

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    return train_df, test_df


def clean_text(text):
    """Clean a customer message."""

    if not isinstance(text, str):
        return ""

    # Remove leading/trailing spaces
    text = text.strip()

    # Replace multiple spaces/newlines with one space
    text = " ".join(text.split())

    return text


def preprocess_banking_data():
    """Clean and prepare the Banking77 datasets."""

    train_df, test_df = load_banking_data()

    # Clean customer messages
    train_df["text"] = train_df["text"].apply(clean_text)
    test_df["text"] = test_df["text"].apply(clean_text)

    # Remove missing values
    train_df = train_df.dropna(subset=["text", "category"])
    test_df = test_df.dropna(subset=["text", "category"])

    # Remove duplicate examples
    train_df = train_df.drop_duplicates(
        subset=["text", "category"]
    )

    test_df = test_df.drop_duplicates(
        subset=["text", "category"]
    )

    return train_df, test_df


def main():
    train_df, test_df = preprocess_banking_data()

    print("=" * 60)
    print("BANKING DATA PREPROCESSING")
    print("=" * 60)

    print("\nTraining samples:", len(train_df))
    print("Testing samples:", len(test_df))

    print("\nNumber of training intents:",
          train_df["category"].nunique())

    print("Number of testing intents:",
          test_df["category"].nunique())

    print("\nTraining columns:")
    print(train_df.columns.tolist())

    print("\nSample training data:")
    print(train_df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()