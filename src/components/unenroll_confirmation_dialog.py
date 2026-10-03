import streamlit as st
from src.database.db import unenroll_student_to_subject

@st.dialog("⚠️ Confirm Unenrollment")
def unenroll_confirm_dialog(student_id, subject_id, subject_name):
    st.warning(
        f"Are you sure you want to unenroll from **{subject_name}**?"
    )

    st.info(
        "You will lose access to this subject and your attendance records for this course will no longer be visible."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancel", width='stretch'):
            st.rerun()

    with col2:
        if st.button("Yes, Unenroll",type="primary",width='stretch'):
            unenroll_student_to_subject(student_id, subject_id)
            st.toast(f"Unenrolled from {subject_name} successfully!",icon="✅")
            st.rerun()