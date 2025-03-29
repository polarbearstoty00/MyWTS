import streamlit as st

if st.session_state["page"] == "main":
    st.title("WTS 메인 페이지")
    st.subheader("계좌 잔고")

    # 계좌 요약 정보 출력
    try:
        account_summary_1, account_summary_2 = get_account_summary(st.session_state["access_token"])
    
        st.write("계좌 기본 정보")
        # 계좌 기본 정보 표시
        account_info_df = pd.DataFrame({
            "계좌번호": [account_summary_1.get("AcntNo", "정보 없음")],
            "계좌명": [account_summary_2.get("AcntNm", "정보 없음")],
            "지점명": [account_summary_2.get("BrnNm", "정보 없음")]
        })
        st.dataframe(account_info_df, hide_index=True)
    
        st.write("계좌 잔고 요약")
        # 중요 잔고 정보만 선택하여 표시
        summary_data = {
            "총 평가 금액": account_summary_2.get("BalEvalAmt", 0),
            "예수금": account_summary_2.get("Dps", 0),
            "총 손익률": account_summary_2.get("PnlRat", 0),
            "D+2 출금가능금액": account_summary_2.get("D2PrsmptWthdwAbleAmt", 0),
            "주문가능금액": account_summary_2.get("SeOrdAbleAmt", 0),
            "대용금액": account_summary_2.get("SubstAmt", 0),
            "예탁자산총액": account_summary_2.get("DpsastTotamt", 0)
        }
    
        # DataFrame으로 변환
        summary_df = pd.DataFrame([summary_data])
    
        # 숫자 형식 변환
        for col in ["총 평가 금액", "예수금", "D+2 출금가능금액", "주문가능금액", "대용금액", "예탁자산총액"]:
            summary_df[col] = summary_df[col].astype(float).apply(lambda x: f"{x:,.0f}원")
    
        # 손익률 형식 변환
        summary_df["총 손익률"] = summary_df["총 손익률"].astype(float).apply(lambda x: f"{x:.2f}%")
    
        # 표 형태로 표시
        st.dataframe(summary_df, hide_index=True)
        
    except Exception as e:
        st.error(f"계좌 요약 조회 실패: {str(e)}")
        st.write(traceback.format_exc())

    st.divider() # 구분줄 추가
    
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
