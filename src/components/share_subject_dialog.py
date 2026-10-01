import streamlit as st
import segno
import io

@st.dialog("Share Class Link")
def share_subject_dialog(sub_name,sub_code):
    app_domain="haazirai-main.steamlit.app"
    join_url=f"{app_domain}/?join-code={sub_code}"
    
    qr=segno.make(join_url)
    out=io.BytesIO()
    qr.save(out, kind="png", scale=10, border=1)
    
    st.header("Scan To Join")
    col1,col2=st.columns(2)
    with col1:
        st.markdown('Copy Link')
        st.code(join_url,language="text")
        st.code(sub_code,language="text")
        st.info('Copy this link to share')
    with col2:
        st.image(out.getvalue(),width='content',caption='QRCODE')
        
        
        

    