import requests
import mariadb
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time
import asyncio
import websockets
import ssl
import numpy as np
from api.db import *

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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













import pandas as pd
import numpy as np
import time
import requests
import math

# ----------------------------------------------------------------------
# 통합 지표 계산 함수
# ----------------------------------------------------------------------

def get_ilbong_rsi(ilbong):
    """
    주어진 일봉 데이터(ilbong: List of Dict)에 RSI, MACD, Bollinger Band, 일목균형표 
    (ilmok_a/b, 돌파, 양운/음운)를 모두 계산하여 추가합니다.
    """
    if not ilbong:
        return []

    # 1. 날짜 오름차순 정렬 (모든 지표 계산의 기본 조건)
    ilbong.sort(key=lambda row: row['date'])

    # 2. Pandas DataFrame으로 변환 (계산 효율성 극대화)
    df = pd.DataFrame(ilbong)
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['close'] = pd.to_numeric(df['close']) 
    
    closes = df['close']
    
    # ----------------------------------------------------------------------
    # A. RSI (N=14)
    # ----------------------------------------------------------------------
    N_rsi = 14
    delta = closes.diff()
    u = delta.apply(lambda x: x if x > 0 else 0)
    d = delta.apply(lambda x: -x if x < 0 else 0)

    # 초기값 설정 (rolling mean 사용)
    # EMA 방식 계산 (Wilder's smoothing)
    alpha_rsi = 1 / N_rsi
    df['au'] = u.ewm(com=N_rsi-1, adjust=False).mean()
    df['ad'] = d.ewm(com=N_rsi-1, adjust=False).mean()

    # RSI 계산
    # df['rsi14'] = 100 - (100 / (1 + df['au'] / df['ad'])) # 표준 RSI 공식
    # 사용자 로직 (100 * AU / (AU + AD))
    df['rsi14'] = 100 * df['au'] / (df['au'] + df['ad'])

    # ----------------------------------------------------------------------
    # B. MACD (EMA12, EMA26, Signal 9)
    # ----------------------------------------------------------------------
    ema_short, ema_long, signal_n = 12, 26, 9
    
    # EMA 계산 (표준 MACD 방식: adjust=False 사용)
    df['ema12'] = closes.ewm(span=ema_short, adjust=False).mean()
    df['ema26'] = closes.ewm(span=ema_long, adjust=False).mean()
    
    df['macd'] = df['ema12'] - df['ema26']
    
    # MACD Signal (MACD9)
    df['macd9'] = df['macd'].ewm(span=signal_n, adjust=False).mean()
    
    # ----------------------------------------------------------------------
    # C. Bollinger Band (N=20)
    # ----------------------------------------------------------------------
    N_bol = 20
    df['ma20_bol'] = closes.rolling(window=N_bol).mean()
    stddev_20 = closes.rolling(window=N_bol).std()
    df['bol_u'] = df['ma20_bol'] + stddev_20 * 2
    df['bol_l'] = df['ma20_bol'] - stddev_20 * 2
    
    # 볼린저 밴드 폭 및 돌파 여부
    df['bol_width'] = df['bol_u'] - df['bol_l']
    # 전체 계산된 폭의 평균 계산
    bol_mean = df['bol_width'].mean()
    
    df['bol_size'] = np.where(
        df['bol_u'].isna(), None, # NaN이면 None 처리
        np.where(df['bol_width'] > bol_mean * 1.5, 'Big', 'Small')
    )
    
    df['bol_dolpa'] = np.where(
        df['bol_u'].isna(), None,
        np.where(df['close'] > df['bol_u'], '상향돌파',
                 np.where(df['close'] < df['bol_l'], '하향돌파', '보통'))
    )

    # ----------------------------------------------------------------------
    # D. 일목균형표 (키움 스타일)
    # ----------------------------------------------------------------------
    
    # Kijun (26일 최고가/최저가 중간값)
    high_26 = df['high'].rolling(window=26).max()
    low_26 = df['low'].rolling(window=26).min()
    kijun = (high_26 + low_26) / 2

    # Tenkan (9일 최고가/최저가 중간값)
    high_9 = df['high'].rolling(window=9).max()
    low_9 = df['low'].rolling(window=9).min()
    tenkan = (high_9 + low_9) / 2

    # ilmok_a (선행스팬 1): (kijun + tenkan) / 2 를 26일 선행 (shift 25)
    df['ilmok_a'] = ((kijun + tenkan) / 2).shift(26 - 1)

    # ilmok_b (선행스팬 2): 52일 최고가/최저가의 중간값을 26일 선행
    high_52 = df['high'].rolling(window=52).max()
    low_52 = df['low'].rolling(window=52).min()
    df['ilmok_b'] = ((high_52 + low_52) / 2).shift(26 - 1)
    
    # 구름 종류 (ilmok_yang)
    df['ilmok_yang'] = np.where(df['ilmok_a'].isna() | df['ilmok_b'].isna(),
                                None, # NaN이면 None 처리
                                np.where(df['ilmok_a'] > df['ilmok_b'], '양운', '음운')
    )
    
    # 구름 돌파 여부 (ilmok_dolpa) - 키움 로직 반영
    nan_condition = df['ilmok_a'].isna() | df['ilmok_b'].isna()

    df['ilmok_dolpa'] = np.where(
        nan_condition,
        None, # NaN이면 None 처리
        np.where(
            (df['high'] > df['ilmok_a']) & (df['high'] > df['ilmok_b']),
            "상향돌파",
            np.where(
                (df['low'] < df['ilmok_a']) & (df['low'] < df['ilmok_b']),
                "하향돌파",
                np.where(
                    ((df['low'] > df['ilmok_a']) & (df['low'] < df['ilmok_b'])) | \
                    ((df['low'] < df['ilmok_a']) & (df['low'] > df['ilmok_b'])) | \
                    ((df['high'] > df['ilmok_a']) & (df['high'] < df['ilmok_b'])) | \
                    ((df['high'] < df['ilmok_a']) & (df['high'] > df['ilmok_b'])),
                    "구름내부",
                    "보통"
                )
            )
        )
    )
    
    # ----------------------------------------------------------------------
    # 7. 최종 결과를 기존 ilbong 리스트에 병합
    # ----------------------------------------------------------------------
    
    # 필요한 열 선택 및 Dict 리스트로 변환
    indicator_cols = ['rsi14', 'macd', 'macd9', 'bol_u', 'bol_l', 'bol_size', 'bol_dolpa', 
                      'ilmok_a', 'ilmok_b', 'ilmok_yang', 'ilmok_dolpa']
    
    # 기존 ilbong 리스트에 없는 MA 값은 get_ilbong에서 이미 처리되었으므로 추가하지 않음
    
    for i, row in enumerate(ilbong):
        # RSI
        row['rsi14'] = round(df['rsi14'].iloc[i], 4) if pd.notna(df['rsi14'].iloc[i]) else None
        
        # MACD
        row['macd'] = round(df['macd'].iloc[i], 4) if pd.notna(df['macd'].iloc[i]) else None
        row['macd9'] = round(df['macd9'].iloc[i], 4) if pd.notna(df['macd9'].iloc[i]) else None
        
        # Bollinger Band
        row['bol_u'] = round(df['bol_u'].iloc[i], 2) if pd.notna(df['bol_u'].iloc[i]) else None
        row['bol_l'] = round(df['bol_l'].iloc[i], 2) if pd.notna(df['bol_l'].iloc[i]) else None
        row['bol_size'] = df['bol_size'].iloc[i] if pd.notna(df['bol_size'].iloc[i]) else None
        row['bol_dolpa'] = df['bol_dolpa'].iloc[i] if pd.notna(df['bol_dolpa'].iloc[i]) else None
        
        # 일목균형표
        row['ilmok_a'] = round(df['ilmok_a'].iloc[i], 2) if pd.notna(df['ilmok_a'].iloc[i]) else None
        row['ilmok_b'] = round(df['ilmok_b'].iloc[i], 2) if pd.notna(df['ilmok_b'].iloc[i]) else None
        row['ilmok_yang'] = df['ilmok_yang'].iloc[i] if pd.notna(df['ilmok_yang'].iloc[i]) and df['ilmok_yang'].iloc[i] != '?' else None
        row['ilmok_dolpa'] = df['ilmok_dolpa'].iloc[i] if pd.notna(df['ilmok_dolpa'].iloc[i]) and df['ilmok_dolpa'].iloc[i] != '?' else None

    return ilbong

















































