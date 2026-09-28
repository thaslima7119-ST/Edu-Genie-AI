from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    hours_per_week: int = 5,
) -> str:

    prompt = f"""
Create a learning path for the following topic:

Topic:
{topic}

Student level:
{level}

Study time:
{hours_per_week} hours per week

Include:

1. Learning goal
2. Beginner stage
3. Intermediate stage
4. Advanced stage
5. Topics in the correct order
6. Suggested timeline
7. Practice activities
8. Small projects
9. Progress checking methods
10. Useful resource types

Make the plan practical and easy for a student to follow.
Do not invent specific URLs.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie, a learning-path designer "
            "who creates practical study plans."
        ),
        temperature=0.45,
        max_output_tokens=2200,
    )