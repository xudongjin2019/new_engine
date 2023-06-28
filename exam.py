import streamlit as st
import pandas as pd
import datetime
import time
import sqlite3
from widgets import __login__
import streamlit_antd_components as sc

def get_course():
    con = st.experimental_connection('user_db', type='sql')
    with con.session as s:
        s.execute("CREATE TABLE IF NOT EXISTS course_table(grade TEXT, course_name TEXT, version TEXT,NO TEXT UNIQUE,question TEXT, c1 TEXT,c2 TEXT,c3 TEXT,c4 TEXT, answer TEXT)")
        s.commit()
        # Query and display the data you inserted             
    course_db = con.query('SELECT * FROM course_table ')
    return course_db

def add_score(grade,course,version,username,score,depart,score_time):
    con = st.experimental_connection('user_db', type='sql')

    with con.session as s:
        data = dict()
        data['grade']= grade
        data['course']=course
        data['version']=version
        data['user']=username
        data['score']=score
        data['dept']=depart
        data['time']=score_time
        s.execute(
            "INSERT OR REPLACE INTO score_table(grade,course_name,version,user_name,user_score,user_dept,score_time) VALUES (:grade,:course,:version,:user,:score,:dept,:time);",
            params= data)
        s.commit()



def session():
    if 'course_select' not in st.session_state:
        st.session_state.course_select = False
    if 'exam_start' not in st.session_state:
        st.session_state.exam_start = False
    if 'certi_gen' not in st.session_state:
        st.session_state.certi_gen = False
    if 'exam_finish' not in st.session_state:
        st.session_state.exam_finish = False
    if 'grade' not in st.session_state:
        st.session_state.grade = ''
    if 'course' not in st.session_state:
        st.session_state.course = ''


def course_select(username): 
        st.session_state.course_select = False
        cc = st.empty()
        with cc.container():
            course_db = get_course()
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
            if grade and course:
                st.write('Hello',username,'You select Grade:',grade,'Course:',course)
                st.write('Please confirm above information to start exam')
            
        
            if st.button('confirm', key = course):
                st.session_state.course_select = True
                st.session_state.grade = grade
                st.session_state.course = course
                cc.empty()
                return grade,course
            else:
                st.session_state.course_select = False
                return grade,course




def exam_score(grade,course,username,depart):
    if st.session_state.course_select == True:
        st.session_state.exam_finish = False
        with st.form('Score'):
            course_db = get_course()
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



            submitted_exam = st.form_submit_button("Submit the answer")
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
                st.session_state.exam_score = str(score)
                st.session_state.score_time = score_time
                st.session_state.exam_finish = True
                add_score(grade,course,version,username,score,depart,score_time)
                st.success('Score data saved to DB')

                
               # return grade,course,version,username,score,depart,score_time
            

def load_score():

    con = st.experimental_connection('user_db', type='sql')
    score_db2 = con.query('SELECT * FROM score_table ',ttl=10)
    st.dataframe(score_db2)

def welcome():
   st.write("# Welcome to LME Certification System 👋")
   st.markdown(
        """
        LME Certification System is a web app for Course Exam and Certification. 
        - **👈 Select the page from the sidebar to go directly to take exam or get certification!**
        - **👈 Suggest to take exam after trainning session hold by LME team**
        - **👈 You can get certification paper in case you pass the exam with Score>80!**
        - **👈 If you have any question or trouble,please contact with GTE solution team.**

    """
    )

def take_exam(user_name,user_dept):
    welcome()
    sc.divider('Step1: Select the Couse',icon='house',align='left')
    if st.session_state.course_select == False:
            grade,course= course_select(user_name)
            
        
    if st.session_state.course_select == True:
        grade = st.session_state.grade
        course = st.session_state.course
        st.write('Hello',user_name,'You select Grade:',grade,'Course:',course)
        exam_start = 'Step2: Exam Start '+'@'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+'  Course: '+grade+'-'+ course
        sc.divider(exam_start,icon='arrow-down-square',align='left')
        exam_score(grade,course,user_name,user_dept)
        if  st.session_state.exam_finish == True:
            #   save_score(grade,course,version,username,score,depart,score_time)
            sc.divider('Step3: Display score info in DB ',icon='check cycle',align='left')
            load_score()