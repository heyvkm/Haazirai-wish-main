import streamlit as st

from src.components.header import header_home

from src.ui.base_layout import style_base_layout,style_background_home

def home_screen():
   # st.header('Home Screen')
    
    
    
    style_background_home()
    style_base_layout()
    header_home()
    
    col1,col2=st.columns(2,gap="large")
    
    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/YFkp46cF/Student.png",width=150)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()
        
        
    with col2:     
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/QvQkj2zk/Teacher.png",width=150)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='teacher'
            st.rerun()