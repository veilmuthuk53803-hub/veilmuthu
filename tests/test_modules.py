def test_qna_module(monkeypatch):

    import qna

    monkeypatch.setattr(
        qna,
        "generate_text",
        lambda prompt, **kwargs:
            "Test answer",
    )

    result = qna.answer_question(
        "What is Python?"
    )

    assert result == "Test answer"


def test_summary_module(monkeypatch):

    import summary_module

    monkeypatch.setattr(
        summary_module,
        "generate_text",
        lambda prompt, **kwargs:
            "Test summary",
    )

    result = summary_module.summarize_text(
        "Python is a programming language."
    )

    assert result == "Test summary"
    