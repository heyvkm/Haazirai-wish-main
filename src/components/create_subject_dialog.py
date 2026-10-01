import streamlit as st
from src.database.db import create_subjects

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details Of new subject")
    
    sub_name = st.text_input("Subject Name", placeholder="e.g. Introduction to Computer Science")
    sub_code = st.text_input("Subject Code", placeholder="e.g. CS-101")
    sub_section = st.text_input("Section",placeholder="e.g. A")
    
    st.divider()
    
    if st.button("Create Subject Now",type='primary', width='stretch'):
        if sub_name and sub_code and sub_section:
            try:
                create_subjects(sub_code,sub_name,sub_section,teacher_id)
                st.toast("Subject created successfully!")
                import time
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error (f"Error:{str(e)}") 
        else:
            st.warning("Plz fill all the fields")
