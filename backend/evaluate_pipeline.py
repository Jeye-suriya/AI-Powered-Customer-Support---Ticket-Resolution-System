import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sentence_transformers import SentenceTransformer

from backend.app.models.oos_detector import OOSDetector
from backend.app.models.intent_classifier import IntentClassifier
from backend.app.retrieval.knowledge_base import KnowledgeBase


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
RETRIEVAL_TOP_K = 3
INTENT_CONFIDENCE_THRESHOLD = 0.60


# ============================================================
# LOAD IN-DOMAIN TEST DATA
# ============================================================

def load_in_domain_test():
    path = DATA_DIR / "test.csv"

    df = pd.read_csv(path)

    df = df.dropna(
        subset=["text", "category"]
    )

    return df


# ============================================================
# LOAD OOS TEST DATA
# ============================================================

def load_oos_test():
    path = DATA_DIR / "data_full.json"

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    return data["oos_test"]


# ============================================================
# OOS DETECTOR EVALUATION
# ============================================================

def evaluate_oos(
    detector,
    in_domain_df
):
    print("\n" + "=" * 60)
    print("OOS DETECTOR EVALUATION")
    print("=" * 60)

    oos_samples = load_oos_test()

    y_true = []
    y_pred = []

    for text in in_domain_df["text"]:

        result = detector.predict(text)

        y_true.append("in_domain")

        y_pred.append(
            "oos"
            if result["is_oos"]
            else "in_domain"
        )

    for sample in oos_samples:

        if isinstance(sample, dict):
            text = sample.get(
                "text",
                sample.get("query", "")
            )
        else:
            text = str(sample)

        if not text:
            continue

        result = detector.predict(text)

        y_true.append("oos")

        y_pred.append(
            "oos"
            if result["is_oos"]
            else "in_domain"
        )

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    print(
        f"\nSamples evaluated: {len(y_true)}"
    )

    print(
        f"Accuracy: {accuracy:.4f}"
    )

    print("\nClassification Report:")

    print(
        classification_report(
            y_true,
            y_pred,
            digits=4
        )
    )

    return accuracy


# ============================================================
# INTENT CLASSIFIER EVALUATION
# ============================================================

def evaluate_intent(
    classifier,
    df
):
    print("\n" + "=" * 60)
    print("INTENT CLASSIFIER EVALUATION")
    print("=" * 60)

    y_true = []
    y_pred = []

    for _, row in df.iterrows():

        result = classifier.predict(
            row["text"]
        )

        y_true.append(
            row["category"]
        )

        y_pred.append(
            result["intent"]
        )

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    print(
        f"\nSamples evaluated: {len(y_true)}"
    )

    print(
        f"Accuracy: {accuracy:.4f}"
    )

    print("\nClassification Report:")

    print(
        classification_report(
            y_true,
            y_pred,
            digits=4,
            zero_division=0
        )
    )

    return accuracy


# ============================================================
# KNOWLEDGE BASE RETRIEVAL EVALUATION
# ============================================================

def evaluate_retrieval(
    knowledge_base,
    intent_classifier,
    df
):
    print("\n" + "=" * 60)
    print("KNOWLEDGE BASE RETRIEVAL EVALUATION")
    print("=" * 60)

    total = 0
    retrieved = 0

    top1_correct = 0
    top3_correct = 0

    reciprocal_ranks = []
    similarities = []

    for _, row in df.iterrows():

        ticket = row["text"]
        true_intent = row["category"]

        intent_result = intent_classifier.predict(
            ticket
        )

        predicted_intent = intent_result["intent"]

        results = knowledge_base.search(
            query=ticket,
            intent=predicted_intent,
            top_k=RETRIEVAL_TOP_K
        )

        total += 1

        if not results:
            continue

        retrieved += 1

        top_similarity = results[0].get(
            "similarity"
        )

        if isinstance(
            top_similarity,
            (int, float)
        ):
            similarities.append(
                top_similarity
            )

        retrieved_intents = [
            result.get("intent")
            for result in results
        ]

        if (
            retrieved_intents
            and retrieved_intents[0] == true_intent
        ):
            top1_correct += 1

        if true_intent in retrieved_intents:

            top3_correct += 1

            rank = (
                retrieved_intents.index(true_intent)
                + 1
            )

            reciprocal_ranks.append(
                1.0 / rank
            )

        else:
            reciprocal_ranks.append(0.0)

    coverage = (
        retrieved / total
        if total
        else 0.0
    )

    top1_accuracy = (
        top1_correct / total
        if total
        else 0.0
    )

    top3_recall = (
        top3_correct / total
        if total
        else 0.0
    )

    mrr = (
        sum(reciprocal_ranks)
        / len(reciprocal_ranks)
        if reciprocal_ranks
        else 0.0
    )

    average_similarity = (
        sum(similarities)
        / len(similarities)
        if similarities
        else 0.0
    )

    print(
        f"\nSamples evaluated: {total}"
    )

    print(
        f"Retrieved successfully: "
        f"{retrieved}/{total}"
    )

    print(
        f"No sufficiently relevant result: "
        f"{total - retrieved}"
    )

    print(
        f"Retrieval coverage: "
        f"{coverage:.4f}"
    )

    print(
        f"KB Top-1 Intent Accuracy: "
        f"{top1_accuracy:.4f}"
    )

    print(
        f"KB Top-3 Intent Recall: "
        f"{top3_recall:.4f}"
    )

    print(
        f"KB Mean Reciprocal Rank (MRR): "
        f"{mrr:.4f}"
    )

    print(
        f"Average top similarity: "
        f"{average_similarity:.4f}"
    )

    return {
        "coverage": coverage,
        "top1_accuracy": top1_accuracy,
        "top3_recall": top3_recall,
        "mrr": mrr,
        "average_similarity": average_similarity
    }


