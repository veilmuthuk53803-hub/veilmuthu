from fastapi import HTTPException
from google import genai

from config import settings
from schemas import LearningPathResponse


def get_learning_recommendations(
    topic: str,
) -> LearningPathResponse:

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
You are EduGenie, a personalized learning assistant.

Create a practical learning path for:

{topic}

Requirements:
- Give the topic name.
- Provide a short overview.
- Give a realistic estimated timeline.
- Create 4 to 6 sequential learning steps.
- Each step must include:
  - level
  - topic
  - description
  - suggested_resources
- Start from fundamentals and progress toward practical use.
- Make the path suitable for self-learning.
- Do not invent URLs.
- Do not include unnecessary information.
"""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config={
                "temperature": 0.4,
                "response_mime_type": "application/json",
                "response_schema": LearningPathResponse,
                "max_output_tokens": 2200,
            },
        )

        result = response.parsed

        if result is None:
            raise ValueError(
                "Gemini did not return a learning path."
            )

        return result

    except Exception as exc:

        if isinstance(exc, HTTPException):
            raise

        raise HTTPException(
            status_code=502,
            detail=(
                f"Learning path generation failed: {exc}"
            ),
        )
    def get_learning_recommendations(topic, level="beginner"):
        """ 
        Generate learning recommendations for a given topic and level.
        """
    recommendations = {
        "beginner": [
            f"Learn the basics of {topic}",
            f"Understand the key concepts of {topic}",
            f"Practice simple {topic} exercises",
            f"Build a small {topic} project"
        ],
        "intermediate": [
            f"Study intermediate concepts of {topic}",
            f"Practice intermediate {topic} problems",
            f"Build a practical {topic} project",
            f"Review common mistakes and best practices"
        ],
        "advanced": [
            f"Study advanced concepts of {topic}",
            f"Work on complex {topic} problems",
            f"Build an advanced {topic} project",
            f"Study real-world applications of {topic}"
        ]
    }

    return recommendations.get(
        level.lower(),
        recommendations["beginner"]
    )