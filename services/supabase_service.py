import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

#add try/except for all functions to catch errors and return them as response

def sign_up(email, password,name):
    try:
        response = client.auth.sign_up(email=email, password=password, options={"data": {"name": name}})
        return response
    except Exception as e:
        return {"error": str(e)}

def sign_in_with_password(email, password):
    try:
        response = client.auth.sign_in_with_password(email=email, password=password)
        return response
    except Exception as e:
        return {"error": str(e)}

#student start with A1 and step1, and empty prompt for first time sign in 
def create_progress(student_id):
    try:
        response = client.from_("progress").insert({
            "student_id": student_id
        }).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

def get_progress(student_id):
    try:
        response = client.from_("progress").select("*").eq("student_id", student_id).execute()
        return response
    except Exception as e:
        return {"error": str(e)}

def update_progress(student_id, current_level, current_step, current_prompt):
    try:
        response = client.from_("progress").update({
            "current_level": current_level,
            "current_step": current_step,
            "current_prompt": current_prompt
        }).eq("student_id", student_id).execute()
        return response
    except Exception as e:
        return {"error": str(e)}