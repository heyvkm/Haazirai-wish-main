import streamlit as st

def header_home():
    
    logo_url="https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style='display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:30px; margin-bottom:45px;'>       
            <img src='{logo_url}' style='height:100px'/>
            <h1 style='text-algin:center; color:#E0E3FF'>SNAP AI</h1>
        </div>       
                """,unsafe_allow_html=True)
    