import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import hashlib
import json
import sqlite3
from pathlib import Path
import time
import datetime

from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit_login_auth_ui.widgets import __login__

import streamlit_authenticator as stauth
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages,hide_pages
from streamlit_extras.stateful_button import button
from streamlit_extras.switch_page_button import switch_page
from streamlit_login_auth_ui.widgets import __login__
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import _on_pages_changed, get_pages

conn = sqlite3.connect("ECS0612.db")
c = conn.cursor()

def create_user():
    c.execute("CREATE TABLE IF NOT EXISTS user_table(name TEXT, email TEXT UNIQUE, password TEXT, dept TEXT )")

def add_user(name, email, password,dept):
    c.execute("INSERT OR REPLACE INTO user_table(name, email, password,dept) VALUES (?,?,?,?)",(name,email,password,dept),)
    conn.commit()

def create_exam():
    c.execute("CREATE TABLE IF NOT EXISTS exam_table(name TEXT UNIQUE, level TEXT , course TEXT, version TEXT,score )")

def add_exam(name, email, password,dept):
    c.execute("INSERT OR REPLACE INTO exam_table(name, email, password,dept) VALUES (?,?,?,?)",(name,email,password,dept),)
    conn.commit()

def fetch_all_user():
    c.execute("SELECT * FROM user_table")
    data = c.fetchall()
    return data

def login_user(email, password):
    c.execute(
        "SELECT * FROM users_table WHERE email =? AND password = ?", (email, password)
    )
    data = c.fetchall()
    return data

def create_course():
    c.execute(
        "CREATE TABLE IF NOT EXISTS course_table(grade TEXT, course_name TEXT, version TEXT,NO TEXT UNIQUE,question TEXT, c1 TEXT,c2 TEXT,c3 TEXT,c4 TEXT, answer TEXT)"
    )


# Insert or replace the data into table
def add_course(grade, course_name, version,NO,question, c1,c2,c3 ,c4 , answer):
    c.execute(
        "INSERT OR REPLACE INTO course_table(grade, course_name, version,NO,question, c1,c2,c3 ,c4 , answer) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (grade, course_name, version,NO,question, c1,c2,c3 ,c4 , answer),
    )
    conn.commit()


# t_item  fetch  试题查询
def search_exam(grade,course_name, version):
    c.execute(
        "SELECT * FROM course_table WHERE grade =? AND course_name =? AND version =?", (grade,course_name,version)
    )
    exam_data = c.fetchall()
    return exam_data



def view_all_course():
    c.execute("SELECT * FROM course_table")
    data = c.fetchall()
    return data

def view_exam_course():
    c.execute("SELECT grade,course_name,version FROM course_table")
    data = c.fetchall()
    return data

def view_grade_course(grade):
    c.execute("SELECT course_name,version FROM course_table WHERE grade = ?",grade)
    data = c.fetchall()
    return data

def view_course(grade):
    c.execute("SELECT course_name FROM course_table WHERE grade = ?",grade)
    data = c.fetchall()
    return data

def get_questionlist():
        course_result = view_exam_course()
        course_db = pd.DataFrame( course_result, columns=["question"])
        # st.dataframe(course_db, use_container_width=True)

        question_list= sorted(set(course_db.iloc[:,0].to_list()),reverse=False)
        
        return question_list


def get_examlist():
        course_result = view_exam_course()
        course_db = pd.DataFrame( course_result, columns=["grade", "course_name", "version"])
        # st.dataframe(course_db, use_container_width=True)

        grade_list= sorted(set(course_db.iloc[:,0].to_list()),reverse=False)
        course_name_list= sorted(set(course_db.iloc[:,1].to_list()),reverse=True)
        course_version_list= sorted(set(course_db.iloc[:,2].to_list()),reverse=True)
        
        return grade_list,course_name_list,course_version_list

