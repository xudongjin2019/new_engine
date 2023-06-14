import hashlib
import time
import datetime
import json
import sqlite3
from pathlib import Path
import datetime
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages,hide_pages
from streamlit_extras.stateful_button import button
from streamlit_extras.switch_page_button import switch_page
from streamlit_login_auth_ui.widgets import __login__
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import _on_pages_changed, get_pages
import altair as alt

st.set_page_config(page_title = "LME Certification System", page_icon = "👋", layout = "wide")

conn = sqlite3.connect("ECS0612.db")
c = conn.cursor()

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



def user(username):
    st.write('Hi',username,'Please select the sub item to continue or review your histroy')
 
    col1,col2,col3,col4 =st.columns(4)
    with col1:
        b1= st.button('Step:one:,Take Exam')
        if b1:
            switch_page('Take Exam')
    with col2:
        b2= st.button('Setp:two: , Get Certification')
        if b2:
            switch_page('Get Certification')

    st.divider()


    score_result = view_all_score()
    score_db = pd.DataFrame( score_result, columns=["grade", "course_name", "version","user_name","user_score","user_dept","score_time"])
    st.dataframe(score_db, use_container_width=True)



def welcome():
   st.write("# Welcome to LME Engineering Certification System 👋")
   st.markdown(
        """
        GTE Certification System is a web app built with Streamlit specifically for Course Exam and Certification. 
        GTE Solution team reserve all the rights.
        - **👈 Select the page from the sidebar to go directly to take exam or get certification!**
        - **👈 Please login and confirm the name/email/department to save your exam data .**
        - **👈 Suggest to take exam after trainning session hold by GTE team.**
        - **👈 You can get certification paper in case you pass the exam with score >80 !**
        - **👈 If you have any question or trouble,please contact with GTE solution team.**

    """
    )
    

def main():
    welcome()
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
            user(username)                           


if __name__ == "__main__":
    main()