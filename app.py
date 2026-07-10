from core import session_manager
import streamlit as st
from interfaces import auth_interface, text_interface

session_manager.init_session_state()

if st.session_state.student_id is None:
    auth_interface.show()
else:
    text_interface.show()