def create_score_table():
    c.execute(
        "CREATE TABLE IF NOT EXISTS score_table(grade TEXT, course_name TEXT, version TEXT,user_name TEXT, user_score TEXT,user_dept TEXT, score_time TEXT)"
    )


# Insert or replace the data into table
def add_score(grade, course_name, version,user_name,user_score,user_dept,score_time):
    c.execute(
        "INSERT OR REPLACE INTO score_table(grade, course_name, version,user_name,user_score,user_dept,score_time) VALUES (?,?,?,?,?,?,?)",
        (grade, course_name, version,user_name,user_score,user_dept,score_time),
    )
    conn.commit()

def view_all_score():
    c.execute("SELECT * FROM score_table")
    data = c.fetchall()
    return data

class user():
    user_count = 0
    create_user()
    def __init__(self, name, email, password, dept):
        self.user_count +1
        self.name = name
        self.email = email
        self.password = hashlib.sha256(str.encode(password)).hexdigest()
        self.dept = dept

    def save_db(self):
        create_user()
        add_user(self.name,self.email,self.password,self.dept)

    def show_db():
        c.execute("SELECT * FROM user_table")
        data = c.fetchall()
        st.dataframe(pd.DataFrame(data))
    
    def login():
        st.write('test')

class course():
    create_course()


class exam():
    create_exam()
    def __init__(self, name, level, course,version):
        self.name = name
        self.level = level
        self.course = course
        self.version = version
    
    def start(self):
        self.start = datetime.datetime.now()
        self.start_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def end(self):
        self.end = datetime.datetime.now()
        self.end_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def used_time(self):
        self.used_time =  self.end - self.start
        st.write('Start time', self.start_str,'End time' , self.end_str, 'Total used', self.used_time)

    def score():
        st.divider()


def login_form(username,email):
    st.write('Step:one:,Please login to save your information')
    login_holder= st.empty()
    with login_holder.container():
        with st.form("login information check"):
            col1,col2 = st.columns(2)
            with col1:
                name = username
            with col2:
                email = email
            dept = st.radio('Select dept?',('GE-GTE', 'LSSC-NB-ENG', 'LSSC-DT-ENG','LSSC-SVR-ENG','TJSC-NB-ENG'),key='user dept',horizontal=True)
            
            submitted_user1 = st.form_submit_button("Submit user information")
            if submitted_user1:
                if name == '':
                    st.error('User name is blank')
                elif email == '':
                    st.error('User email is blank')
                elif dept == '':
                    st.error('dept is blank')
                else:
                    st.session_state["logged_in"] = True
                    st.success(' user inform confirm success')          
    
    if st.session_state.logged_in == True:
        login_holder.empty()
        st.write('Hello, ',name, 'from', dept,'with e-mail',email,' ',':sunglasses:')
        st.session_state.user = name
        st.session_state.dept = dept
    return name
  

