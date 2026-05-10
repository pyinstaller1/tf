from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from api.start_kospi import set_kospi, set_kospi_1day
from api.ilbong import *
from api.db import *

from django.db import connection, transaction
from django.http import HttpResponse

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


def start_kospi(request):
    set_kospi()
    return redirect('index')

def start_kospi_1day(request):
    set_kospi_1day()
    return redirect('index')






def get_ilbong_total_view(request):
    return StreamingHttpResponse(get_ilbong_total(), content_type='text/event-stream')

def get_ilbong_1day_view(request):
    return StreamingHttpResponse(get_ilbong_1day(), content_type='text/event-stream')





def render_to_group_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT group_name, group_order 
            FROM tb_gwansim 
            ORDER BY group_order ASC
        """)
        groups = cursor.fetchall()

    # 전체 페이지가 아니라 리스트 조각만 있는 '별도의 템플릿'을 만들거나, 
    # 조건부 렌더링을 사용하여 조각만 보냅니다.
    return render(request, 'gwansim_list_snippet.html', {'groups': groups})


















def gwansim_view(request):
    groups = select_tb_gwansim_group()
    raw_kospi = select_tb_kospi() # 튜플 리스트 가져오기
    
    # 튜플 [0], [1], [2], [3] 데이터를 딕셔너리로 변환
    kospi_list = [
        {
            'shcode': s[0],    # 종목코드
            'hname': s[1],     # 종목명
            'price': s[2],     # 현재가
            'rate': s[3]       # 등락율
        } for s in raw_kospi
    ]
    
    return render(request, 'gwansim.html', {
        'groups': groups,
        'kospi': kospi_list,
    })





def add_gwansim_stock_view(request):

    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        shcode = request.POST.get('shcode')
        
        if group_id and shcode:
            insert_tb_gwansim_stock(group_id, shcode)
            
    return redirect('gwansim')




def add_gwansim_group_view(request):

    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        
        if group_name:
            insert_tb_gwansim_group(group_name)
            
    return redirect('gwansim')




def get_gwansim_stock_view(request):
    group_id = request.GET.get('group_id')
    
    # 1. db.py의 함수를 사용하여 그룹 내 종목 리스트를 가져옵니다.
    # [{ 'shcode': '005930', 'hname': '삼성전자' }, ...] 형태의 리스트 기대
    stocks = select_gwansim_stocks(group_id) 
    
    # 2. JSON 형태로 반환하여 자바스크립트에서 처리하게 합니다.
    return JsonResponse({'stocks': stocks})
























































def index(request):
    check_web = request.GET.get('check_web', 'false') 
    list_kospi = select_tb_kospi() 
    
    initial_code = '068270' # 셀트리온
    
    if check_web == 'true':
        ilbong_data = get_ilbong(access_token=get_token(), shcode=initial_code)
    else:
        ilbong_data = get_ilbong_db(shcode=initial_code) 
    
    json_ilbong = json.dumps(ilbong_data)
    
    basic_raw = select_tb_kospi(initial_code)
    json_basic = json.dumps(basic_raw)
    
    return render(request, 'index.html', {
        'kospi': list_kospi,
        'code': initial_code,
        'json_ilbong': json_ilbong,
        'json_basic': json_basic,
    })
















def partial_kospi(request):
    # HTMX용 조각 뷰: 종목 리스트만 새로고침할 때
    kospi_list = select_tb_kospi()
    return render(request, '_partial_kospi.html', {'kospi': kospi_list})



def partial_detail(request):
    code = request.GET.get('code')
    check_web = request.GET.get('check_web')


    if check_web == 'true':
        ilbong_data = get_ilbong(access_token=get_token(), shcode=code)
    else:
        ilbong_data = get_ilbong_db(shcode=code)


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


