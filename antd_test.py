import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from io import StringIO
import numpy as np
import datetime
import hashlib
import json
from pathlib import Path
from widgets import __login__

import streamlit_antd_components as sc

st.set_page_config(page_title = "LME Certification System", page_icon = "👋", layout = "wide")

from exam import course_select,exam_score,load_score,take_exam
from Certification import gen_cert
from user_report import user_report
from user_admin import user_admin
from evaluation import value

reduce_header_height_style = """
    <style>
        div.block-container {padding-top:0rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)




__login__obj = __login__(auth_token = "courier_auth_token", 
            company_name = "Shims",
            width = 200, height = 250, 
            logout_button_name = 'Logout', hide_menu_bool = True, 
            hide_footer_bool = True, 
            lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

def get_username(self):
    fetched_cookies = self.cookies
    if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
        username=fetched_cookies['__streamlit_login_signup_ui_username__']
        return username

def set_sidebar(username):
    with st.sidebar.container():
        qq= 'Welcome , '+username+'   😎'
        st.header("LME Engineering Evaluation System ")
        st.write(qq)
        if username in admin_list:
            menu_item = sc.menu([
                sc.MenuItem(type='divider'),
                sc.MenuItem('Dashboard', icon='check2-square'),
                sc.MenuItem('Evaluation', icon='award'), 
                sc.MenuItem('Course Admin', icon='award'), 
                sc.MenuItem('User Admin', icon='bar-chart'),
                sc.MenuItem(type='divider'),
                sc.MenuItem('reference', type='group', children=[
                    sc.MenuItem('Take Exam', icon='check2-square'),
                    sc.MenuItem('Get Certification', icon='award'), 
                    sc.MenuItem('User Summary', icon='clipboard2-data'),
                    sc.MenuItem('User Setting', icon='gear'),],),
                sc.MenuItem(type='divider'),],
                format_func='title', open_all=True,index=1)
        else: 
            menu_item = sc.menu([
                sc.MenuItem(type='divider'),
                sc.MenuItem('Take Exam', icon='check2-square'),
                sc.MenuItem('Get Certification', icon='award'), 
                sc.MenuItem('Summary Report', icon='clipboard2-data'),
                sc.MenuItem('User Setting', icon='gear'),
                
                sc.MenuItem(type='divider'),],
                format_func='title', open_all=True,index=0)
            
        st.write(f'The selected menu label is: {menu_item}')


    return menu_item

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
        st.session_state.grade = False
    if 'course' not in st.session_state:
        st.session_state.course = False

def get_user(self):
   
    fetched_cookies = self.cookies
    if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
        user_name=fetched_cookies['__streamlit_login_signup_ui_username__']
    else:
        user_name='Jeremy Xu'

    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)
        for user in authorized_users_data:
            if user['username'] == user_name:
                user_mail =  user['email']
                user_dept =  user['depart']
  
    return user_name,user_mail,user_dept



# 定义管理员列表
admin_list = ['Jeremy Xu', 'jeremyxu', 'gteadmin', 'xudj1']


def main():
    user_name,user_mail,user_dept = get_user(__login__obj)
    select = set_sidebar(user_name)
    LOGGED_IN = __login__obj.build_login_ui()

    session()
    if select == 'Take Exam':
        
        list = [dict(label='Select Course', icon='check-square'),dict(label='Take Exam', icon='explicit'),
            dict(label='Get Certification', icon='award'),dict(label='Check History', icon='bar-chart'),]
        take_exam(user_name,user_dept)
        

    if select == 'Get Certification':  
        gen_cert(user_name)

    if select == 'Evaluation':  
        value()

    if select == 'Check History':
        load_score()

        ww = st.text_input('input')

        list = [dict(label='Select Course', icon='check-square'),dict(label='Take Exam', icon='explicit'),
            dict(label='Get Certification', icon='award'),dict(label='Check History', icon='bar-chart'),]
        if ww =='1':
            but = sc.buttons(list,index=0)
        if ww =='2':
            but = sc.buttons(list,index=1)
        if ww =='3':
            but = sc.buttons(list,index=2)
        if ww =='4':
            but = sc.buttons(list,index=3)

    if select == 'User Summary':
        user_report(user_name)

    if select == 'User Admin':
        user_admin()
        

if __name__ == "__main__":
    main()
