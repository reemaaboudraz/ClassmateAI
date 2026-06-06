# ClassmateAI

ClassmateAI is a simple AI-powered student support assistant for COMP 472 Mini Project 1.

This version focuses on two required features:

1. Answer user questions from a CSV knowledge base.
2. Detect user sentiment.

# ClassmateAI

- Reema Aboudraz (40253549)
- Mridul Mridul (40279215)

## Libraries Used

- `pandas` for loading the CSV knowledge base
- `sentence-transformers` for sentence embeddings
- `scikit-learn` for cosine similarity
- `numpy` for finding the best similarity score
- `transformers` for sentiment analysis

## Project Files

```text
ClassmateAI/
├── main.py
├── chatbot.py
├── knowledge_base.csv
├── requirements.txt
└── README.md
```

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the chatbot:

```bash
python main.py
```

The first run may take longer because the AI models need to be downloaded.

## Example Usage

```text
Welcome to Student Support AI
Type 'quit' to exit.

You: I cannot access my account and I am frustrated
Sentiment: NEGATIVE (0.85)
Matched question: How do I reset my password?
Similarity score: 0.57
Answer: Visit the IT portal and select Forgot Password.

You: This is terrible i cannot access my acccount
Sentiment: NEGATIVE (0.93)
Recommended escalation: Contact human advisor.
Matched question: How do I reset my password?
Similarity score: 0.42
Answer: Visit the IT portal and select Forgot Password.

You: Where is the registrar office?
Sentiment: NEUTRAL (0.88)
Matched question: Where is the registrar office?
Similarity score: 1.00
Answer: The registrar office is located in Building MB, room 2.145.

You: Everything is so nice about this university.
Sentiment: POSITIVE (0.97)
Answer: I couldn't find an answer to that in my knowledge base. Please rephrase your question, or contact a human advisor for help.
```

## Notes
