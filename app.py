import streamlit as st
import requests
import json
import pandas as pd
from auth_01 import get_access_token
from auth_01 import get_account_balance

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

if st.session_state["page"] == "main":
    st.title("WTS 메인 페이지")
    st.subheader("계좌 잔고")
    
    try:
        balance_summary, balance_details = get_account_balance(st.session_state["access_token"])
        st.write("보유 종목 내역")
        
        # 보유 종목을 표 형태로 변환하여 표시
        if balance_details:
            df = pd.DataFrame(balance_details)
            df = df.rename(columns={"hname": "종목명"}).set_index("종목명")  # 종목명을 인덱스로 설정
            df = df[["janqty", "sunikrt", "appamt", "dtsunik", "price", "pamt", "mamt", "fee", "tax"]]  # 평가금액과 평가손익만 표시
            df = df.rename(columns={"janqty" : "잔고수량", "sunikrt" : "수익률", "appamt": "평가금액", "dtsunik": "평가손익", "price" : "현재가",
                                   "pamt" : "평균단가", "mamt" : "매입금액", "fee" : "수수료", "tax" : "제세금"})  # 컬럼명 변경
            # 화폐단위 적용
            df["평가금액"] = df["평가금액"].apply(lambda x: f"{x:,.0f}")
            df["평가손익"] = df["평가손익"].apply(lambda x: f"{x:,.0f}")
            df["현재가"] = df["현재가"].apply(lambda x: f"{x:,.0f}")
            df["평균단가"] = df["평균단가"].apply(lambda x: f"{x:,.0f}")
            df["매입금액"] = df["매입금액"].apply(lambda x: f"{x:,.0f}")
            df["수수료"] = df["수수료"].apply(lambda x: f"{x:,.0f}")
            df["제세금"] = df["제세금"].apply(lambda x: f"{x:,.0f}")

            st.dataframe(df)
        else:
            st.write("보유 종목이 없습니다.")
    except Exception as e:
        st.error(f"잔고 조회 실패: {str(e)}")
    
    if st.button("로그아웃"):
        st.session_state.clear()
        st.session_state["page"] = "login"
        st.rerun()
