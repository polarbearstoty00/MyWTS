import streamlit as st
import requests
import json
from auth_01 import get_access_token

def get_account_balance(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    data = {
        "t0424InBlock": {
            "prcgb": "",
            "chegb": "",
            "dangb": "",
            "charge": "",
            "cts_expcode": ""
        }
    }
    
    response = requests.post(STOCK_ACCNO_URL, headers=headers, json=data)
    return response.json()

# Streamlit UI
st.title("WTS 로그인 페이지")

app_key = st.text_input("App Key", type="password")
app_secret = st.text_input("App Secret Key", type="password")

if st.button("로그인"):
    if app_key and app_secret:
        access_token, response_json = get_access_token(app_key, app_secret)
        if access_token:
            st.success("로그인 성공! Access Token 발급 완료.")
            st.session_state["access_token"] = access_token
            st.session_state["logged_in"] = True
        else:
            st.error(f"로그인 실패: {response_json}")
    else:
        st.warning("App Key와 Secret Key를 입력하세요.")

if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.subheader("계좌 잔고")
    balance_data = get_account_balance(st.session_state["access_token"])
    if balance_data.get("rsp_cd") == "00000":
        st.json(balance_data["t0424OutBlock"])
        st.write("보유 종목 내역")
        st.json(balance_data["t0424OutBlock1"])
    else:
        st.error(f"잔고 조회 실패: {balance_data.get('rsp_msg', '알 수 없는 오류')}")
