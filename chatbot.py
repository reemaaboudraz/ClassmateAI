"""Reema Aboudraz, 40253549
Mridul Mridul, 40279215
COMP-472 Summer 2026
Mini-Project 1 Submission"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline


@dataclass
class AssistantResponse:
    sentiment_label: str
    sentiment_score: float
    answer: str
    matched_question: str
    similarity_score: float
    matched: bool


class ClassmateAI:

    SIMILARITY_THRESHOLD = 0.4

    NO_MATCH_MESSAGE = (
        "I couldn't find an answer to that in my knowledge base. "
        "Please rephrase your question, or contact a human advisor for help."
    )

    def __init__(self, knowledge_base_path: str = "knowledge_base.csv") -> None:
        self.knowledge_base_path = Path(knowledge_base_path)
        self.questions: List[str] = []
        self.answers: List[str] = []

        self._load_knowledge_base()

        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        self.question_embeddings = self.embedding_model.encode(self.questions)

        self.sentiment_analyzer = pipeline(
            task="sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest",
        )

    def _load_knowledge_base(self) -> None:
        if not self.knowledge_base_path.exists():
            raise FileNotFoundError(
                f"Knowledge base file not found: {self.knowledge_base_path}"
            )

        try:
            data = pd.read_csv(self.knowledge_base_path)
        except pd.errors.EmptyDataError as exc:
            raise ValueError("The knowledge base CSV file is empty.") from exc
        except pd.errors.ParserError as exc:
            raise ValueError("The knowledge base CSV file could not be parsed.") from exc

        required_columns = {"question", "answer"}
        missing_columns = required_columns - set(data.columns)
        if missing_columns:
            raise ValueError(
                "The knowledge base must contain these columns: question, answer. "
                f"Missing: {', '.join(missing_columns)}"
            )

        data = data.dropna(subset=["question", "answer"])
        data["question"] = data["question"].astype(str).str.strip()
        data["answer"] = data["answer"].astype(str).str.strip()
        data = data[(data["question"] != "") & (data["answer"] != "")]
        data = data.drop_duplicates(subset=["question"])

        if data.empty:
            raise ValueError("The knowledge base does not contain valid question-answer rows.")

        self.questions = data["question"].tolist()
        self.answers = data["answer"].tolist()

    def detect_sentiment(self, user_text: str) -> Dict[str, float | str]:
        
        if not user_text.strip():
            return {"label": "NEUTRAL", "score": 1.0}

        result = self.sentiment_analyzer(user_text)[0]
        label = str(result["label"]).upper()
        score = float(result["score"])

        return {"label": label, "score": score}

    def find_best_answer(self, user_question: str) -> Dict[str, float | str]:
        
        user_embedding = self.embedding_model.encode([user_question])
        similarities = cosine_similarity(user_embedding, self.question_embeddings)[0]

        best_index = int(np.argmax(similarities))
        best_score = float(similarities[best_index])

        return {
            "answer": self.answers[best_index],
            "matched_question": self.questions[best_index],
            "similarity_score": best_score,
        }

    def respond(self, user_text: str) -> AssistantResponse:
        """Analyze sentiment and retrieve the best knowledge base answer."""
        sentiment = self.detect_sentiment(user_text)
        retrieval = self.find_best_answer(user_text)

        similarity_score = float(retrieval["similarity_score"])
        matched = similarity_score >= self.SIMILARITY_THRESHOLD
        answer = str(retrieval["answer"]) if matched else self.NO_MATCH_MESSAGE

        return AssistantResponse(
            sentiment_label=str(sentiment["label"]),
            sentiment_score=float(sentiment["score"]),
            answer=answer,
            matched_question=str(retrieval["matched_question"]),
            similarity_score=similarity_score,
            matched=matched,
        )
