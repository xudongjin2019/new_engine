import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import numpy as np
import pdfkit
import datetime
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

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

wkhtmltopdf_path = os.path.join(os.getcwd(), 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')
if not os.path.isfile(wkhtmltopdf_path):
    raise FileNotFoundError("wkhtmltopdf executable not found at %s" % wkhtmltopdf_path)
# Configure pdfkit to use the binary
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

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
            


def gen_cert(student,course):
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
    font = ImageFont.truetype('arial.ttf', 70,encoding='unic')
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


def main():

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


        else:
            hide_pages(['Course Admin','Data Summary','User Admin'])
            st.sidebar.write('hellow ',username,'with email',get_email(username))


    st.write("# LME Engineering Certification System! 👋")
    st.divider()

    st.write("This app make a PNG certification file based on user's course name and score !")

    left, right = st.columns(2)

    right.write("Here's the template we'll be using:")
    right.image("certificate_template.png", width=300)

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    template = env.get_template("template.html")


    left.write("confirm the data:")
    form = left.form("template_form")
    with form:
       
        if st.session_state.exam_grade:
            student_str = username.title()
            grade = str(st.session_state.exam_grade)
            course = str(st.session_state.exam_name)
            score = int(st.session_state.exam_score)
        else:
            student_str = 'Jerry Mark'
            grade = ' B6'
            course = 'ODM Test Process'
            score = 100
        course_str = grade +" " +course
        st.write('Name: ',student_str)
        st.write('Course: ',course_str)
        st.write('Score: ',str(score))
        submit = form.form_submit_button("Generate Certification")


    if submit:
        if score >= 80: 
            save_pic, file_name = gen_cert(student_str,course_str)

            if save_pic:
                st.balloons()
                st.success("🎉 Your diploma was generated!")
                # st.write(html, unsafe_allow_html=True)
                # st.write("")
                with open(save_pic, "rb") as file:
                    btn = st.download_button(label=" ⬇️ Download PNG Certification",data=file,file_name=file_name,mime="image/png")
                    if btn:
                        st.success('Download finish')     
            else: 
                st.error('Pic generation error')

            html = template.render(student=student_str,course=course_str,date=date.today().strftime("%B %d, %Y"),)
            pdf = pdfkit.from_string(html, False,configuration=config)
            file = student_str +'_' + course_str +'_'+ datetime.datetime.now().strftime("%Y%m%d") +'.pdf'
            if pdf:
                st.download_button("⬇️ Download PDF Certification",data=pdf,file_name=file,mime="application/octet-stream",)
            else: 
                st.error('PDF Generation error')

        else: 
            st.error('Score <80, can not get certification')

if __name__ == "__main__":
    session()
    main()