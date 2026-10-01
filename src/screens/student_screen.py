import streamlit as st
import numpy as np

from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from PIL import Image

def student_screen():
    
    style_base_layout()
    style_background_dashboard()
        
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home',key='loginbackbtn'):
            st.session_state['login_type']=None
            st.rerun()
            
            
    st.header('Login using FaceID',text_alignment='center')
    st.space()
    st.space()
    
    photo_src=st.camera_input("Position your face in the center")
    
    if photo_src:
        np.array(Image.open(photo_src))