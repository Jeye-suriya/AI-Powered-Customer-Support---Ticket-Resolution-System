from pathlib import Path

import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "intent"
    / "intent_classifier.joblib"
)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class IntentClassifier:
    def __init__(self, load_model=False, encoder=None):
        self.encoder = encoder or SentenceTransformer(EMBEDDING_MODEL)
        self.classifier = None

        if load_model:
            self.load()

    def train(self, train_df):
        texts = train_df["text"].tolist()
        labels = train_df["category"].tolist()

        print("Encoding intent training data...")

        embeddings = self.encoder.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        self.classifier = LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            C=2.0
        )

        self.classifier.fit(
            embeddings,
            labels
        )

    def evaluate(self, test_df):
        if self.classifier is None:
            raise RuntimeError(
                "Intent classifier has not been trained or loaded."
            )

        texts = test_df["text"].tolist()
        labels = test_df["category"].tolist()

        print("Encoding intent test data...")

        embeddings = self.encoder.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        predictions = self.classifier.predict(
            embeddings
        )

        accuracy = accuracy_score(
            labels,
            predictions
        )

        macro_f1 = f1_score(
            labels,
            predictions,
            average="macro"
        )

        weighted_f1 = f1_score(
            labels,
            predictions,
            average="weighted"
        )

        print("\nIntent Classifier Evaluation")
        print("=" * 60)

        print(f"Accuracy: {accuracy:.4f}")
        print(f"Macro F1: {macro_f1:.4f}")
        print(f"Weighted F1: {weighted_f1:.4f}")

        print("\nClassification Report:")
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
                "Intent classifier has not been trained or loaded."
            )

        embedding = self.encoder.encode(
            [text],
            normalize_embeddings=True
        )

        prediction = self.classifier.predict(
            embedding
        )[0]

        probabilities = self.classifier.predict_proba(
            embedding
        )[0]

        confidence = float(
            probabilities.max()
        )

        return {
            "intent": prediction,
            "confidence": confidence
        }

    def save(self):
        if self.classifier is None:
            raise RuntimeError(
                "Cannot save an untrained intent classifier."
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
            f"Intent classifier saved to: {MODEL_PATH}"
        )

    def load(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Intent classifier model not found: {MODEL_PATH}"
            )

        saved_model = joblib.load(
            MODEL_PATH
        )

        self.classifier = saved_model["classifier"]

        print("Intent classifier loaded.")


if __name__ == "__main__":
    from backend.app.data.preprocess import load_datasets

    train_df, test_df, _, _ = load_datasets()

    classifier = IntentClassifier()

    classifier.train(
        train_df=train_df
    )

    classifier.evaluate(
        test_df=test_df
    )

    classifier.save()