def course_select():
    st.write('Step:two:,Please select the course') 
    course_holder= st.empty()
    with course_holder.container():
        with st.form("course select"):

            dept = st.radio('Quick Select?',('B4-DT测试流程入门', 'B5-NB问题分析初级', 'B6-测试程序开发初级'),key='quick select',horizontal=True)
            if dept == 'B4-DT测试流程入门' :
                exam_grade = 'B4'
                exam_name = 'DT测试流程入门'
                exam_version = '2023061211'
            
            elif dept == 'B5-NB问题分析初级' :
                exam_grade = 'B5'
                exam_name = 'NB问题分析初级'
                exam_version = '2023061211'

            elif dept == 'B6-测试程序开发初级' :
                exam_grade = 'B6'
                exam_name = '测试程序开发初级'
                exam_version = '2023061211'

           
            check = st.checkbox('Manual select')
            if check:
                col1,col2,col3 = st.columns(3)
                course_grade,course_name,course_version = get_examlist()
                with col1:
                    exam_grade = st.selectbox('Select grade?',course_grade)
                with col2:
                    
                    exam_name = st.selectbox('Select course name?',course_name)
                with col3:
                    exam_version = st.selectbox('Select course version?',course_version)
                    
            submitted_user2 = st.form_submit_button("Submit course information")
                
            if submitted_user2:
                    if exam_grade == '':
                        st.error('exam grade is blank')
                    elif exam_name == '':
                        st.error('exam name is blank')
                    elif exam_version == '':
                        st.error('exam version is blank')
                    else:
                        st.session_state["course_select"] = True
                        st.success('Course select success')

    if st.session_state.course_select == True:
        
        st.write('You choose','Grade  ',exam_grade, 'Name ',exam_name, 'verison',exam_version,'for exam! :ledger:')
        exam_list = search_exam(exam_grade,exam_name,exam_version)
        exam_pd = pd.DataFrame( exam_list, columns=["grade", "course_name", "version",'NO','question','c1','c2','c3','C4','Answer'])
        question_list = exam_pd['question']
        st.write(question_list)
        confirm = st.checkbox('Confirm')
        if confirm:
            st.session_state.exam_grade = exam_grade
            st.session_state.exam_name = exam_name
            st.session_state.exam_version = exam_version
            st.session_state.course_confirm = True
            course_holder.empty()
        else: 
            st.warning('check to confirm the selection or un-check to select agaion')

    return exam_grade,exam_name,exam_version
    
def exam_form(name,grade,course_name,version):
    st.write('Step:three:,Start the exam') 
    exam_holder= st.empty()
    with exam_holder.container():
        with st.form("take exam"):
            st.markdown("**:blue[Start Test ]**")

            exam_list = search_exam(grade,course_name,version)
            exam_pd = pd.DataFrame( exam_list, columns=["grade", "course_name", "version",'NO','question','c1','c2','c3','C4','Answer'])
            exam_answer_list =exam_pd['Answer']
            user_answer_list =[]
            question_list = exam_pd['question']
            for row_index,row in exam_pd.iterrows(): 
                exam_question = st.write('NO',str(row_index+1),',',row[4],':question:') 
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write('A,',row[5])
                    st.write('B,',row[6])
                    st.write('C,',row[7])
                    st.write('D,',row[8])
                with col2:
                    exam_answer = st.radio('Please choose',('A','B','C','D'),label_visibility='visible',key=row_index,horizontal= True)
                    rate = str(format((row_index+1)/len(exam_pd),'.0%'))
                    st.write('Total',str(len(exam_pd)),',     :blue[Finish rate] =',rate )
                user_answer_list.append(exam_answer)
                st.divider()
        
        
            submitted_exam = st.form_submit_button("Submit the answer")
            if submitted_exam :
                st.success("submit success ✔ ") 
                st.session_state.exam_finish = True
                total, correct = 0, 0
                for i in range(len(user_answer_list)):
                    if exam_answer_list[i] == user_answer_list[i]:
                            st.write('NO',str(i),'......',question_list[i], ':o:','......Answer is',user_answer_list[i])
                            correct += 1
                    else:
                        st.write('NO',str(i),'......',question_list[i],':x:', '......Coccrect answer is',exam_answer_list[i], '......You choose',user_answer_list[i])
                    total += 1
                score = 0
                score = int(correct / total * 100)
                st.write('Your Score is ',str(score))
                score_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
                st.write('exam finish',name,grade,course_name,version,str(score),score_time)
                st.session_state.exam_score = str(score)
                st.session_state.score_time = score_time
                create_score_table()
                add_score(grade, course_name, version,name,str(score),st.session_state.dept,score_time)
                if score >= 80 :
                    st.write('You can get certification since your score >= 80')
                    time.sleep(3)
                    switch_page('Get Certification')


