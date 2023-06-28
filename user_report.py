import streamlit as st
import pdfkit
import datetime
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from streamlit.components.v1 import iframe
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import datetime
import json
from pathlib import Path
from datetime import date
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import extra_streamlit_components as stx
import plotly.express as px

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
            
def get_score(username):
    con = st.experimental_connection('user_db', type='sql') 
    data = dict()
    data['user']=username          
    score_db = con.query('SELECT * FROM score_table where user_name =:user',params=data)
    return score_db



def user_report(username):
    welcome()
    
    score_db=get_score(username)
    df = pd.DataFrame(score_db, columns=["grade", "course_name", "version",'user_name','user_score','user_dept','score_time'])

    version_list= sorted(set(score_db.iloc[:,2].to_list()),reverse=True)
    version = version_list[0]

    score_list= sorted(set(score_db.iloc[:,4].to_list()),reverse=True)
    score_best = score_list[0]

    score_pd = df.loc[(df['user_name']==username) & (df['version']==version) & (df['user_score']>=80) & (df['user_score']==score_best) ,: ]
    score_unique = score_pd.drop_duplicates(subset='course_name')
    st.write('User Score summary')
    st.write(score_unique)
    chart_data = pd.DataFrame(score_unique,columns=["course_name", "user_score"])
    st.bar_chart(data=chart_data, x='course_name', y='user_score', width=300, height=0, use_container_width=False)



if __name__ == "__main__":
    session()
   