import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_agent(prompt = None):
    response=client.models.generate_content(
        model="gemini-2.5-flash-lite", contents = prompt
    )
    return(response.text)