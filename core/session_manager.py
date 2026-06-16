import streamlit as st
from core import prompt_generator, level_tracker, evaluator
from services import supabase_service

def init_session_state():
    defaults = {
        'current_step': 1,
        'current_level': "A1",
        'student_id': None,
        'current_prompt': None,
        'conversation_history': []

    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def greet():    
    if st.session_state.current_step == 1:
        return f"Welcome to Active Syntax Trainer! Let's start your English grammar journey at level {st.session_state.current_level}. I'll guide you through each step with clear explanations and examples. Just follow along and don't worry about making mistakes — we're here to learn together!"
    else:
        return f"Welcome back! You're currently on step {st.session_state.current_step} of level {st.session_state.current_level}. Let's continue building your grammar skills together. Remember, every step forward is progress, so keep up the great work!"
        
def ini_question():
    #generate first question when student first arrives or refreshes page
    st.session_state.current_prompt = prompt_generator.generate_prompt(st.session_state.current_step, st.session_state.current_level)
    return f"Here's your question for this step: {st.session_state.current_prompt}"

def handle_answer(answer):
    # 1. Evaluate immediately using the variables already available
    evaluation = evaluator.evaluate(answer, st.session_state.current_prompt)
    feedback = evaluation.get('feedback')
    score = evaluation.get('score')
    
    # 2. Save the COMPLETE interaction to history just for the UI to read later
    st.session_state.conversation_history.append({
        "prompt": st.session_state.current_prompt,
        "answer": answer,
        "feedback": feedback,
        "score": score
    })
    
    # 3. Decide what to do next based on the score
    if score == 3:
        st.session_state.current_step, st.session_state.current_level = level_tracker.track_level(
            st.session_state.current_step,
            st.session_state.current_level,
            score
        )           
        
        # Generate the next question
        next_prompt = prompt_generator.generate_prompt(st.session_state.current_step, st.session_state.current_level)
        st.session_state.current_prompt = next_prompt

        response = f"{feedback}. Let's move on to the next question: {next_prompt}"
        
    elif score <= 2:
        response = feedback
    
    update_response = supabase_service.update_progress(
        st.session_state.student_id,
        st.session_state.current_level,
        st.session_state.current_step,
        st.session_state.current_prompt
    )

    return response

def sign_in(email, password):
    # take email and password from UI, validate with Supabase
    # if valid, load student's progress in session state
    response = supabase_service.sign_in_with_password(email, password)
    if 'error' in response:
        return f"Sign in failed: {response['error']}"
    else:
        st.session_state.student_id = response.user.id
        progress_response = supabase_service.get_progress(st.session_state.student_id)
        if 'error' in progress_response:
            return f"Failed to load progress: {progress_response['error']}"
        else:
            progress_data = progress_response.data
            if progress_data:
                st.session_state.current_level = progress_data[0]['current_level']
                st.session_state.current_step = progress_data[0]['current_step']
                st.session_state.current_prompt = progress_data[0]['current_prompt']
            else:
                # If no progress exists, create a new entry
                supabase_service.create_progress(st.session_state.student_id)
            return "Sign in successful! Progress loaded."

def sign_up(email, password, name):
    # take email, password, and name from UI, create account with Supabase
    response = supabase_service.sign_up(email, password, name)
    if 'error' in response:
        return f"Sign up failed: {response['error']}"
    else:
        # create student progress entry in database with default values (A1, step 1, empty prompt)
        st.session_state.student_id = response.user.id

        create_response = supabase_service.create_progress(st.session_state.student_id)
        if 'error' in create_response:
            return f"Sign up failed: could not create progress record: {create_response['error']}"

        progress = supabase_service.get_progress(st.session_state.student_id)
        if 'error' in progress:
            return f"Sign up failed: could not load progress: {progress['error']}"

        st.session_state.current_level = progress.data[0]['current_level']
        st.session_state.current_step = progress.data[0]['current_step']
        st.session_state.current_prompt = progress.data[0]['current_prompt']
        return "Sign up successful! Let's start your English journey."