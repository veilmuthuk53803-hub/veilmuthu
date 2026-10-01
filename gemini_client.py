import os
import time
from typing import Optional

from click import prompt

try:
    from google import genai
except ImportError:
    genai = None


_client = None


def _get_client():
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
        )

    if genai is None:
        raise RuntimeError(
            "The google-genai package is not installed. "
            "Run: pip install google-genai"
        )

    _client = genai.Client(api_key=api_key)

    return _client


def generate_text(
    prompt: str,
    model: Optional[str] = None,
) -> str:
    """
    Generate text using Google Gemini.

    Parameters
    ----------
    prompt:
        Prompt sent to Gemini.

    model:
        Optional Gemini model name.

    Returns
    -------
    str
        Generated text.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    client = _get_client()

    model_name = model or os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash",
    )

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()
last_error = None

for attempt in range(4):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        break
    except Exception as exc:
        last_error = exc

        if attempt == 3:
            raise

        time.sleep(2 ** attempt)