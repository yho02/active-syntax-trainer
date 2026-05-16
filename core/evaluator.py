# evaluator.py
from services import ai_service

def evaluate(student_answer: str, original_prompt: str) -> dict:
    eval_prompt = (
        f"A learner was given this grammar exercise:\n"
        f"\"{original_prompt}\"\n\n"
        f"The learner responded with:\n"
        f"\"{student_answer}\"\n\n"
        f"Evaluate their answer. Respond in this exact format:\n"
        f"SCORE: <a number from 0 to 3>\n"
        f"FEEDBACK: <one to three sentences of feedback>\n\n"
        f"Scoring guide:\n"
        f"  3 = Fully correct, demonstrates clear understanding\n"
        f"  2 = Mostly correct, minor error or imprecision\n"
        f"  1 = Partially correct, shows some understanding but a key mistake\n"
        f"  0 = Incorrect or off-task\n\n"
        f"Give honest, specific feedback. If there is an error, explain it clearly "
        f"and briefly suggest how to fix it. Do not give the corrected answer outright "
        f"unless the score is 0 — instead, guide the learner toward it."
    )

    raw = ai_service.call_evaluator(eval_prompt)

    score = None
    feedback = ""

    for line in raw.strip().splitlines():
        if line.startswith("SCORE:"):
            try:
                score = int(line.replace("SCORE:", "").strip())
            except ValueError:
                score = None
        elif line.startswith("FEEDBACK:"):
            feedback = line.replace("FEEDBACK:", "").strip()

    return {
        "score": score,
        "feedback": feedback,
        "raw": raw  # keep the raw response for debugging
    }