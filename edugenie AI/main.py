from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# Load .env
load_dotenv()


# Project directory
BASE_DIR = Path(__file__).resolve().parent


# Create FastAPI app
app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="AI-powered educational learning assistant",
)


# Static folder
app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static")
    ),
    name="static",
)


# Templates folder
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# Request model
class TextRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# --------------------------------------------------
# QUESTION & ANSWER
# --------------------------------------------------

@app.post("/qa")
async def qa(payload: TextRequest):

    try:

        result = answer_question(
            payload.text
        )

        return {
            "answer": result
        }

    except Exception as e:

        print(
            "GEMINI QA ERROR:",
            repr(e)
        )

        return {
            "detail":
                f"Gemini Error: {str(e)}"
        }


# --------------------------------------------------
# EXPLAIN TOPIC
# --------------------------------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    try:

        result = explain_topic(
            payload.text
        )

        return {
            "explanation": result
        }

    except Exception as e:

        print(
            "GEMINI EXPLAIN ERROR:",
            repr(e)
        )

        return {
            "detail":
                f"Gemini Error: {str(e)}"
        }


# --------------------------------------------------
# GENERATE QUIZ
# --------------------------------------------------

@app.post("/quiz")
async def quiz(payload: TextRequest):

    try:

        result = generate_quiz(
            payload.text
        )

        return {
            "quiz": result
        }

    except Exception as e:

        print(
            "GEMINI QUIZ ERROR:",
            repr(e)
        )

        return {
            "detail":
                f"Gemini Error: {str(e)}"
        }


# --------------------------------------------------
# SUMMARIZE
# --------------------------------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    try:

        result = summarize_text(
            payload.text
        )

        return {
            "summary": result
        }

    except Exception as e:

        print(
            "GEMINI SUMMARY ERROR:",
            repr(e)
        )

        return {
            "detail":
                f"Gemini Error: {str(e)}"
        }


# --------------------------------------------------
# LEARNING RECOMMENDATIONS
# --------------------------------------------------

@app.post("/learn/recommendations")
async def recommendations(
    payload: TextRequest
):

    try:

        result = get_learning_recommendations(
            payload.text
        )

        return {
            "recommendations": result
        }

    except Exception as e:

        print(
            "GEMINI RECOMMENDATION ERROR:",
            repr(e)
        )

        return {
            "detail":
                f"Gemini Error: {str(e)}"
        }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok"
    }