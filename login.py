# One Page app with streamlit

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


DEFAULT_PAGE = "login.py"
SECOND_PAGE_NAME = "User Home"

# all pages request
def get_all_pages():
    default_pages = get_pages(DEFAULT_PAGE)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages

# clear all page but not login page
def clear_all_but_first_page():
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages()

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()

# show all pages
def show_all_pages():
    current_pages = get_pages(DEFAULT_PAGE)

    saved_pages = get_all_pages()

    # Replace all the missing pages
    for key in saved_pages:
        if key not in current_pages:
            current_pages[key] = saved_pages[key]

    _on_pages_changed.send()

# Hide default page
def hide_page(name: str):
    current_pages = get_pages(DEFAULT_PAGE)

    for key, val in current_pages.items():
        if val["page_name"] == name:
            del current_pages[key]
            _on_pages_changed.send()
            break

# calling only default(login) page  
clear_all_but_first_page()

def get_username(self):
        if st.session_state['LOGOUT_BUTTON_HIT'] == False:
            fetched_cookies = self.cookies
            if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                username=fetched_cookies['__streamlit_login_signup_ui_username__']
                return username


def main():

    __login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 220, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = True, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()
    username= get_username(__login__obj)


    if LOGGED_IN == True:
        st.markdown("Your Streamlit Application Begins here!")
        st.markdown(st.session_state)
        st.write(username)
                                  

    if LOGGED_IN == True:
        show_all_pages()  # call all page
        hide_page(DEFAULT_PAGE.replace(".py", ""))  # hide first page
        switch_page(SECOND_PAGE_NAME)   # switch to second page
    else:
        clear_all_but_first_page()  # clear all page but show first page


if __name__ == "__main__":
    main()