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
