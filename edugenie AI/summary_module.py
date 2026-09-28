from gemini_client import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the educational passage below.

PASSAGE:

{text}

Requirements:

- Preserve the important facts.
- Remove repetition.
- Use simple language.
- Use headings or bullet points when useful.
- Keep it concise.
- Do not add unsupported information.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie, a precise educational "
            "summarization assistant."
        ),
        temperature=0.25,
        max_output_tokens=1800,
    )