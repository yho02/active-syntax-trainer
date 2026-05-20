import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from core import session_manager

session_manager.init_session_state()

# 2. Display history
for entry in st.session_state.conversation_history:
    with st.chat_message("assistant"):
        st.write(f"**Question:** {entry['prompt']}")
    with st.chat_message("user"):
        st.write(f"**Your answer:** {entry['answer']}")
    with st.chat_message("assistant"):
        st.write(f"**Feedback:** {entry['feedback']} (Score: {entry['score']})")
    st.markdown("---")


# 3. Show greeting
if not st.session_state.conversation_history and st.session_state.current_prompt is None:
    with st.chat_message("assistant"):
        st.write(session_manager.greet())
        st.write(session_manager.ini_question())

# Show current_prompt if it exists AND conversation_history is not empty to avoid showing prompt twice on first load (once in greeting and once here)
# if not st.session_state.conversation_history and st.session_state.current_prompt is None:
#         with st.chat_message("assistant"):
#             st.write(f"Here's your current question: {st.session_state.current_prompt}")

# 4. Handle input
student_answer = st.chat_input("Type your answer here...")
if student_answer:
    # user submitted something
    st.chat_message("user").write(student_answer)
    response = session_manager.handle_answer(student_answer)
    with st.chat_message("assistant"):
        st.write(response)

