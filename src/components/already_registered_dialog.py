import streamlit as st
import time

@st.dialog("Already Registered")
def already_registered_dialog(student):

    st.success(f"Welcome back, {student['name']}! \n\nYour account already exists.")

    # st.info(
    #     "Your account is already registered.\n\n"
    #     "Close this dialog (❌) to continue."
    # )

    st.session_state.is_logged_in = True
    st.session_state.user_role = "student"
    st.session_state.student_data = student

    time.sleep(3)
    st.rerun()