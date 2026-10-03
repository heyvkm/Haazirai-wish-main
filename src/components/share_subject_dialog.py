import streamlit as st
import segno
import io

@st.dialog("Share Class Link")
def share_subject_dialog(sub_name,sub_code):
    APP_URL = "https://haazirai-main.streamlit.app"
    join_url = f"{APP_URL}/?join-code={sub_code.upper()}"
    
    qr=segno.make(join_url)
    out=io.BytesIO()
    qr.save(out, kind="png", scale=10, border=1)
    
    st.header("Scan To Join")
    col1,col2=st.columns(2)
    with col1:
        st.markdown("### Share Link")
        st.code(join_url,language="text")
        st.code(sub_code,language="text")
        st.info("Share the link or QR code with your students.")
    with col2:
        st.image(out.getvalue(),width='content',caption='Scan the QR Code to join')
        
        
        

    