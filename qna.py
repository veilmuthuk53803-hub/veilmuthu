from gemini_client import generate_text


def answer_question(question: str) -> str:
    """
    Answer a user's educational question using the configured AI model.
    """

    if not question or not question.strip():
        return "Please enter a question."

    prompt = f"""
You are EduGenie AI, an educational assistant.

Answer the student's question clearly and accurately.

Rules:
- Explain the concept in simple language.
- Use examples when useful.
- Break difficult concepts into steps.
- Do not invent facts.
- If the question is unclear, explain what information is missing.

Student question:
{question.strip()}
"""

    try:
        response = generate_text(prompt)

        if not response:
            return "I could not generate an answer right now."

        return response.strip()

    except Exception as exc:
        return f"Unable to generate an answer: {exc}"
    