import streamlit as st
import requests
import json
import pandas as pd
from auth_01 import get_access_token
from auth_01 import get_account_balance
from auth_01 import get_account_summary

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

    # 계좌 요약 정보 출력
    try:
        account_summary_1, account_summary_2 = get_account_summary(st.session_state["access_token"])
        st.write("계좌 요약 내역")
    
        # 먼저 데이터 구조 확인용 출력 (디버깅용)
        st.write("account_summary_1 구조:")
        st.write(type(account_summary_1))
        st.json(account_summary_1)
    
        st.write("account_summary_2 구조:")
        st.write(type(account_summary_2))
        st.json(account_summary_2)
    
        # account_summary_2 처리
        if isinstance(account_summary_2, dict):  # 딕셔너리인 경우
            # 딕셔너리를 리스트로 변환하여 DataFrame 생성
            df_summary = pd.DataFrame([account_summary_2])
        elif isinstance(account_summary_2, list) and account_summary_2:  # 리스트이고 비어있지 않은 경우
            df_summary = pd.DataFrame(account_summary_2)
        else:
            st.warning("계좌 요약 정보의 형식이 예상과 다릅니다.")
            st.write(account_summary_2)
            df_summary = None
    
        # DataFrame이 생성된 경우에만 처리
        if df_summary is not None:
            # 컬럼이 존재하는지 확인 후 컬럼명 변경
            columns_to_rename = {
                "BalEvalAmt": "총 평가 금액",
                "Dps": "예수금",
                "PnlRat": "총 손익률"
            }
        
            # 실제 존재하는 컬럼만 변경
            rename_dict = {k: v for k, v in columns_to_rename.items() if k in df_summary.columns}
            if rename_dict:
                df_summary = df_summary.rename(columns=rename_dict)
        
            # 컬럼이 존재하는지 확인 후 형식 변환
            if "총 평가 금액" in df_summary.columns:
                df_summary["총 평가 금액"] = df_summary["총 평가 금액"].astype(float).apply(lambda x: f"{x:,.0f}원")
            if "예수금" in df_summary.columns:
                df_summary["예수금"] = df_summary["예수금"].astype(float).apply(lambda x: f"{x:,.0f}원")
            if "총 손익률" in df_summary.columns:
                df_summary["총 손익률"] = df_summary["총 손익률"].astype(float).apply(lambda x: f"{x:.2f}%")
        
            st.dataframe(df_summary)
        else:
            st.write("계좌 요약 정보가 없거나 처리할 수 없는 형식입니다.")
    except Exception as e:
        st.warning(f"계좌 요약 조회 실패: {str(e)}")
        # 에러 상세 정보 출력
        import traceback
        st.write(traceback.format_exc())

    # 보유 종목 내역
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
