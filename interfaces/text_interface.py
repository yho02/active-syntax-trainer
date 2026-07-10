import streamlit as st
from core import session_manager
from core import grammar_engine

def show():
    with st.sidebar:
        st.header("Your Progress")
        st.metric(label = "Current Level", value = st.session_state.current_level)
        total_steps = grammar_engine.get_total_steps(st.session_state.current_level)

        st.write(f"Step {st.session_state.current_step} out of {total_steps}")

        progress_ratio = st.session_state.current_step / total_steps
        st.progress(progress_ratio)
        
        st.divider()

        # sign out
        if st.button("Sign Out"):
            session_manager.sign_out()
            st.rerun()

    student_answer = st.chat_input("Type your answer here...")

    # 2. Display History (The Past)
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