# ============================================================
# END-TO-END ROUTING EVALUATION
# ============================================================

def evaluate_routing(
    oos_detector,
    intent_classifier,
    df
):
    print("\n" + "=" * 60)
    print("END-TO-END ROUTING EVALUATION")
    print("=" * 60)

    total = 0
    correct = 0

    oos_false_rejections = 0
    low_confidence = 0

    for _, row in df.iterrows():

        ticket = row["text"]

        total += 1

        oos_result = oos_detector.predict(
            ticket
        )

        if oos_result["is_oos"]:

            oos_false_rejections += 1

            continue

        intent_result = intent_classifier.predict(
            ticket
        )

        predicted_intent = intent_result[
            "intent"
        ]

        confidence = intent_result[
            "confidence"
        ]

        if confidence < INTENT_CONFIDENCE_THRESHOLD:
            low_confidence += 1

        if predicted_intent == row["category"]:
            correct += 1

    routing_accuracy = (
        correct / total
        if total
        else 0.0
    )

    print(
        f"\nSamples evaluated: {total}"
    )

    print(
        f"Correct routing: "
        f"{correct}/{total}"
    )

    print(
        f"Routing accuracy: "
        f"{routing_accuracy:.4f}"
    )

    print(
        f"In-domain tickets incorrectly rejected by OOS: "
        f"{oos_false_rejections}"
    )

    print(
        f"Low-confidence intent predictions: "
        f"{low_confidence}"
    )

    return {
        "accuracy": routing_accuracy,
        "oos_false_rejections": oos_false_rejections,
        "low_confidence": low_confidence
    }


# ============================================================
# COMPLETE END-TO-END PIPELINE EVALUATION
# ============================================================

