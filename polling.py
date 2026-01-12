import requests
from dotenv import load_dotenv
import os
import json
from time import sleep
from datetime import datetime

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()


# ------------------------
# 인증 및 계좌 조회
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


def get_account_number(access_token):
    url = "https://openapi.ls-sec.co.kr:8080/stock/accno"
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "authorization": f"Bearer {access_token}",
        "tr_cd": "CSPAQ22200",
        "tr_cont": "N",
        "tr_cont_key": ""
    }
    res = requests.post(url, headers=headers, data={}, verify=False)
    return res.json()["CSPAQ22200OutBlock1"]["AcntNo"]


# ------------------------
# TR 호출: 호가 조회
# ------------------------
def get_hoga(access_token, shcode):
    url = "https://openapi.ls-sec.co.kr:8080/stock/market-data"
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "authorization": f"Bearer {access_token}",
        "tr_cd": "t1101",
        "tr_cont": "N",
        "tr_cont_key": ""
    }
    body = {"t1101InBlock": {"shcode": shcode}}
    res = requests.post(url, headers=headers, json=body, verify=False)
    return res.json().get("t1101OutBlock", {})


# ------------------------
# 실시간 반복 조회
# ------------------------
def realtime_hoga_loop(access_token, shcodes, interval=1):
    """
    shcodes: 실시간으로 조회할 종목코드 리스트
    interval: TR 반복 호출 간격(초)
    """
    print("✅ 실시간 호가 조회 시작...")
    try:
        while True:
            for shcode in shcodes:
                hoga = get_hoga(access_token, shcode)
                ask1 = hoga.get("askprc1", "-")
                bid1 = hoga.get("bidprc1", "-")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {shcode} | 매도: {ask1} / 매수: {bid1}")
            sleep(interval)
    except KeyboardInterrupt:
        print("⏹️ 실시간 조회 종료")


# ------------------------
# 실행
# ------------------------
if __name__ == "__main__":
    access_token = get_token()
    account_number = get_account_number(access_token)
    print(f"계좌번호: {account_number}")

    TARGET_SHCODES = ["005930", "000660"]  # 삼성전자, SK하이닉스 예시
    realtime_hoga_loop(access_token, TARGET_SHCODES, interval=1)
