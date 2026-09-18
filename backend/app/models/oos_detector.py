from pathlib import Path

import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from backend.app.config import DATA_DIR

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = BASE_DIR / "models" / "oos" / "oos_detector.joblib"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class OOSDetector:
    def __init__(self, load_model=False, encoder=None):
        self.encoder = encoder or SentenceTransformer(EMBEDDING_MODEL)
        self.classifier = None

        if load_model:
            self.load()

    def train(self, train_df, oos_train_df):
        in_domain_texts = train_df["text"].tolist()
        in_domain_labels = ["in_domain"] * len(in_domain_texts)

        oos_texts = oos_train_df["text"].tolist()
        oos_labels = ["oos"] * len(oos_texts)

        texts = in_domain_texts + oos_texts
        labels = in_domain_labels + oos_labels

        print("Encoding OOS training data...")

        embeddings = self.encoder.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        self.classifier = LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            C=2.0
        )

        self.classifier.fit(embeddings, labels)

    def evaluate(self, test_df, oos_test_df):
        if self.classifier is None:
            raise RuntimeError(
                "OOS detector has not been trained or loaded."
            )

        in_domain_texts = test_df["text"].tolist()
        in_domain_labels = ["in_domain"] * len(in_domain_texts)

        oos_texts = oos_test_df["text"].tolist()
        oos_labels = ["oos"] * len(oos_texts)

        texts = in_domain_texts + oos_texts
        labels = in_domain_labels + oos_labels

        embeddings = self.encoder.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        predictions = self.classifier.predict(embeddings)

        print("\nOOS Detector Evaluation")
        print("=" * 60)

        print(
            f"Accuracy: "
            f"{accuracy_score(labels, predictions):.4f}"
        )

        print(
            classification_report(
                labels,
                predictions,
                digits=4
            )
        )

    def predict(self, text):
        if self.classifier is None:
            raise RuntimeError(
                "OOS detector has not been trained or loaded."
            )

        embedding = self.encoder.encode(
            [text],
            normalize_embeddings=True
        )

        prediction = self.classifier.predict(embedding)[0]

        probabilities = self.classifier.predict_proba(
            embedding
        )[0]

        oos_index = list(
            self.classifier.classes_
        ).index("oos")

        return {
            "is_oos": prediction == "oos",
            "confidence": float(
                probabilities[oos_index]
            )
        }

    def save(self):
        if self.classifier is None:
            raise RuntimeError(
                "Cannot save an untrained OOS detector."
            )

        MODEL_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(
            {
                "classifier": self.classifier
            },
            MODEL_PATH
        )

        print(
            f"OOS detector saved to: {MODEL_PATH}"
        )

    def load(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"OOS detector model not found: {MODEL_PATH}"
            )

        saved_model = joblib.load(MODEL_PATH)

        self.classifier = saved_model["classifier"]

        print("OOS detector loaded.")


if __name__ == "__main__":
    from backend.app.data.preprocess import load_datasets

    train_df, test_df, oos_train_df, oos_test_df = load_datasets()

    detector = OOSDetector()

    detector.train(
        train_df=train_df,
        oos_train_df=oos_train_df
    )

    detector.evaluate(
        test_df=test_df,
        oos_test_df=oos_test_df
    )

    detector.save()