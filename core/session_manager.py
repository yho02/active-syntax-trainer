import streamlit as st

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

def greet_student():
    if st.session_state.current_step == 1:
        st.write(f"Welcome to Active Syntax Trainer! Let's start your English grammar journey at level {st.session_state.current_level}. I'll guide you through each step with clear explanations and examples. Just follow along and don't worry about making mistakes — we're here to learn together!"
    )
    else:
        st.write(f"Welcome back! You're currently on step {st.session_state.current_step} of level {st.session_state.current_level}. Let's continue building your grammar skills together. Remember, every step forward is progress, so keep up the great work!"
    )