def result():
        st.divider()
        st.write('Step:four:,overall exam status summary')
        with st.form("exam result"):
            st.write('exam finish',st.session_state.user, st.session_state.exam_grade, st.session_state.exam_name, st.session_state.exam_version,st.session_state.exam_score,st.session_state.dept,st.session_state.score_time)
            score_result = view_all_score()
            score_db = pd.DataFrame( score_result, columns=["grade", "course_name", "version","user_name","user_score","user_dept","score_time"])
            st.dataframe(score_db, use_container_width=True)

            confirm = st.form_submit_button("confirm")
            if confirm:
                st.session_state.exam_confirm = True




def session():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'course_select' not in st.session_state:
        st.session_state.course_select = False
    if 'course_confirm' not in st.session_state:
        st.session_state.course_confirm = False
    if 'exam_finish' not in st.session_state:
        st.session_state.exam_finish = False
    if 'user' not in st.session_state:
        st.session_state.user = False
    if 'dept' not in st.session_state:
        st.session_state.dept = False
    if 'exam_grade' not in st.session_state:
        st.session_state.exam_grade = False
    if 'exam_name' not in st.session_state:
        st.session_state.exam_name = False
    if 'exam_version' not in st.session_state:
        st.session_state.exam_version = False
    if 'exam_confirm' not in st.session_state:
        st.session_state.exam_confirm = False
    if 'exam_score' not in st.session_state:
        st.session_state.exam_score = 0
    if 'score_time' not in st.session_state:
        st.session_state.score_time = 0

st.set_page_config(page_title = "LME Certification System", page_icon = "👋", layout = "wide")


def get_username(self):
        if st.session_state['LOGOUT_BUTTON_HIT'] == False:
            fetched_cookies = self.cookies
            if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                username=fetched_cookies['__streamlit_login_signup_ui_username__']
                return username
            
def get_email(username):
    """
    Checks if the email entered is present in the _secret_auth.json file.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user['username'] == username:
                    return user['email']
            
def admin():
    st.divider()
    col1,col2,col3 =st.columns(3)
    with col1:
        b1= st.button('Course Admin')
        if b1:
            switch_page('Course Admin')
    with col2:
        b2= st.button('User Admin')
        if b2:
            switch_page('User Admin')
    with col3:
        b3= st.button('Data summary')
        if b3:
            switch_page('Data summary')



def user():
    st.divider()
    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in = False
    else:
        st.session_state.logged_in = False
                           

def main():
    st.write("# LME Engineering Certification System! 👋")
    session()

    __login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = True, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()
    username= get_username(__login__obj)


    if LOGGED_IN == True:
        
        #st.markdown(st.session_state)
        show_pages(
        [
            Page("pages/1_User Home.py", "User Home", "🏠"),
            Page("pages/2_Take Exam.py", "Take Exam", "✏️"),
            Page("pages/3_Certification.py", "Get Certification", "💪"),
            Page("pages/4_Course Admin.py", "Course Admin", "📖"),
            Page("pages/5_User Admin.py", "User Admin", "👨🏻‍💼"),
            Page("pages/6_Data Summary.py", "Data Summary", "🎈️"),
        ])

        if username == 'jeremyxu' or  username =='gteadmin':

            hide_pages(['Take Exam','Get Certification'])
            st.sidebar.write('hellow ',username,'with email',get_email(username))
            admin()

        else:
            hide_pages(['Course Admin','Data Summary','User Admin'])
            st.sidebar.write('hellow ',username,'with email',get_email(username))
            st.divider()
            login_form(username,get_email(username))
            st.divider()
            course_select()
            st.divider()
            if st.session_state.course_confirm == True and st.session_state.logged_in == True:
                exam_form( st.session_state.user, st.session_state.exam_grade, st.session_state.exam_name, st.session_state.exam_version)
            if st.session_state.exam_finish == True:
                result()
                st.session_state.course_select = False
                st.session_state.exam_finish = False
                st.session_state.logged_in = False
                st.session_state.course_confirm = False


    else:
        st.error('Please login to proceed')     



if __name__ == "__main__":
    main()