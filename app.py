import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen

def main():
    # st.session_state['login_type']=None
    # its type of dict that store state
    # https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    
    st.set_page_config(
        page_title='Haazir AI - Making Attendance faster using Ai',
        page_icon="https://i.ibb.co/gL8QsZxd/logo.png"
    )
    
    if 'login_type' not in st.session_state: #when app open by default empty so check
        st.session_state['login_type'] = None
        
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()
        
        
main()