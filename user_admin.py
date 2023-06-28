import streamlit as st
import pdfkit
import datetime
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from streamlit.components.v1 import iframe
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import io
import datetime
import json
from pathlib import Path
from datetime import date
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import extra_streamlit_components as stx
import plotly.express as px
import streamlit_antd_components as sc
import faker
from faker import Faker
import random

from streamlit_login_auth_ui.widgets import __login__
import altair as alt
from exam import welcome,load_score


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
            
def get_score():
    con = st.experimental_connection('user_db', type='sql')       
    score_db = con.query('SELECT * FROM score_table ')
    return score_db

def upload():
    uploaded_file = st.file_uploader("Choose a CSV or EXCEL file")
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
      bytes_data = uploaded_file.read()
      st.write("filename:", uploaded_file.name)
      st.info('Showing course in current EXCEL file')
      courselist = pd.read_excel(uploaded_file)
      if courselist is not None:
        st.dataframe(courselist, use_container_width=True)



def download(score_data):
    df = pd.DataFrame(score_data)
    with pd.ExcelWriter('scwwwore_0626.xlsx') as writer:
        df.to_excel(writer, sheet_name='sheet1',index=False)
    st.download_button(label="Download data as XLS",data=df,file_name='score.xlsx',mime='application/vnd.ms-excel',)
   

# 定义管理员列表
admin_list = ['Jeremy Xu', 'jeremyxu', 'gteadmin', 'xudj1']

def gen_test_data():

    Datalist = []
    f= faker.Faker()
    userlist = []
    for i in range(50):
        user= f.name()
        userlist.append(user)


    for i in range(1000):
        grade = random.choice(['B4','B5','B6','B7'])
        course_name = random.choice(['NPI Process','Test process basic ','Test code develop','Failure analysis ',
                                     'Inhouse Develop','Preload Process','AFT Introduction','Digital System'])
        version = '2023061211'
        user_name = random.choice(userlist)
        user_score  = f.random_int(25,100)
        user_dept = random.choice(['GTE','LSSC','NEC','LCFC','TJSC','India','MTY','LMH','IDU','CDP'])
        score_time = f.date_between(start_date='-1y',end_date='today').strftime('%Y%m%d%H%M')

        Datalist.append([grade, course_name, version, user_name, user_score, user_dept, score_time])

    data = pd.DataFrame(Datalist,columns=['grade','course_name','version','user_name','user_score','user_dept','score_time'])
    st.dataframe(data,use_container_width=True)
    return Datalist



def user_admin():
    list = [dict(label='Admin list', icon='check-square'),dict(label='User List', icon='explicit'),
            dict(label='Department', icon='award'),dict(label='Other Setting', icon='bar-chart'),
            dict(label='Score Data', icon='award'),dict(label='Other Setting', icon='bar-chart'),]
    but = sc.buttons(list,index=0)
    if but == 'Admin list':
        st.dataframe(admin_list,column_config={"Name":"Admin Namelist"})
        left, right = st.columns(2)
        with left:
            new = st.text_input('Input Admin name to add or delete')
        with right:
            method = st.radio('Method',['Add','Delete'],horizontal=True)
        if st.button('Confirm'):
            if new !='' and method =='Add':
                admin_list.append(new)
                st.dataframe(admin_list,column_config={"Name":"Admin Namelist"})
            if new !='' and method =='Delete' and new in admin_list:
                admin_list.remove(new)
                st.dataframe(admin_list,column_config={"Name":"Admin Namelist"})
    
    if but == 'Score Data':
        db = get_score()
        st.dataframe(db,use_container_width=True)

        gen_test_data()
        




    

if __name__ == "__main__":
    session()
   