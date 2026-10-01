import streamlit as st

from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard

def teacher_screen():

    style_base_layout()
    style_background_dashboard()

    
    
    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()
    
    
  
 
def teacher_screen_login():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home',key='loginbackbtn'):
            st.session_state['login_type']=None
            st.rerun()
            
            
    st.header('Login using password',text_alignment='center')
    st.space()
    st.space()
    
    teacher_username=st.text_input("Enter username",placeholder='@wish')
    teacher_pass=st.text_input("Enter password",type='password',placeholder='Enter your password')
    
    st.divider()
    
    btn1,btn2=st.columns(2)
    with btn1:
        st.button('Login',icon=':material/passkey:', width='stretch')
    with btn2:
        if st.button('Register Instead',icon=':material/passkey:',type='primary',width='stretch'):
            st.session_state.teacher_login_type='register'
            
        
        
def teacher_screen_register():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home',key='loginbackbtn'):
            st.session_state['login_type']=None
            st.rerun()
            
            
    st.header('Register your teacher profile')
    st.space()
    #st.space()
    
    teacher_username=st.text_input("Enter username",placeholder='@wish')
    teacher_name=st.text_input("Enter name",placeholder='wish')
    teacher_pass=st.text_input("Enter password",type='password',placeholder='Enter your password')
    teacher_pass_confirm=st.text_input("Confirm password",type='password',placeholder='Confirm your password')
    
    st.divider()
    
    btn1,btn2=st.columns(2)
    with btn1:
        if st.button('Register Now',icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type='login'
    with btn2:
        if st.button('Login Instead',icon=':material/passkey:',type='primary',width='stretch'):
            st.session_state.teacher_login_type='login'
        
        
        
        
    