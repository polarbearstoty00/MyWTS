import streamlit as st
import requests
import json
import pandas as pd
import traceback
from login_module.authentication_LS import get_access_token
from main_page import show_main_page

# 페이지 상태 초기화
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if st.session_state["page"] == "login":
    st.title("WTS 로그인 페이지")
    
    app_key = st.text_input("App Key", type="password")
    app_secret = st.text_input("App Secret Key", type="password")
    
    if st.button("로그인"):
        if app_key and app_secret:
            access_token, response_json = get_access_token(app_key, app_secret)
            if access_token:
                st.success("로그인 성공! Access Token 발급 완료.")
                st.session_state["access_token"] = access_token
                st.session_state["page"] = "main"  # 메인 페이지로 이동
                st.rerun() # 화면 갱신
            else:
                st.error(f"로그인 실패: {response_json}")
        else:
            st.warning("App Key와 Secret Key를 입력하세요.")

# 메인 페이지 함수 호출
if st.session_state["page"] == "main":
    show_main_page()
