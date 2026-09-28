from gemini_client import generate_text


def explain_topic(topic: str) -> str:

    prompt = f"""
Explain the following topic to a beginner:

{topic}

Use this structure:

1. Simple definition
2. How it works / key idea
3. A relatable example
4. Three key points to remember

Avoid unnecessary jargon.
If a technical term is essential, define it clearly.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie, an expert teacher who makes "
            "complex concepts easy to understand."
        ),
        temperature=0.35,
        max_output_tokens=1400,
    )