import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from io import StringIO
import numpy as np
import datetime
import time
import hashlib
import json
import sqlite3
from pathlib import Path
import pandas.io.sql as pd_sql


from widgets import __login__
from pathlib import Path

import altair as alt


st.set_page_config(page_title = "LME Certification System", page_icon = "👋", layout = "wide")

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "LME certification system";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 26px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.markdown("""
  <style>
    .css-o18uir.e16nr0p33 {
      margin-top: -75px;
    }
  </style>
""", unsafe_allow_html=True)

reduce_header_height_style = """
    <style>
        div.block-container {padding-top:1rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

st.sidebar.header('LME Engineering Certification System')



con = st.experimental_connection('user_db', type='sql')
with con.session as s:
    s.execute("CREATE TABLE IF NOT EXISTS course_table(grade TEXT, course_name TEXT, version TEXT,NO TEXT UNIQUE,question TEXT, c1 TEXT,c2 TEXT,c3 TEXT,c4 TEXT, answer TEXT)")
    s.commit()
    # Query and display the data you inserted             
course_db = con.query('SELECT * FROM course_table ')

conn = sqlite3.connect("ECS_0619.db")
c = conn.cursor()

def add_score(grade, course_name, version,user_name,user_score,user_dept,score_time):
    c.execute(
        "INSERT OR REPLACE INTO score_table(grade, course_name, version,user_name,user_score,user_dept,score_time) VALUES (?,?,?,?,?,?,?)",
        (grade, course_name, version,user_name,user_score,user_dept,score_time),
    )
    conn.commit()


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



def get_dept(username):
    """
    Checks if the email entered is present in the _secret_auth.json file.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user['username'] == username:
                    return user['depart']


def user_sidebar():
    st.sidebar.markdown('***Please follow next steps for exam and certification***')
    if 'course_select' not in st.session_state:
        st.session_state.course_select = False
    if 'exam_start' not in st.session_state:
        st.session_state.exam_start = False
    if 'certi_gen' not in st.session_state:
        st.session_state.certi_gen = False
    if 'exam_finish' not in st.session_state:
        st.session_state.exam_finish = False
    if 'grade' not in st.session_state:
        st.session_state.grade = False
    if 'course' not in st.session_state:
        st.session_state.course = False

    if st.sidebar.button('Step 1,  Select Course 👉',key = 'course_click'):
        st.session_state['course_select'] = True
    if st.sidebar.button('Step 2,  Take your Exam 👉',key = 'exam_Click'):
        st.session_state['exam_start'] = True
    if st.sidebar.button('Setp 3,  Certification 👉',key = 'certi_Click'):
        st.session_state['certi_gen'] = True

    st.sidebar.write('ADDCB-DCDBC')


def admin():
     st.sidebar.button('Step:two:')



def course_select(username): 
    if st.session_state.course_select == True:
        st.session_state.exam_start = False
       
        course_emp = st.empty()
        # Insert some data with conn.session.
        with course_emp.container():
            st.write('Step:one:,Please select the course') 
            st.divider()

            grade_list= sorted(set(course_db.iloc[:,0].to_list()),reverse=False)

            # 转换为字典,去重
            course_zip = pd.DataFrame(zip(course_db.iloc[:,0],course_db.iloc[:,1]), columns=['grade', 'course'])
            course_set = course_zip.drop_duplicates(course_zip)
            #course_list = st.dataframe(course_set)

            grade_list= sorted(set(course_db.iloc[:,0].to_list()),reverse=False)
            grade = st.radio('Level',grade_list,horizontal=True)
            if grade:
                select = course_set.loc[ course_set['grade'] ==grade,:]
                course_list= sorted(set(select.iloc[:,1].to_list()),reverse=True)
                course = st.radio('Select Course',course_list,horizontal=True)

            
            if grade and course:    # confirm user informaiton
                st.write('Hello',username,'You select Grade:',grade,'Course:',course)
                st.write('Please confirm above information to start exam')



                confirm = st.button('Confirm and Start test')
                if confirm:
                    course_emp.empty()
                    st.session_state.course_select = False
                    st.session_state.exam_start = True
                    st.session_state.grade = grade
                    st.session_state.course = course


    


