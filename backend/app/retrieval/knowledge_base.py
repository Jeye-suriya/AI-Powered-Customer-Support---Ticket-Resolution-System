from pathlib import Path

import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_PATH = BASE_DIR / "data" / "support_knowledge_base.csv"
VECTOR_DB_PATH = BASE_DIR / "models" / "vector_db"

COLLECTION_NAME = "support_knowledge_base"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

MIN_SIMILARITY = 0.45

# Intent match is used as a ranking bonus,
# not as a hard filter.
INTENT_MATCH_BONUS = 0.15


# ============================================================
# KNOWLEDGE BASE
# ============================================================

class KnowledgeBase:

    def __init__(self, encoder=None):

        self.encoder = (
            encoder
            or SentenceTransformer(EMBEDDING_MODEL)
        )

        self.client = chromadb.PersistentClient(
            path=str(VECTOR_DB_PATH)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={
                    "hnsw:space": "cosine"
                }
            )
        )

    # ========================================================
    # LOAD DATA
    # ========================================================

    def load_data(self):

        if not DATA_PATH.exists():
            raise FileNotFoundError(
                f"Knowledge base not found: {DATA_PATH}"
            )

        df = pd.read_csv(DATA_PATH)

        required_columns = [
            "kb_id",
            "category",
            "intent",
            "title",
            "search_text",
            "escalation_condition"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                "Knowledge base is missing columns: "
                f"{missing_columns}"
            )

        df = df.dropna(
            subset=required_columns
        )

        df = df.drop_duplicates(
            subset=["kb_id"]
        )

        return df

    # ========================================================
    # BUILD VECTOR DATABASE
    # ========================================================

    def build(self):

        df = self.load_data()

        print(
            "Building knowledge base vector store..."
        )

        print(
            f"Knowledge base entries: {len(df)}"
        )

        texts = (
            df["search_text"]
            .astype(str)
            .tolist()
        )

        print(
            "\nEncoding knowledge base..."
        )

        embeddings = self.encoder.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        self.collection.upsert(
            ids=df["kb_id"].astype(str).tolist(),
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=[
                {
                    "kb_id": str(row["kb_id"]),
                    "category": str(row["category"]),
                    "intent": str(row["intent"]),
                    "title": str(row["title"]),
                    "escalation_condition": str(
                        row["escalation_condition"]
                    )
                }
                for _, row in df.iterrows()
            ]
        )

        print(
            "\nKnowledge base successfully indexed."
        )

        print(
            f"Vector database: {VECTOR_DB_PATH}"
        )

    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        query,
        intent=None,
        top_k=3
    ):

        if not query or not str(query).strip():
            return []

        # Retrieve more candidates than requested.
        # This allows the intent-aware ranking to work.
        candidate_k = max(
            top_k * 5,
            10
        )

        embedding = self.encoder.encode(
            [str(query)],
            normalize_embeddings=True
        )

        results = self.collection.query(
            query_embeddings=embedding.tolist(),
            n_results=candidate_k
        )

        matches = self._format_results(
            results
        )

        if not matches:
            return []

        # ----------------------------------------------------
        # Intent-aware re-ranking
        # ----------------------------------------------------

        for result in matches:

            semantic_similarity = (
                result["similarity"]
            )

            intent_match = (
                intent is not None
                and result["intent"] == intent
            )

            result["intent_match"] = (
                intent_match
            )

            result["ranking_score"] = (
                semantic_similarity
                + (
                    INTENT_MATCH_BONUS
                    if intent_match
                    else 0.0
                )
            )

        matches.sort(
            key=lambda result: result["ranking_score"],
            reverse=True
        )

        return matches[:top_k]

    # ========================================================
    # FORMAT RESULTS
    # ========================================================

    def _format_results(
        self,
        results
    ):

        matches = []

        ids = results.get(
            "ids",
            [[]]
        )[0]

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        for i in range(len(ids)):

            metadata = metadatas[i]

            distance = float(
                distances[i]
            )

            similarity = (
                1.0 - distance
            )

            if similarity < MIN_SIMILARITY:
                continue

            matches.append(
                {
                    "kb_id": metadata["kb_id"],
                    "category": metadata["category"],
                    "intent": metadata["intent"],
                    "title": metadata["title"],
                    "escalation_condition": metadata.get(
                        "escalation_condition"
                    ),
                    "document": documents[i],
                    "distance": distance,
                    "similarity": similarity
                }
            )

        return matches


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    knowledge_base = KnowledgeBase()

    test_cases = [
        {
            "query": "I forgot my password and cannot log in.",
            "intent": "passcode_forgotten"
        },
        {
            "query": "My card payment wasn't mine.",
            "intent": "declined_card_payment"
        },
        {
            "query": "My transfer is still pending.",
            "intent": "pending_transfer"
        },
        {
            "query": "I want to delete my account.",
            "intent": "terminate_account"
        },
        {
            "query": "What is the weather today?",
            "intent": None
        }
    ]

    print(
        "\nTesting intent-aware semantic knowledge base retrieval...\n"
    )

    for case in test_cases:

        print(
            f"Query: {case['query']}"
        )

        print(
            f"Predicted intent: {case['intent']}"
        )

        results = knowledge_base.search(
            query=case["query"],
            intent=case["intent"],
            top_k=3
        )

        if not results:
            print(
                "No sufficiently relevant KB article found."
            )

        for result in results:

            print(
                f"KB ID: {result['kb_id']}"
            )

            print(
                f"Intent: {result['intent']}"
            )

            print(
                f"Title: {result['title']}"
            )

            print(
                f"Similarity: "
                f"{result['similarity']:.4f}"
            )

            print(
                f"Intent match: "
                f"{result['intent_match']}"
            )

            print(
                f"Ranking score: "
                f"{result['ranking_score']:.4f}"
            )

            print(
                f"Escalation condition: "
                f"{result['escalation_condition']}"
            )

            print(
                "-" * 60
            )

        print(
            "=" * 60
        )