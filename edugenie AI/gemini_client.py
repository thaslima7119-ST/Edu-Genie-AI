import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load .env
load_dotenv()


# Get API key
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()


# Gemini model
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


# Create ONE Gemini client
# Keep it alive while the FastAPI application is running
_client = None


def get_client():

    global _client

    if not API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    if _client is None:
        _client = genai.Client(
            api_key=API_KEY
        )

    return _client


def generate_text(
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 2048,
    response_mime_type: str | None = None,
) -> str:

    config_kwargs = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }


    if system_instruction:

        config_kwargs[
            "system_instruction"
        ] = system_instruction


    if response_mime_type:

        config_kwargs[
            "response_mime_type"
        ] = response_mime_type


    config = types.GenerateContentConfig(
        **config_kwargs
    )


    # Reuse the same client
    client = get_client()


    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )


    text = (
        response.text or ""
    ).strip()


    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    return text