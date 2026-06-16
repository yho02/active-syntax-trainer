import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from core import session_manager

session_manager.init_session_state()

# 1. validate sign in or sign up, use st.form instead of individual input and button to avoid multiple calls to supabase when user is typing in the input fields. Only call supabase when the form is submitted.
if st.session_state.student_id is None:
    with st.form("auth_form"):
        st.write("Please sign in or sign up to continue.")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        name = st.text_input("Name (for sign up)")
        col1, col2 = st.columns(2)
        with col1:
            sign_in_button = st.form_submit_button("Sign In")
        with col2:
            sign_up_button = st.form_submit_button("Sign Up")

    if sign_in_button: 
        response = session_manager.sign_in(email, password)
        if "successful" in response:
            st.rerun()  # Refresh the page to load progress and display the main interface
        else:
            st.error(response)

    if sign_up_button:
        response = session_manager.sign_up(email, password, name)
        if "successful" in response:
            st.rerun()  # Refresh the page to load progress and display the main interface
        else:
            st.error(response)
else:
    # 2. Handle input (Capture it first!)
    student_answer = st.chat_input("Type your answer here...")

    # 3. Display History (The Past)
    for entry in st.session_state.conversation_history:
        with st.chat_message("assistant"):
            st.write(f"**Question:** {entry['prompt']}")
        with st.chat_message("user"):
            st.write(f"**Your answer:** {entry['answer']}")
        with st.chat_message("assistant"):
            st.write(f"**Feedback:** {entry['feedback']} (Score: {entry['score']})")
        st.markdown("---")

    # 4. Display the Present (Greeting & Active Prompt)
    if not student_answer:
        # The user is just looking at the screen, so show them the active question
        with st.chat_message("assistant"):
            # Show greeting only if it's their very first time
            if not st.session_state.conversation_history:
                st.write(session_manager.greet())
            
            # Ensure a prompt exists (fallback just in case)
            if not st.session_state.current_prompt:
                session_manager.ini_question()
            
            st.write(f"**Current Question:** {st.session_state.current_prompt}")
            
    else:
        # 5. The user just hit submit!
        with st.chat_message("user"):
            st.write(student_answer)
        
        # Evaluate and show the result immediately
        response = session_manager.handle_answer(student_answer)
        with st.chat_message("assistant"):
            st.write(response)