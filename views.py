from django.shortcuts import render
from api.ilbong import get_ilbong
from api.db import select_tb_kospi, select_tb_basic
import json
import requests



from dotenv import load_dotenv
import os
load_dotenv()
def get_token():
    url = "https://openapi.ls-sec.co.kr:8080/oauth2/token"

    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "appkey": os.getenv("LS_APP_KEY"),
        "appsecretkey": os.getenv("LS_APP_SECRET"),
        "scope": "oob"
    }

    res = requests.post(url, headers=headers, data=data, verify=False)

    if res.status_code != 200:
        print("토큰 발급 실패 ❌, status:", res.status_code, ' ', res.text)
        return None

    return res.json().get("access_token")










def index(request):
    list_kospi = select_tb_kospi() 
    
    ilbong_raw = get_ilbong(access_token=get_token(), shcode='068270')   # 삼성전자 초기화
    if ilbong_raw:
        ilbong_raw = ilbong_raw[::-1]    
    json_ilbong = json.dumps(ilbong_raw)
    
    basic_raw = select_tb_kospi('068270')   # 삼성전자 초기화 
    json_basic = json.dumps(basic_raw)
    
    return render(request, 'index.html', {
        'kospi': list_kospi,        # 전체 리스트
        'code': '068270',           # 삼성전자 초기화
        'json_ilbong': json_ilbong, # 삼성전자 차트
        'json_basic': json_basic,   # 삼성전자 기본  정보
    })













def partial_kospi(request):
    # HTMX용 조각 뷰: 종목 리스트만 새로고침할 때
    kospi_list = select_tb_kospi()
    return render(request, '_partial_kospi.html', {'kospi': kospi_list})



def partial_detail(request):
    code = request.GET.get('code')
    ilbong_data = get_ilbong(access_token=get_token(), shcode=code)
    if ilbong_data:
        ilbong_data = ilbong_data[::-1]

    
    # 3. 나머지는 그대로
    basic_data = select_tb_kospi(code)
    
    context = {
        'code': code,
        'json_basic': json.dumps(basic_data),
        'json_ilbong': json.dumps(ilbong_data),
    }
    return render(request, '_partial_detail.html', context)






def account_view(request):
    # 나중에 여기서 DB에 저장된 내 계좌/보유종목 데이터를 가져올 겁니다.
    access_token=get_token()
    account_number = get_account_number(access_token)
    balance = get_balance(access_token, account_number)
    print(balance)
    print(type(balance))
    return render(request, 'account.html', {'balance': balance})


