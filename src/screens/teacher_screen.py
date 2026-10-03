import streamlit as st

from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.database.db import create_teacher,check_teacher_exists,teacher_login,get_teacher_subjects,get_attendance_for_teacher
from src.components.create_subject_dialog import create_subject_dialog
from src.components.share_subject_dialog import share_subject_dialog
from src.components.subject_card import subject_card
from src.components.add_photo_dialog import add_photo_dialog
import numpy as np
from src.pipelines.face_pipeline import predict_attendance

from src.components.attendance_result_dialog import attendance_result_dialog

from src.database.config import supabase
from datetime import datetime
import pandas as pd



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
        return
        
    subjects_options={f"{s['name']}-{s['subject_code']}":s['subject_id'] for s in subjects}
        
        
    col1,col2=st.columns([3,1],vertical_alignment='bottom')
    with col1:
        selected_subject_labels=st.selectbox('Select Subject',options=list(subjects_options.keys()))
        
    with col2:
        if st.button('Add Photo',type='primary',width='stretch' ,icon=':material/photo_auto_merge:'):
            add_photo_dialog()
    
    selected_subject_id=subjects_options[selected_subject_labels]
    
    st.divider()
    
    if st.session_state.attendance_image:
        st.header('Added Photos')

        photo_cols=st.columns(4)

        for idx,img in enumerate(st.session_state.attendance_image):
            with photo_cols[idx%4]:
                st.image(img,width='stretch',caption=f"photo {idx+1}")

        has_photo=bool(st.session_state.attendance_image)       
        c1,c2,c3=st.columns(3)
        with c1:
            if st.button('Clear all photos',width='stretch',type='tertiary',icon=':material/delete_history:',disabled=not has_photo):
                st.session_state.attendance_image=[]
                st.rerun()

        with c2:
            if st.button('Run Face Analysis',width='stretch',type='secondary',icon=':material/conditions:',disabled=not has_photo):
                
                with st.spinner('🔍 AI is deep scanning your photo... Please wait...'):
            
                    all_detected_ids={}
                    
                    for idx,img in enumerate(st.session_state.attendance_image):
                        img_np=np.array(img.convert('RGB'))
                        
                        detected,_,_,=predict_attendance(img_np)
                        if detected:
                            for sid in detected.keys():
                                student_id=int(sid)
                                
                                all_detected_ids.setdefault(student_id,[]).append(f"photo {idx+1}")
                                
                    
                    enrolled_res=supabase.table('subject_students').select("*,students(*)").eq('subject_id',selected_subject_id).execute()   
                    enrolled_students=enrolled_res.data
                    
                    if not enrolled_students:
                        st.warning("No students enrolled in this course")
                    else:
                        results,attendance_to_log=[],[] #show on screen & store in DB
                        
                        current_timestamp= datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                        
                        for node in enrolled_students:
                            student=node['students']
                            src=all_detected_ids.get(int(student['student_id']),[])
                            is_present=len(src)>0
                            
                            results.append({
                                "Name":student['name'],
                                "ID":student['student_id'],
                                "Source":", ".join(src) if is_present else "-",
                                "Status":"✅Present" if is_present else "❌ Absent" 
                            })
                            
                            attendance_to_log.append({
                                'subject_id': selected_subject_id,
                                'student_id': student['student_id'],
                                'timestamp': current_timestamp,
                                'is_present': bool(is_present)
                            })
                            
                        attendance_result_dialog(pd.DataFrame(results),attendance_to_log)
                        
                    
                             
            
        with c3:
            st.button('Voice (Coming soon)',width='stretch',type='primary',icon=':material/adaptive_audio_mic:',disabled=True)
            # Use Voice Attendance
                
            
    
    
    
    
    
    
    
    
    
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
        
            def share_btn():
                if st.button(f"Share Code: {sub['subject_code']}", key=f"share_{sub['subject_code']}", icon=":material/share:", width='stretch'):
                    share_subject_dialog(sub['name'],sub['subject_code'])
        
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
    teacher_id=st.session_state.teacher_data['teacher_id']
    
    records=get_attendance_for_teacher(teacher_id)
    
    if not records:
        st.info("No attendance records found.")
        return
    data = []

    for r in records:
        dt = datetime.fromisoformat(r["timestamp"])

        data.append({
            "Time": dt.strftime("%d-%m-%Y %I:%M %p"),
            "Student": r["students"]["name"],
            "Subject": r["subjects"]["name"],
            "Code": r["subjects"]["subject_code"],
            "Status": "Present ✅" if r["is_present"] else "Absent ❌"
        })

    df = pd.DataFrame(data)

    # ---------- Filters ----------
    col1, col2 = st.columns(2)

    with col1:
        subject = st.selectbox(
            "Filter by Subject",
            ["All"] + sorted(df["Subject"].unique().tolist())
        )

    with col2:
        status = st.selectbox(
            "Filter by Status",
            ["All", "Present ✅", "Absent ❌"]
        )

    if subject != "All":
        df = df[df["Subject"] == subject]

    if status != "All":
        df = df[df["Status"] == status]

    st.divider()

    st.dataframe(df, width='stretch',hide_index=True)

    st.download_button("📥 Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="attendance_records.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    
        
    
    

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
    
    teacher_username=st.text_input("Enter username",placeholder='@imran15')
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
    
    teacher_username=st.text_input("Enter username",placeholder='@rishi042')
    teacher_username = teacher_username.strip().lower()
    teacher_name=st.text_input("Enter full name",placeholder='Eg: Rishikesh Gupta')
    teacher_name=teacher_name.strip().title()
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
        
        
        
        
    