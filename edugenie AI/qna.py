from gemini_client import generate_text


def answer_question(question: str) -> str:

    prompt = f"""
Answer the student's question accurately and clearly.

Question:
{question}

Requirements:
- Give the direct answer first.
- Explain it in simple language.
- Break difficult concepts into easy points.
- Give an example when useful.
- Do not invent facts.
- If the question is unclear, mention the assumption.
- Keep the answer suitable for a student.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie, a friendly academic assistant. "
            "Help students understand concepts clearly."
        ),
        temperature=0.3,
        max_output_tokens=1200,
    )