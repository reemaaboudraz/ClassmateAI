"""Reema Aboudraz, 40253549
Mridul Mridul, 40279215
COMP-472 Summer 2026
Mini-Project 1 Submission"""


from chatbot import ClassmateAI


def print_welcome_banner():
    banner = r"""
🌸🐱🌸🐱🌸🐱🌸🐱🌸🐱🌸🐱🌸

          Welcome to ClassmateAI
              made by
      Reema Aboudraz & Mridul Mridul

🐾 Your friendly student support assistant
🌷 Ask a question, and ClassmateAI will help!

Type 'quit' anytime to exit.

🌸🐱🌸🐱🌸🐱🌸🐱🌸🐱🌸🐱🌸
"""
    print(banner)


def print_assistant_response(response):

    print(f"Sentiment: {response.sentiment_label} ({response.sentiment_score:.3f})")

    if response.escalated:
        print("Recommended escalation: Contact human advisor.")

    if response.matched:
        print(f"Matched question: {response.matched_question}")
        print(f"Similarity score: {response.similarity_score:.2f}")

    print(f"Answer: {response.answer}\n")


def print_conversation_summary(history):

    if not history:
        print("No conversation history to summarize.")
        return

    print("\n🌸🐱 Conversation Summary 🐱🌸\n")

    for index, response in enumerate(history, start=1):
        print(f"Exchange {index}:")
        print(f"  You: {response.user_input}")
        print(
            f"  Sentiment: {response.sentiment_label} "
            f"({response.sentiment_score:.3f})"
        )
        if response.matched:
            print(f"  Matched question: {response.matched_question}")
            print(f"  Similarity score: {response.similarity_score:.2f}")
        print(f"  Answer: {response.answer}")
        if response.escalated:
            print("  ⚠️  This exchange was flagged for escalation.")
        print()

    total = len(history)
    negative = sum(1 for response in history if response.sentiment_label == "NEGATIVE")
    escalations = sum(1 for response in history if response.escalated)

    print(f"Total exchanges: {total}")
    print(f"Negative exchanges: {negative} ({(negative / total) * 100:.1f}%)")
    print(f"Escalations recommended: {escalations}")


def main():
    try:
        assistant = ClassmateAI("knowledge_base.csv")

    except FileNotFoundError:
        print("Error: knowledge_base.csv was not found.")
        print("Please make sure the file is in the same folder as main.py.")
        return

    except ValueError as error:
        print(f"Error loading knowledge base: {error}")
        return

    except Exception as error:
        print(f"Unexpected error while starting ClassmateAI: {error}")
        return

    print_welcome_banner()

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == "quit":
                print("\n🐱 Goodbye from ClassmateAI! 🌸")
                print_conversation_summary(assistant.history)
                break

            if not user_input:
                print("Please enter a question, or type 'quit' to exit.\n")
                continue

            response = assistant.respond(user_input)
            print_assistant_response(response)

        except KeyboardInterrupt:
            print("\n\nClassmateAI was closed. Goodbye! 🌸")
            print_conversation_summary(assistant.history)
            break

        except Exception as error:
            print(f"An error occurred while processing your question: {error}")


if __name__ == "__main__":
    main()