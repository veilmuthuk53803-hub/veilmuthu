from typing import List

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000,
        description="Text or topic supplied by the user.",
    )


class QAResponse(BaseModel):
    answer: str


class ExplanationResponse(BaseModel):
    explanation: str


class SummaryResponse(BaseModel):
    summary: str


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(
        ...,
        min_length=4,
        max_length=4,
    )
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(
        ...,
        min_length=3,
        max_length=3,
    )


class LearningStep(BaseModel):
    level: str
    topic: str
    description: str
    suggested_resources: List[str] = Field(
        default_factory=list
    )


class LearningPathResponse(BaseModel):
    topic: str
    overview: str
    estimated_timeline: str
    steps: List[LearningStep] = Field(
        ...,
        min_length=4,
        max_length=6,
    )


class HealthResponse(BaseModel):
    status: str
    service: str
    