def evaluate_end_to_end(
    oos_detector,
    intent_classifier,
    knowledge_base,
    df
):
    print("\n" + "=" * 60)
    print("COMPLETE END-TO-END PIPELINE EVALUATION")
    print("=" * 60)

    total = len(df)

    oos_rejected = 0
    low_confidence = 0
    no_kb_result = 0
    successfully_routed = 0
    correctly_routed = 0

    for _, row in df.iterrows():

        ticket = row["text"]
        true_intent = row["category"]

        # ----------------------------------------------------
        # Step 1: OOS detection
        # ----------------------------------------------------

        oos_result = oos_detector.predict(
            ticket
        )

        if oos_result["is_oos"]:
            oos_rejected += 1
            continue

        # ----------------------------------------------------
        # Step 2: Intent classification
        # ----------------------------------------------------

        intent_result = intent_classifier.predict(
            ticket
        )

        predicted_intent = intent_result["intent"]
        confidence = intent_result["confidence"]

        if confidence < INTENT_CONFIDENCE_THRESHOLD:
            low_confidence += 1
            continue

        # ----------------------------------------------------
        # Step 3: Knowledge base retrieval
        # ----------------------------------------------------

        results = knowledge_base.search(
            query=ticket,
            intent=predicted_intent,
            top_k=RETRIEVAL_TOP_K
        )

        if not results:
            no_kb_result += 1
            continue

        successfully_routed += 1

        # ----------------------------------------------------
        # Step 4: Final routing correctness
        # ----------------------------------------------------

        if predicted_intent == true_intent:

            retrieved_intents = [
                result.get("intent")
                for result in results
            ]

            if true_intent in retrieved_intents:
                correctly_routed += 1

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    successful_processing_rate = (
        successfully_routed / total
        if total
        else 0.0
    )

    final_correctness = (
        correctly_routed / total
        if total
        else 0.0
    )

    print(
        f"\nTotal tickets: {total}"
    )

    print(
        f"OOS false rejections: "
        f"{oos_rejected}"
    )

    print(
        f"Low-confidence escalations: "
        f"{low_confidence}"
    )

    print(
        f"No KB result: "
        f"{no_kb_result}"
    )

    print(
        f"Successfully processed: "
        f"{successfully_routed}"
    )

    print(
        f"Correctly processed: "
        f"{correctly_routed}"
    )

    print(
        f"Successful processing rate: "
        f"{successful_processing_rate:.4f}"
    )

    print(
        f"Final pipeline correctness: "
        f"{final_correctness:.4f}"
    )

    return {
        "successful_processing_rate": successful_processing_rate,
        "final_correctness": final_correctness,
        "oos_false_rejections": oos_rejected,
        "low_confidence": low_confidence,
        "no_kb_result": no_kb_result,
        "successfully_processed": successfully_routed,
        "correctly_processed": correctly_routed
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("SUPPORTAI PIPELINE EVALUATION")
    print("=" * 60)

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    print("\nLoading test data...")

    test_df = load_in_domain_test()

    print(
        f"In-domain test samples: "
        f"{len(test_df)}"
    )

    # --------------------------------------------------------
    # Shared encoder
    # --------------------------------------------------------

    print(
        "\nLoading shared embedding model..."
    )

    encoder = SentenceTransformer(
        EMBEDDING_MODEL
    )

    # --------------------------------------------------------
    # Models
    # --------------------------------------------------------

    print(
        "Loading OOS detector..."
    )

    oos_detector = OOSDetector(
        load_model=True,
        encoder=encoder
    )

    print(
        "OOS detector loaded."
    )

    print(
        "Loading intent classifier..."
    )

    intent_classifier = IntentClassifier(
        load_model=True,
        encoder=encoder
    )

    print(
        "Intent classifier loaded."
    )

    print(
        "Loading knowledge base..."
    )

    knowledge_base = KnowledgeBase(
        encoder=encoder
    )

    # --------------------------------------------------------
    # Evaluate
    # --------------------------------------------------------

    oos_accuracy = evaluate_oos(
        oos_detector,
        test_df
    )

    intent_accuracy = evaluate_intent(
        intent_classifier,
        test_df
    )

    retrieval_metrics = evaluate_retrieval(
        knowledge_base,
        intent_classifier,
        test_df
    )

    routing_metrics = evaluate_routing(
        oos_detector,
        intent_classifier,
        test_df
    )

    end_to_end_metrics = evaluate_end_to_end(
        oos_detector,
        intent_classifier,
        knowledge_base,
        test_df
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL EVALUATION SUMMARY")
    print("=" * 60)

    print(
        f"\nOOS Accuracy: "
        f"{oos_accuracy:.4f}"
    )

    print(
        f"Intent Accuracy: "
        f"{intent_accuracy:.4f}"
    )

    print(
        f"KB Retrieval Coverage: "
        f"{retrieval_metrics['coverage']:.4f}"
    )

    print(
        f"KB Top-1 Intent Accuracy: "
        f"{retrieval_metrics['top1_accuracy']:.4f}"
    )

    print(
        f"KB Top-3 Intent Recall: "
        f"{retrieval_metrics['top3_recall']:.4f}"
    )

    print(
        f"KB MRR: "
        f"{retrieval_metrics['mrr']:.4f}"
    )

    print(
        f"Average KB Similarity: "
        f"{retrieval_metrics['average_similarity']:.4f}"
    )

    print(
        f"End-to-End Routing Accuracy: "
        f"{routing_metrics['accuracy']:.4f}"
    )

    print(
        f"Final Pipeline Processing Rate: "
        f"{end_to_end_metrics['successful_processing_rate']:.4f}"
    )

    print(
        f"Final Pipeline Correctness: "
        f"{end_to_end_metrics['final_correctness']:.4f}"
    )

    print(
        "\nEvaluation completed successfully."
    )


if __name__ == "__main__":
    main()