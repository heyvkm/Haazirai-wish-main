from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(),hashed.encode())

def check_teacher_exists(username):
    #check for unique username and return false if already exits
    response=supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data)>0


def create_teacher(username,password,name):
    data={"username":username,"password":hash_pass(password),"name":name}
    response=supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username,password):
    response=supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
        teacher=response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
    return None


def get_all_students():
    response=supabase.table('students').select("*").execute()
    return response.data

def create_student(new_name,face_embedding=None,voice_embedding=None):
    data={'name':new_name,'face_embedding':face_embedding,'voice_embedding':voice_embedding}
    response=supabase.table('students').insert(data).execute()
    return response.data
    
    
def create_subjects(sub_code,sub_name,sub_section,teacher_id):
    data={'subject_code':sub_code,'name':sub_name,'section':sub_section,'teacher_id':teacher_id}
    response=supabase.table('subjects').insert(data).execute()
    return response


def get_teacher_subjects(teacher_id):
    # 1. Execute query fetching all columns, nested student count, and attendance timestamps
    response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data

    for sub in subjects:
        # 2. FIXED: Matches the plural 'subject_students' key from the query string
        # Supabase aggregate counts return a dictionary inside a single-element list: [{'count': X}]
        student_data = sub.get('subject_students', [])
        sub['total_students'] = student_data[0].get('count', 0) if student_data else 0
        
        # 3. Safely pull and look through the logs to get unique class session dates
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance if 'timestamp' in log))
        sub['total_classes'] = unique_sessions

        # 4. Clean up the response dictionary before sending it to the frontend
        sub.pop('subject_students', None)  # FIXED: Popping the correct plural key name
        sub.pop('attendance_logs', None)

    return subjects

def enroll_student_to_subject(student_id,subject_id):
    data={'student_id':student_id,'subject_id':subject_id}
    response=supabase.table('subject_students').insert(data).execute()
    return response.data


def unenroll_student_to_subject(student_id,subject_id):
    response=supabase.table('subject_students').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return response.data

def get_student_subject(student_id):
    response=supabase.table('subject_students').select('*,subjects(*)').eq('student_id',student_id).execute()
    return response.data

def get_student_attendance(student_id):
    response=supabase.table('attendance_logs').select('*,subjects(*)').eq('student_id',student_id).execute()
    return response.data
