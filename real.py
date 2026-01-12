import requests
import os
import json
from dotenv import load_dotenv
from time import sleep
from datetime import datetime

load_dotenv()

# ------------------------
# 인증
# ------------------------
def get_token():
    url = "https://openapi.ls-sec.co.kr:8080/oauth2/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "appkey": os.getenv("LS_APP_KEY"),
        "appsecretkey": os.getenv("LS_APP_SECRET"),
        "scope": "oob"
    }
    res = requests.post(url, headers=headers, data=data, verify=False)
    if res.status_code != 200:
        raise Exception(f"토큰 발급 실패 ❌ {res.status_code} {res.text}")
    return res.json()["access_token"]

# ------------------------
# H1_ Real 데이터 수신용
# ------------------------
def get_h1_real(access_token, shcode):
    url = "https://openapi.ls-sec.co.kr:8080/stock/real"
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "authorization": f"Bearer {access_token}"
    }
    body = {"H1InBlock": {"shcode": shcode}}
    res = requests.post(url, headers=headers, json=body, verify=False)
    if res.status_code != 200:
        print(f"[{shcode}] 수신 실패: {res.status_code} {res.text}")
        return None
    return res.json().get("H1OutBlock", {})

# ------------------------
# 실시간 확인용 루프 (print만)
# ------------------------
def realtime_h1_loop(access_token, shcodes, interval=1):
    print("✅ [H1_] 실시간 수신 대기 시작...")
    try:
        while True:
            for shcode in shcodes:
                data = get_h1_real(access_token, shcode)
                if data:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {shcode} 실시간 호가 도착 ✅")
                    print(json.dumps(data, indent=2, ensure_ascii=False))
            sleep(interval)
    except KeyboardInterrupt:
        print("⏹️ 실시간 조회 종료")

# ------------------------
# 실행
# ------------------------
if __name__ == "__main__":
    access_token = get_token()
    TARGET_SHCODES = ["005930", "000660"]  # 삼성전자, SK하이닉스
    realtime_h1_loop(access_token, TARGET_SHCODES, interval=1)
