from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    TextRequest,
    QAResponse,
    ExplanationResponse,
    QuizResponse,
    SummaryResponse,
    LearningPathResponse,
    HealthResponse,
)

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static")
    ),
    name="static",
)


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "EduGenie",
        },
    )


@app.get(
    "/health",
    response_model=HealthResponse
)
async def health():

    return HealthResponse(
        status="ok",
        service="EduGenie",
    )


@app.post(
    "/qa",
    response_model=QAResponse
)
async def qa(request: TextRequest):

    answer = answer_question(
        request.text
    )

    return QAResponse(
        answer=answer
    )


@app.post(
    "/explain",
    response_model=ExplanationResponse
)
async def explain(request: TextRequest):

    explanation = explain_concept(
        request.text
    )

    return ExplanationResponse(
        explanation=explanation
    )


@app.post(
    "/quiz",
    response_model=QuizResponse
)
async def quiz(request: TextRequest):

    return generate_quiz(
        request.text
    )


@app.post(
    "/summarize",
    response_model=SummaryResponse
)
async def summarize(request: TextRequest):

    summary = summarize_text(
        request.text
    )

    return SummaryResponse(
        summary=summary
    )


@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse
)
async def recommendations(
    request: TextRequest
):

    return get_learning_recommendations(
        request.text
    )
