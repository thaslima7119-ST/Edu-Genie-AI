import json
import re

from gemini_client import generate_text


def extract_json(text: str):

    cleaned = text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:

        start = cleaned.find("[")

        end = cleaned.rfind("]")

        if start >= 0 and end > start:
            return json.loads(
                cleaned[start:end + 1]
            )

        raise ValueError(
            "Gemini returned invalid quiz JSON."
        )


def generate_quiz(
    text: str,
    count: int = 3
):

    prompt = f"""
Create exactly {count} multiple-choice questions
from the educational content below.

CONTENT:

{text}

Return ONLY valid JSON.

Use exactly this format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Option A",
    "explanation": "Short explanation"
  }}
]

Rules:

- Exactly {count} questions.
- Exactly four options for each question.
- Only one correct answer.
- Questions must be answerable from the content.
- Make distractors reasonable.
- Do not add Markdown.
"""


    raw = generate_text(
        prompt,
        system_instruction=(
            "You create educational multiple-choice questions "
            "and always return valid JSON."
        ),
        temperature=0.4,
        max_output_tokens=2500,
        response_mime_type="application/json",
    )

    data = extract_json(raw)

    if not isinstance(data, list):
        raise ValueError(
            "Quiz response is not a list."
        )

    questions = []

    for item in data[:count]:

        if not isinstance(item, dict):
            continue

        question = str(
            item.get("question", "")
        ).strip()

        options = item.get(
            "options",
            []
        )

        correct_answer = str(
            item.get(
                "correct_answer",
                ""
            )
        ).strip()

        explanation = str(
            item.get(
                "explanation",
                ""
            )
        ).strip()

        if (
            question
            and isinstance(options, list)
            and len(options) == 4
            and correct_answer in options
        ):
            questions.append({
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation,
            })

    if len(questions) < count:
        raise ValueError(
            "Gemini returned an incomplete quiz. "
            "Please try again."
        )

    return questions