import streamlit as st

from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.database.db import create_teacher,check_teacher_exists,teacher_login,get_teacher_subjects
from src.components.create_subject_dialog import create_subject_dialog
from src.components.share_subject_dialog import share_subject_dialog
from src.components.subject_card import subject_card
from src.components.add_photo_dialog import add_photo_dialog
def teacher_screen():

    style_base_layout()
    style_background_dashboard()

    
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()
    

def  teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']}""")
        if st.button('Logout',key='loginbackbtn'):
            st.session_state['login_type']=None
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()
            
    st.space()
    
    
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab='take_attendance'
    
    
    tab1,tab2,tab3=st.columns(3)
    with tab1:
        type1="primary" if st.session_state.current_teacher_tab=='take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1,width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab='take_attendance'
            st.rerun()
    
    with tab2:
        type2="primary" if st.session_state.current_teacher_tab=='manage_subjects' else "tertiary"
        if st.button('Manage_Subject',type=type2,width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab='manage_subjects'
            st.rerun()
    
    with tab3:
        type3="primary" if st.session_state.current_teacher_tab=='attendance_records' else "tertiary"
        if st.button('Attendance Records',type=type3,width='stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab='attendance_records'
            st.rerun()
            
        
    if st.session_state.current_teacher_tab=='take_attendance':
        teacher_tab_take_attendance()
        
    if st.session_state.current_teacher_tab=='manage_subjects':
        teacher_tab_manage_subjects()
        
    if st.session_state.current_teacher_tab=='attendance_records':
        teacher_tab_attendance_records()
        
        
def teacher_tab_take_attendance():
    st.header('Take Attendance')
    
    teacher_id=st.session_state.teacher_data['teacher_id']
    
    if 'attendance_image' not in st.session_state:
        st.session_state.attendance_image=[]
    
    subjects=get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning('You havent created any subject ! Plz create one to began!')
        
    subjects_options={f"{s['name']}-{s['subject_code']}":s['subject_id'] for s in subjects}
        
        
    col1,col2=st.columns([3,1])
    with col1:
        selected_subject_labels=st.selectbox('Select Subject',options=list(subjects_options.keys()))
        
    with col2:
        if st.button('Add Photo',type='primary',width='stretch' ,icon=':material/photo_auto_merge:'):
            add_photo_dialog()
    
    selected_subject_id=subjects_options[selected_subject_labels]
    
    st.divider()
        
    
    
    
    
    
def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data['teacher_id']
    col1,col2=st.columns(2)
    with col1:
        st.header('Manage Subjects')
    with col2:
        if st.button('Create New Subject',width='stretch'):
            create_subject_dialog(teacher_id)
            
    
    #All Subject
    subjects=get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👤", "Students", sub['total_students']),
                ("⏰", "Classes", sub['total_classes']),
            ]
        
            def share_btn(name, code):
              share_subject_dialog(name, code)
        
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("No SUBJECT FOUND. CREATE IT..")
            
    
    
    
def teacher_tab_attendance_records():
    st.header('Attendance Records')
        
    
    

def login_teacher(username,password):
    if not username or  not password:
        return False
        
    teacher=teacher_login(username,password)
    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if teacher_pass!=teacher_pass_confirm:
        return False,"Password doesn't match"
        
    if not teacher_username or not  teacher_name or not teacher_pass:
        return False,"All Fields are required!"
    
    if check_teacher_exists(teacher_username):
        return False,"Username already taken!"
    
    
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True, "registered successfully! Login Now!"
        
    except  Exception as e:
        return False,"Unexpected Error!"
    
        
  
 
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
        if st.button('Login',icon=':material/passkey:', width='stretch',shortcut="Enter"):
            if login_teacher(teacher_username,teacher_pass):
                st.toast(f"Welcome back ")
                import time
                time.sleep(1)
                st.rerun()   
            else:
                st.error("Invalid username & password")
            
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
            success,message=register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(1)
                st.session_state.teacher_login_type="login"
                st.rerun()   
            else:
                st.error(message)
    with btn2:
        if st.button('Login Instead',icon=':material/passkey:',type='primary',width='stretch'):
            st.session_state.teacher_login_type='login'
        
        
        
        
    