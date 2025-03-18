import streamlit as st
from .auth_01 import get_access_token

# Streamlit UI
st.title("WTS 로그인 페이지")

app_key = st.text_input("App Key", type="password")
app_secret = st.text_input("App Secret Key", type="password")

if st.button("로그인"):
    if app_key and app_secret:
        access_token, response_json = get_access_token(app_key, app_secret)
        if access_token:
            st.success("로그인 성공! Access Token 발급 완료.")
            st.text_area("Access Token", access_token, height=100)
        else:
            st.error(f"로그인 실패: {response_json}")
    else:
        st.warning("App Key와 Secret Key를 입력하세요.")
