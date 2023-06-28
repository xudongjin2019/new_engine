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
import plotly.express as px
import streamlit as st
import streamlit_authenticator as stauth
import extra_streamlit_components as stx
import plotly.express as px
import streamlit_antd_components as sc
import faker
from faker import Faker
import random
import plotly.figure_factory as ff
import numpy as np
from numpy import *

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
        user_score  = f.random_int(50,100)
        user_dept = random.choice(['GTE','LSSC','NEC','LCFC','TJSC','India','MTY','LMH','IDU','CDP'])
        score_time = f.date_between(start_date='-1y',end_date='today').strftime('%Y%m%d%H%M')

        Datalist.append([grade, course_name, version, user_name, user_score, user_dept, score_time])

    data = pd.DataFrame(Datalist,columns=['grade','course_name','version','user_name','user_score','user_dept','score_time'])
    # st.dataframe(data,use_container_width=True)
    return Datalist,userlist

def show_data(data):
    st.subheader("Define a custom colorscale")
    df = data
    fig = px.scatter(df,x="sepal_width",y="sepal_length",color="sepal_length",color_continuous_scale="reds",)

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

def get_chart_dept(data):

    df = pd.DataFrame(data,columns=['grade','course_name','version','user_name','user_score','user_dept','score_time'])
    # Add histogram data
    set1 = df.loc[(df['user_dept']=='GTE'),['user_score']]
    d1 = set1.iloc[:,0].to_list()
    b1 = mean(d1)
    set2 = df.loc[(df['user_dept']=='LSSC'),['user_score']]
    d2 = set2.iloc[:,0].to_list()
    b2 = mean(d2)
    set3 = df.loc[(df['user_dept']=='TJSC'),['user_score']]
    d3 = set3.iloc[:,0].to_list()
    b3 = mean(d3)
    set4 = df.loc[(df['user_dept']=='LMH'),['user_score']]
    d4 = set4.iloc[:,0].to_list()
    b4 = mean(d4)

    # Group data together

    x1 = 1.2*np.random.randn(200) +80
    x2 = 1.1*np.random.randn(200) +75
    x3 = np.random.randn(200) +74
    x4 = np.random.randn(200) +70
    hist_data = [x1, x2, x3, x4]

    group_labels = ['GTE','LSSC','TJSC','LMH']
    avg = [b1,b2,b3,b4]
    st.write('Distribution')
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,curve_type='kde' ,show_hist=True,show_rug=False,bin_size=.1)
    st.plotly_chart(fig, theme=None,use_container_width=True)

    st.write('Average score ')
    # prepare data : 
    newdf = df.copy()

    # 获取各工厂的平均分数
    newdf2 = newdf.groupby('user_dept')['user_score'].mean().reset_index()
    newdf2.sort_values(by="user_score",axis=0,ascending=True,inplace=True)
    fig1 = px.bar(newdf2,color="user_score", x='user_dept',y='user_score')
    st.plotly_chart(fig1, theme=None,use_container_width=True)



def get_chart_user(data,user):

    

    df = pd.DataFrame(data,columns=['grade','course_name','version','user_name','user_score','user_dept','score_time'])
    score_pd = df.loc[(df['user_name']==user),: ]

    score_unique = score_pd.drop_duplicates(subset='course_name')
    fig = px.line_polar(score_unique, r='user_score', theta='course_name', line_close=True)
    left,right = st.columns(2)
    with left:
        st.dataframe(score_unique,use_container_width=True,hide_index=True)
    with right:
        st.plotly_chart(fig, theme=None,use_container_width=True)
    

    # 获取所有用户的user total Score 
    st.header('Total score by user')
    newdf4 = df.copy()
    df5 = newdf4.groupby('user_name')['user_score'].sum().reset_index()
    df5.sort_values(by="user_score",axis=0,ascending=False,inplace=True)
    fig2 = px.bar(df5,color="user_score", x='user_score',y='user_name',orientation='h')
    left1,right1 = st.columns([1,3])
    with left1:
        st.dataframe(df5,use_container_width=True,hide_index=True)
    with right1:
        st.plotly_chart(fig2, theme=None,use_container_width=True)
    
    

def value():

    list = [dict(label='Evaluation by Dept', icon='check-square'),dict(label='Evaluation by User', icon='explicit'),
            dict(label='Department', icon='award'),dict(label='Other Setting', icon='bar-chart'),
            dict(label='Score Data', icon='award'),dict(label='Other Setting', icon='bar-chart'),]
    
    but = sc.buttons(list,index=0,return_index=True)

    if but == 0:
        st.header('Score distribution by department')
        data,userlist = gen_test_data()
        get_chart_dept(data)

    if but == 1:
        st.header('User Evaluation')
        data,userlist = gen_test_data()
        userlist1 = userlist[:10]
        user = st.radio('Select user',userlist1,horizontal=True)
        if user :
            get_chart_user(data,user)


        




    

if __name__ == "__main__":
    session()
   