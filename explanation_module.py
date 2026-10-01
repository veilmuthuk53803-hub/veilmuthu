from functools import lru_cache

from fastapi import HTTPException

from config import settings
from gemini_client import generate_text


@lru_cache(maxsize=1)
def _local_pipeline():

    try:
        from transformers import (
            AutoTokenizer,
            AutoModelForSeq2SeqLM,
            pipeline,
        )

        tokenizer = AutoTokenizer.from_pretrained(
            settings.LOCAL_EXPLAINER_MODEL
        )

        model = AutoModelForSeq2SeqLM.from_pretrained(
            settings.LOCAL_EXPLAINER_MODEL
        )

        return pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
        )

    except Exception as exc:
        raise RuntimeError(
            f"Unable to load local explanation model: {exc}"
        )


def _local_explain(concept: str) -> str:

    generator = _local_pipeline()

    prompt = f"""
Explain the following concept to a student.

Concept:
{concept}

Use simple language.
Give the meaning, main idea, and one simple example.
"""

    result = generator(
        prompt,
        max_new_tokens=300,
        do_sample=False,
    )

    if not result:
        raise RuntimeError(
            "Local model returned no result."
        )

    return result[0]["generated_text"].strip()


def explain_concept(concept: str) -> str:

    if not settings.USE_LOCAL_EXPLAINER:
        prompt = f"""
You are EduGenie.

Explain this concept to a student in a simple,
clear and educational way.

Concept:
{concept}

Structure:
1. Simple definition
2. Explanation
3. Important points
4. Simple example
5. One-line recap

Avoid unnecessary complexity.
"""

        return generate_text(
            prompt,
            temperature=0.3,
            max_output_tokens=900,
        )

    try:
        return _local_explain(concept)

    except Exception:
        # Fallback to Gemini if the local model
        # is unavailable or fails.
        prompt = f"""
Explain the following concept clearly to a student.

Concept:
{concept}

Use simple language and include an example.
"""

        return generate_text(
            prompt,
            temperature=0.3,
            max_output_tokens=900,
        )
    
    