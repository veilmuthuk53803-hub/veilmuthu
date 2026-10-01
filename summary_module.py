def summarize_text(text: str) -> str:
    """
    Create a simple summary from the supplied text.
    """

    if not text or not text.strip():
        return ""

    text = text.strip()

    # Split the text into sentences.
    sentences = [
        sentence.strip()
        for sentence in text.replace("!", ".").replace("?", ".").split(".")
        if sentence.strip()
    ]

    # Return the first few sentences as a simple summary.
    if len(sentences) <= 3:
        return ". ".join(sentences) + ("." if sentences else "")

    return ". ".join(sentences[:3]) + "."
