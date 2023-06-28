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

from streamlit_login_auth_ui.widgets import __login__
import altair as alt
from exam import welcome,load_score


# wkhtmltopdf_path = os.path.join(os.getcwd(), 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')
# if not os.path.isfile(wkhtmltopdf_path):
#    raise FileNotFoundError("wkhtmltopdf executable not found at %s" % wkhtmltopdf_path)
# Configure pdfkit to use the binary
# config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

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
            


def generator(student,course):
    # 打开模板图片
    template = Image.open('certificate_template.png')
    # 二维码
    code = student + course + datetime.datetime.now().strftime("%Y%m%d")
    qrcode_img = qrcode.make(code)
    template.paste(qrcode_img, (500, 850), mask=None)
    

    # 创建一个draw对象
    draw = ImageDraw.Draw(template)
    # 在模板上添加文字
    text1 = 'This Certification is presented to following employee with outstanding performance in '
    font = ImageFont.truetype("arial", 60, encoding="unic")  # 设置字体
    draw.text((500, 500), text1, font=font, fill='white')
    
    text3 = 'LME Engineering Trainning and Certification Activities! '
    font = ImageFont.truetype('arial.ttf', 60)
    draw.text((800, 600), text3, font=font, fill='white')

    text2 = student
    font = ImageFont.truetype('arialbd.ttf', 80)
    draw.text((1200, 800), text2, font=font, fill='white')


    text4 = 'Course: '+ course
    font = ImageFont.truetype('simhei.TTF', 70,encoding='unic')
    draw.text((1200, 1000), text4, font=font, fill='white')

    text5 = 'Date: '+datetime.datetime.now().strftime("%Y%m%d")
    font = ImageFont.truetype('arial.ttf', 70)
    draw.text((1200, 1200), text5, font=font, fill='white')

    
    
    # 保存证书图片


    file_dir = os.getcwd()
    file_name =student +'_' + course +'_'+ datetime.datetime.now().strftime("%Y%m%d") +'.png'
    save_pic = os.path.join(file_dir,'PNG',file_name) 

    template.save(save_pic)
    st.write('Your Certification shows like following:')
    st.image(template, caption='Certification for you')
    return save_pic,file_name

# 生成二维码
def gen_qrcode(info):
    img = qrcode.make(info)
    with open('qrcode.png', 'wb') as f:
        img.save(f)

def get_score():
    con = st.experimental_connection('user_db', type='sql')           
    score_db = con.query('SELECT * FROM score_table ')
    return score_db

def gen_cert(username):
    session()
    welcome()
    st.divider()
    st.write("This app make a PNG certification file based on user's course name and score !")

    left, right = st.columns(2)

    right.write("Here's the template we'll be using:")
    right.image("certificate_template.png", width=300)

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    template = env.get_template("template.html")

    with left :

        score_db = get_score()
        df = pd.DataFrame(score_db, columns=["grade", "course_name", "version",'user_name','user_score','user_dept','score_time'])

        version_list= sorted(set(score_db.iloc[:,2].to_list()),reverse=True)
        version = version_list[0]

        score_list= sorted(set(score_db.iloc[:,4].to_list()),reverse=True)
        score_best = score_list[0]

        score_pd = df.loc[(df['user_name']==username) & (df['version']==version) & (df['user_score']>=80) & (df['user_score']==score_best) ,: ]
        score_unique = score_pd.drop_duplicates(subset='course_name')
        
        if score_pd.empty:
            st.write('Can not find record meet standard. Using dummy score for test')
            student_str = 'Jerry Mark'
            grade = ' B6'
            course = 'ODM Test Process'
            score = 100

        else: 
            grade_list= sorted(set(score_unique.iloc[:,0].to_list()),reverse=True)

            course_list= sorted(set(score_unique.iloc[:,1].to_list()),reverse=True)
            course_choice = st.radio('Select the course you want for certification',course_list,horizontal=True)
            grade_pd = score_unique.loc[(df['course_name']==course_choice) ,: ]
            grade_list= sorted(set(grade_pd.iloc[:,0].to_list()),reverse=True)
            grade =st.radio('Select the grade',grade_list,horizontal=True)

            student_str = username.title()
            course = course_choice
            score = score_best

        course_str = grade +"-" +course
        ll,rr = st.columns(2)
        with ll:
            st.write('Name: ',student_str)
        with rr:
            st.write('Score: ',str(score))

        submit = st.button("Generate Certification")

    if submit:
        save_pic, file_name = generator(student_str,course_str)


        if save_pic:
            st.balloons()
            # st.write(html, unsafe_allow_html=True)
            # st.write("")
            with open(save_pic, "rb") as file:
                btn = st.download_button(label=" ⬇️ Download PNG Certification",data=file,file_name=file_name,mime="image/png")
                if btn:
                    st.success('Download finish') 
            st.success("🎉 Your diploma was generated!")    
        else: 
            st.error('Pic generation error')

