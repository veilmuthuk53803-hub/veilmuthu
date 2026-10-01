from fastapi import HTTPException
from google import genai

from config import settings
from schemas import QuizResponse


def generate_quiz(text: str) -> QuizResponse:

    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail=(
                "GEMINI_API_KEY is not configured. "
                "Add it to your .env file."
            ),
        )

    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions
from the material below.

Material:
{text}

Rules:
- Exactly 3 questions.
- Each question must have exactly 4 options.
- Only one option must be correct.
- correct_answer must exactly match one option.
- Include a short explanation for each answer.
- Questions must be based only on the supplied material.
- Avoid ambiguous questions.
- Use student-friendly language.
"""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config={
                "temperature": 0.4,
                "response_mime_type": "application/json",
                "response_schema": QuizResponse,
                "max_output_tokens": 1800,
            },
        )

        result = response.parsed

        if result is None:
            raise ValueError(
                "Gemini did not return structured quiz data."
            )

        for question in result.questions:

            if len(question.options) != 4:
                raise ValueError(
                    "Every quiz question must have 4 options."
                )

            if (
                question.correct_answer
                not in question.options
            ):
                raise ValueError(
                    "Correct answer must match one option."
                )

        return result

    except Exception as exc:

        if isinstance(exc, HTTPException):
            raise

        raise HTTPException(
            status_code=502,
            detail=f"Quiz generation failed: {exc}",
        )
    