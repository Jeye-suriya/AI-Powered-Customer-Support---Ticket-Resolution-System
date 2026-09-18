import json
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"


def inspect_csv(filename):
    file_path = DATA_DIR / filename

    print("\n" + "=" * 60)
    print(f"FILE: {filename}")
    print("=" * 60)

    df = pd.read_csv(file_path)

    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))


def inspect_json(filename):
    file_path = DATA_DIR / filename

    print("\n" + "=" * 60)
    print(f"FILE: {filename}")
    print("=" * 60)

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    print("Type:", type(data).__name__)

    if isinstance(data, list):
        print("Records:", len(data))
        print("\nFirst record:")
        print(json.dumps(data[0], indent=2, ensure_ascii=False))

    elif isinstance(data, dict):
        print("Keys:", list(data.keys()))


def main():
    inspect_csv("train.csv")
    inspect_csv("test.csv")
    inspect_csv("support_knowledge_base.csv")
    inspect_csv(
        "Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"
    )

    inspect_json("data_full.json")
    inspect_json("categories.json")


if __name__ == "__main__":
    main()