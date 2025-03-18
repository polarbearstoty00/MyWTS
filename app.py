import streamlit as st
import requests
import json

# LS증권 API 기본 정보
BASE_URL = "https://openapi.ls-sec.co.kr:8080"
TOKEN_URL = f"{BASE_URL}/oauth2/token"

def get_access_token(app_key, app_secret):
    token_data = {
        "grant_type": "client_credentials",
        "appkey": app_key,
        "appsecretkey": app_secret,
        "scope": "oob"
    }
    token_headers = {"content-type": "application/x-www-form-urlencoded"}
    
    response = requests.post(TOKEN_URL, headers=token_headers, data=token_data)
    token_json = response.json()
    
    return token_json.get("access_token"), token_json

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
