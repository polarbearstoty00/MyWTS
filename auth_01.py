import requests
import json

# LS증권 API 기본 정보
BASE_URL = "https://openapi.ls-sec.co.kr:8080"
TOKEN_URL = f"{BASE_URL}/oauth2/token"
STOCK_ACCNO_URL = f"{BASE_URL}/stock/accno"
STOCK_MARKET_DATA_URL = f"{BASE_URL}/stock/market-data"

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

# LS증권 계좌 잔고 조회
def get_account_balance(access_token):
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {access_token}",
        "tr_cd": "t0424",
        "tr_cont": "N",
        "tr_cont_key": ""
    }
    
    body = json.dumps({
        "t0424InBlock": {
            "prcgb": "",
            "chegb": "",
            "dangb": "",
            "charge": "",
            "cts_expcode": ""
        }
    })
    
    response = requests.post(STOCK_ACCNO_URL, headers=headers, data=body)
    response_text = response.content.decode("utf-8", errors="ignore")
    account_json = json.loads(response_text)
    
    if "t0424OutBlock" in account_json and "t0424OutBlock1" in account_json:
        return account_json["t0424OutBlock"], account_json["t0424OutBlock1"]
    else:
        raise Exception("계좌 잔고 데이터를 찾을 수 없습니다.")
