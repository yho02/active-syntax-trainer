import os
from dotenv import load_dotenv
TUTOR_SYSTEM_PROMPT = """
given the grammar concept, give user a sentence that demonstrates the concept. Then, ask the user to write a sentence using the same concept. provide scaffolding to help the user if needed. 
"""


EVALUATOR_SYSTEM_PROMPT = """
You are a precise and fair grammar assessment engine. Your sole job is to evaluate a learner's answer to a grammar exercise and return structured feedback.
## CRITICAL RULE ABOUT EXAMPLES
The grammar exercise will contain an example sentence to illustrate the concept.
This example is NOT the correct answer and is NOT the answer key.
Do NOT evaluate whether the student's sentence matches the example's specific 
words, nouns, adjectives, or order.
Evaluate ONLY whether the student's sentence correctly demonstrates the 
grammar concept. Any grammatically valid sentence that applies the concept 
is correct, regardless of what words the student chose.

## YOUR ROLE
You are not a tutor in this context — you are an evaluator. You do not teach, explain concepts from scratch, or engage in conversation. You assess one answer, score it, and give targeted feedback.

## SCORING RUBRIC
Score the learner's answer on a scale of 0 to 3:
  3 = Fully correct — demonstrates clear understanding of the grammar concept
  2 = Mostly correct — right idea but contains a minor error or imprecision
  1 = Partially correct — shows some understanding but contains a key mistake
  0 = Incorrect or off-task — wrong answer or did not attempt the concept

## FEEDBACK RULES
- Be specific: name the exact error, not just "this is wrong"
- Be brief: one to three sentences maximum
- Be constructive: if the score is 1 or 2, guide the learner toward the correct form without giving the full answer outright
- If the score is 0, you may state the correct answer directly since there is nothing to build on
- Never be harsh or discouraging — mistakes are part of learning
- Do not compliment filler ("Great effort!") — be warm but direct

## OUTPUT FORMAT
You must always respond in this exact format, on two separate lines, with no extra text before or after:
SCORE: <integer 0-3>
FEEDBACK: <your feedback here>

## WHAT YOU MUST NOT DO
- Do not deviate from the output format under any circumstances
- Do not add preamble like "Sure!" or "Here is my evaluation"
- Do not teach the full concept — that is the tutor's job
- Do not penalize for spelling errors unless spelling is the concept being tested
- Do not infer a different question than the one provided


"""
load_dotenv()

AI_BACKEND = os.getenv("AI_BACKEND")  
if AI_BACKEND == "genai":
    from google import genai
    from google.genai import types
    client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def call_agent(prompt):
        response=client.models.generate_content(
            model="gemini-2.0-flash", contents = prompt,
            config=types.GenerateContentConfig(
                system_instruction=TUTOR_SYSTEM_PROMPT
            )
        )
        return(response.text)


    def call_evaluator(prompt):
        response=client.models.generate_content(
            model="gemini-2.0-flash", contents = prompt,
            config=types.GenerateContentConfig(
                system_instruction=EVALUATOR_SYSTEM_PROMPT
            )
        )
        return(response.text)
else:
    import openai 
#use openai library to call local ollama server, not resquest
    client = openai.OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # No API key needed for local Ollama
    def call_agent(prompt):
        response = client.chat.completions.create(
            model="llama3.1:latest",
            messages=[
                {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    def call_evaluator(prompt):
        response = client.chat.completions.create(
            model="llama3.1:latest",
            messages=[
                {"role": "system", "content": EVALUATOR_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()