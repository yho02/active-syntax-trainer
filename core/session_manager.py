import streamlit as st
from core import prompt_generator, level_tracker, evaluator

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
        
def question():
    st.session_state.current_prompt = prompt_generator.generate_prompt(st.session_state.current_step, st.session_state.current_level)
    return f"Here's your question for this step: {st.session_state.current_prompt}"

def save_answer(answer):
    if st.session_state.current_prompt is not None:
        st.session_state.conversation_history.append({
            "prompt": st.session_state.current_prompt,
            "answer": answer
        })

def update_step_and_level():
    feedback = evaluator.evaluate(st.session_state.conversation_history[-1]['prompt'], st.session_state.conversation_history[-1]['answer'])
    score = feedback.get('score')

    st.session_state.current_step, st.session_state.current_level = level_tracker.track_level(
        st.session_state.current_step,
        st.session_state.current_level,
        score
    )
    st.session_state.conversation_history[-1]['feedback'] = feedback
    st.session_state.current_prompt = None