def get_ilbong(access_token, shcode, start_date = '19990101', end_date = time.strftime('%Y%m%d', time.localtime())):
    """
    일봉, 이평선, 수급, 공매도/프로그램 데이터를 가장 간결한 1회 요청 방식으로 통합하여 가져오는 함수입니다.
    (t8410의 500일 제한 기간 내에서만 데이터를 처리하며, t1716은 최대 250일치만 가져옵니다.)
    """
    
    # ----------------------------------------------------------------------
    # 0. 공통 설정 및 t8410 (일봉 데이터) 요청 및 MA 계산 (500일)
    # ----------------------------------------------------------------------
    
    url_base = "https://openapi.ls-sec.co.kr:8080/stock/chart"
    url_supply = "https://openapi.ls-sec.co.kr:8080/stock/frgr-itt"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "authorization": f"Bearer {access_token}"
    }

    # t8410 (일봉) 요청: 500일치 요청
    headers_ohlcv = {**headers, "tr_cd": "t8410", "tr_cont": "N", "tr_cont_key": ""}
    body_ohlcv = {
        "t8410InBlock": {
            "shcode": shcode, "gubun": "2", "qrycnt": 500,  
            "sdate": start_date, "edate": end_date, "cts_date": "", 
            "comp_yn": "N", "sujung": "Y"
        }
    }

    try:
        res_ohlcv = requests.post(url_base, headers=headers_ohlcv, json=body_ohlcv, verify=False) 
        rows = res_ohlcv.json().get("t8410OutBlock1", [])
    except Exception:
        rows = []
    
    if not rows:
        return []

    # 일봉 데이터프레임 (df) 생성 및 MA 계산
    temp_ilbong_data = []
    for row in rows:
        temp_ilbong_data.append({
            "date": row["date"], "open": float(row["open"]), "high": float(row["high"]), 
            "low": float(row["low"]), "close": float(row["close"]), "volume": int(row["jdiff_vol"])
        })
    
    df = pd.DataFrame(temp_ilbong_data)
    df['close'] = pd.to_numeric(df['close']) 
    df['date'] = df['date'].astype(str)
    df.set_index('date', inplace=True)

    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ma60'] = df['close'].rolling(window=60).mean()
    df['ma120'] = df['close'].rolling(window=120).mean()
    
    # ----------------------------------------------------------------------
    # 1. t1702 (수급 데이터: 개인, 외국인, 기관 등) 1회 요청 및 병합
    # ----------------------------------------------------------------------
    
    headers_t1702 = {**headers, "tr_cd": "t1702", "tr_cont": "N", "tr_cont_key": ""}
    # 매개변수 start_date와 end_date 직접 사용
    body_t1702 = {"t1702InBlock": {"shcode": shcode, "fromdt": start_date, "todt": end_date, "volvalgb": "1", "msmdgb": "0", "gubun": "0", "exchgubun": "U"}}
    
    investor_rows = []
    try:
        res_t1702 = requests.post(url_supply, headers=headers_t1702, json=body_t1702, verify=False)
        investor_rows = res_t1702.json().get("t1702OutBlock1", [])
    except Exception:
        pass

    if investor_rows:
        investor_data_list = []
        for row in investor_rows:
            핵심_기관_합계 = (
                float(row.get("tjj0001", 0)) + float(row.get("tjj0002", 0)) +
                float(row.get("tjj0003", 0)) + float(row.get("tjj0004", 0)) +
                float(row.get("tjj0005", 0)) 
            )
            
            investor_data_list.append({
                'date': row["date"], '개인': float(row.get("tjj0008", 0)), 
                '외국인': float(row.get("tjj0016", 0)), '기관': 핵심_기관_합계,                     
                '연기금': float(row.get("tjj0006", 0)), '사모펀드': float(row.get("tjj0000", 0)),
            })
            
        df_investor = pd.DataFrame(investor_data_list).drop_duplicates(subset=['date']).set_index('date')
        df = df.join(df_investor, how='left')
        
    # ----------------------------------------------------------------------
    # 2. t1716 (공매도 및 프로그램 매매 현황) 1회 요청 및 병합
    # ----------------------------------------------------------------------
    
    headers_t1716 = {**headers, "tr_cd": "t1716", "tr_cont": "N", "tr_cont_key": ""}
    # 매개변수 start_date와 end_date 직접 사용
    body_t1716 = {
        "t1716InBlock": {
            "shcode": shcode, "gubun": "0", "fromdt": start_date, "todt": end_date,
            "prapp": 0, "prgubun": "0", "orggubun": "0", "frggubun": "0"
        }
    }

    all_short_rows = []
    try:
        res_t1716 = requests.post(url_supply, headers=headers_t1716, json=body_t1716, verify=False)
        all_short_rows = res_t1716.json().get("t1716OutBlock", [])
    except Exception:
        pass

    if all_short_rows:
        extra_data_list = []
        for row in all_short_rows:
            extra_data_list.append({
                'date': row["date"],
                '공매도수량': float(row.get("gm_volume", 0)), 
                '공매도대금': float(row.get("gm_value", 0)),
                '프로그램': float(row.get("pgmvol", 0)), 
            })
        
        # DataFrame으로 변환 및 병합
        df_extra = pd.DataFrame(extra_data_list).drop_duplicates(subset=['date']).set_index('date')
        df = df.join(df_extra, how='left')

    # ----------------------------------------------------------------------
    # 3. 최종 결과 구조 (Dict List)로 변환 (모든 로직 인라인)
    # ----------------------------------------------------------------------
    
    ilbong = []
    
    for index, row in df.reset_index().iterrows():
        
        item = {
            'code': shcode, 'date': row['date'],
            'open': row['open'], 'high': row['high'], 'low': row['low'], 'close': row['close'],
            'volume': row.get('volume', 0), 
            
            # 이평선: pd.notna 체크 후 round 처리
            'ma5': round(row['ma5'], 2) if pd.notna(row.get('ma5')) else None,
            'ma20': round(row['ma20'], 2) if pd.notna(row.get('ma20')) else None,
            'ma60': round(row['ma60'], 2) if pd.notna(row.get('ma60')) else None,
            'ma120': round(row['ma120'], 2) if pd.notna(row.get('ma120')) else None,
            
            # 수급 데이터 (t1702) 초기값 설정
            '개인': None, '외국인': None, '기관': None, '연기금': None, '사모펀드': None,
            
            # 공매도 및 프로그램 매매 데이터 (t1716) 초기값 설정
            '프로그램': None, '공매도수량': None, '공매도대금': None
        }

        # 수급 데이터 (t1702) 처리: 컬럼 존재 및 값이 NaN이 아닐 때만 float으로 변환
        if '개인' in df.columns:
            if pd.notna(row['개인']): item['개인'] = float(row['개인'])
            if pd.notna(row['외국인']): item['외국인'] = float(row['외국인'])
            if pd.notna(row['기관']): item['기관'] = float(row['기관'])
            if pd.notna(row['연기금']): item['연기금'] = float(row['연기금'])
            if pd.notna(row['사모펀드']): item['사모펀드'] = float(row['사모펀드'])
        
        # 공매도 및 프로그램 매매 데이터 (t1716) 처리: 컬럼 존재 및 값이 NaN이 아닐 때만 float으로 변환
        if '프로그램' in df.columns:
            if pd.notna(row['프로그램']): item['프로그램'] = float(row['프로그램'])
            if pd.notna(row['공매도수량']): item['공매도수량'] = float(row['공매도수량'])
            if pd.notna(row['공매도대금']): item['공매도대금'] = float(row['공매도대금'])
            
        ilbong.append(item)


    ilbong = get_ilbong_rsi(ilbong)
    # create_tb_ilbong()
    insert_tb_ilbong(shcode, ilbong)

    return ilbong












if __name__ == "__main__":
    access_token = get_token()



    list_kospi = select_tb_kospi()
    print('일봉 수집 시작!   ' + time.strftime('[%H:%m]', time.localtime()))

    for i, item in enumerate(list_kospi):
        
        print(str(i+1) + ' ' + str(item[0]) + ' ' + str(item[1]))
        get_ilbong(access_token, str(item[0]))


    print('일봉 수집 종료   ' + time.strftime('[%H:%m]', time.localtime()))











    