def exam_score(grade,course,username):

    if st.session_state.exam_start == True:

        exam_holder= st.empty()
        with exam_holder.container():
            st.write('Step:two:,Start the exam') 
            st.divider()
            df = pd.DataFrame(course_db, columns=["grade", "course_name", "version",'NO','question','c1','c2','c3','c4','answer'])
            version_list= sorted(set(course_db.iloc[:,2].to_list()),reverse=True)
            version = version_list[0]
            exam_pd_old = df.loc[(df['grade']==grade) &(df['course_name']==course) & (df['version']==version) ,: ]
            exam_pd = exam_pd_old.reset_index(drop=True)

            exam_answer_list =exam_pd['answer']
            user_answer_list =[]
            question_list = exam_pd['question']
            row_NO = 0
            for row_index,row in exam_pd.iterrows(): 
                row_NO = row_NO+1
                exam_question = st.write('NO',str(row_NO),',',row[4],':question:') 
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write('A,',row[5])
                    st.write('B,',row[6])
                    st.write('C,',row[7])
                    st.write('D,',row[8])
                with col2:
                    exam_answer = st.radio('Please choose',('A','B','C','D'),label_visibility='visible',key=row_index,horizontal= True)
                    rate = str(format((row_NO)/len(exam_pd),'.0%'))
                    st.write('Total',str(len(exam_pd)),',     :blue[Finish rate] =',rate )
                user_answer_list.append(exam_answer)
                st.divider()

        
        
            submitted_exam = st.button("Submit the answer")
            if submitted_exam :
                st.success("submit success ✔ ") 
                st.session_state.exam_finish = True
                total, correct = 0, 0
                for i in range(len(user_answer_list)):
                    if exam_answer_list[i] == user_answer_list[i]:
                            st.write('NO',str(i+1),'......',question_list[i], ':o:','......Answer is',user_answer_list[i])
                            correct += 1
                    else:
                        st.write('NO',str(i+1),'......',question_list[i],':x:', '......Correct answer is',exam_answer_list[i], '......You choose',user_answer_list[i])
                    total += 1
                score = 0
                score = int(correct / total * 100)
                st.write('Your Score is ',str(score))
                score_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
                st.write('exam finish',username,grade,course,version,str(score),score_time)
                st.write('You can get certification if your score >= 80')
                st.divider()

            left, right = st.columns([1,3])
            with left:
                check = st.button('Confirm the score ')
                if check:
                    st.session_state.exam_score = str(score)
                    st.session_state.score_time = score_time

                    dept = get_dept(username)

                    add_score(grade,course,version,username,str(score),dept,score_time)
                    st.success('Score data saved to DB')
                    score_db = con.query('SELECT * FROM score_table ')
                    st.write(score_db)
                    time.sleep(3)
                    exam_holder.empty()

            with right: 
                if score >= 80 :
                    cert_but= st.button('Get Certification if score >=80')
                    if cert_but:
                        exam_holder.empty()
                        st.session_state.exam_start = False
                        st.session_state.exam_finish = True
                        st.session_state.certi_gen = True
                        get_cert()


def get_cert():
    if st.session_state.exam_finish == True and st.session_state.certi_gen == True:
        st.write('certi')


def main(): 
    add_logo()
    __login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = True, 
                    hide_footer_bool = True, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()
    username= get_username(__login__obj)
    mail= get_email(username)
    dept = get_dept(username)
    st.write(mail,dept)
    st.sidebar.divider()

    if LOGGED_IN == True:
        if username == 'jeremyxu' or  username =='gteadmin':
            admin()
        else:
            user_sidebar()
            course_select(username)
            if st.session_state.exam_start == True:
                exam_score(st.session_state.grade,st.session_state.course,username)
            if st.session_state.certi_gen == True:
                get_cert()


         


if __name__ == "__main__":
    main()