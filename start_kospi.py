import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime


from db import *
# from RSI_app.kiwoom.util.db import *


import sys
import os
# 프로젝트 루트 경로를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
# from RSI_app.kiwoom.util.db import *  # 상대경로 기준으로 import


BASE_URL = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok='
CODES = [0, 1]  # KOSPI:0, KOSDAQ:1
fields = []
now = datetime.now()
formattedDate = now.strftime("%Y%m%d")







def get_recent_day():
    url = f"https://finance.naver.com/item/sise_day.nhn?code=005930&page=1"
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(html.text, "html.parser")
    return soup.find_all('td')[1].text.replace('.', '')



def get_ilbong_1day(code):
    url = f"https://finance.naver.com/item/sise_day.nhn?code=" + code + "&page=1"
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(html.text, "html.parser")

    list_recent = []
    list_recent.append(soup.find_all('td')[1].text.replace('.', ''))
    list_recent.append(int(soup.find_all('td')[4].text.replace(',', '')))
    list_recent.append(int(soup.find_all('td')[5].text.replace(',', '')))
    list_recent.append(int(soup.find_all('td')[6].text.replace(',', '')))
    list_recent.append(int(soup.find_all('td')[2].text.replace(',', '')))
    list_recent.append(int(soup.find_all('td')[7].text.replace(',', '')))
    df_recent = pd.DataFrame([list_recent[1:]], columns=['open','high','low','close','volume'], index=[list_recent[0]])

    return df_recent




def execute_crawler():

    df_total = []   # df_kospi + df_kosdaq
    df_kospi = []
    df_kosdaq = []

    for code in CODES:   # KOSPI:0, KOSDAQ:1

        html = requests.get(BASE_URL + str(CODES[0]))
        soup = BeautifulSoup(html.text, 'lxml')
        
        # '맨뒤'에 해당하는 태그를 기준으로 전체 페이지 개수 추출하기
        total_page_num = soup.select_one('td.pgRR > a')   # find('td', class_='pgRR').find('a') <td class=pgRR       class는. id는#        
        total_page_num = int(total_page_num.get('href').split('=')[-1])   # 47

        # 조회할 수 있는 항목정보들 추출
        ipt_html = soup.select_one('div.subcnt_sise_item_top')


        # 전역변수 fields에 항목들을 담아 다른 함수에서도 접근가능하도록 만듬
        global fields
        fields = [item.get('value') for item in ipt_html.select('input')]   # 제목들


        if code == 0:   # 코스피 200 종목
            result = [crawler(code, str(page)) for page in range(1, 5)]    # total_page_num + 1)] ###############
        if code == 1:   # 코스닥 100 종목
            result = [crawler(code, str(page)) for page in range(1, 3)]    # total_page_num + 1)] ###############

        # 전체 페이지를 저장한 result를 하나의 데이터프레임으로 만듬
        df = pd.concat(result, axis=0, ignore_index=True)

        # 변수 df는 KOSPI, KOSDAQ별로 크롤링한 종목 정보이고 이를 하나로 합치기 위해 df_total에 추가
        df_total.append(df)



  
    df_total = pd.concat(df_total)     # df_total를 하나의 데이터프레임으로 만듬
    df_total.reset_index(inplace=True, drop=True)   # 합친 데이터프레임의 index 번호를 새로 매김
    df_total.index = df_total.index + 1

    

    return df_total


def crawler(code, page):

    global fields


    # Naver finance에 전달할 값들 세팅(요청을 보낼 때는 menu, fieldIds, returnUrl을 지정해서 보내야 함)
    data = {'menu': 'market_sum',
            'fieldIds': fields,
            'returnUrl': BASE_URL + str(code) + "&page=" + str(page)}



    html = requests.post('https://finance.naver.com/sise/field_submit.nhn', data=data)
    # html = requests.get(BASE_URL + str(code) + "&page=" + str(page))
    soup = BeautifulSoup(html.text, 'lxml')

    table_html = soup.select_one('div.box_type_l')


    header_data = [item.get_text().strip() for item in table_html.select('thead th')][1:-1]   # 종목명, 현재가, 전일비

    codes = [item.get('href').split('=')[-1] for item in table_html.select('a.tltle')]



    # 종목명 + 수치 추출 (a.title = 종목명, td.number = 기타 수치)
    inner_data = [item.get_text().strip() for item in table_html.find_all(lambda x:
                                                                          (x.name == 'a' and
                                                                           'tltle' in x.get('class', [])) or
                                                                          (x.name == 'td' and
                                                                           'number' in x.get('class', []))
                                                                          )]   # <a class="tltle"     <td class="number">57,900</td>





    # page마다 있는 종목의 순번 가져오기
    no_data = [item.get_text().strip() for item in table_html.select('td.no')]
    number_data = np.array(inner_data)



    # 가로 x 세로 크기에 맞게 행렬화
    number_data.resize(len(no_data), len(header_data))

    # 한 페이지에서 얻은 정보를 모아 DataFrame로 만들어 반환
    df = pd.DataFrame(data=number_data, columns=header_data)


    # 종목코드를 DataFrame에 추가
    df['종목코드'] = codes
    df['시장'] = '코스피' if code == 0 else '코스닥'
    cols = ['종목코드'] + [col for col in df.columns if col not in ['종목코드', '시장']] + ['시장']

    df = df[cols]

    return df


def set_kospi():

    print('set_kospi 시작')

    df = execute_crawler()

    
    mapping = {',': '', 'N/A': '0'}
    df.replace(mapping, regex=True, inplace=True)

    # 필요한 컬럼만 선택
    selected_columns = ['종목코드', '종목명', '현재가', '등락률', '시가총액', '매출액', '영업이익', '당기순이익', '주당순이익', '보통주배당금', '외국인비율', 'PER', 'ROE', '시장']
    df_selected = df[selected_columns].rename(columns={'종목코드': '코드', '매출액': '매출', '보통주배당금': '배당금', '외국인비율': '외국인'})
    df_selected['순위'] = df_selected.groupby('시장').cumcount() + 1


    create_tb_kospi(df_selected)   # 전체 종목
    df_selected.to_excel("Kospi.xlsx")

    

    print('set_kospi 완료')
 

    return df_selected['종목명'].tolist()






def set_kospi_1day():

    
    df = execute_crawler()    # 크롤링 결과를 얻어옴

    mapping = {',': '', 'N/A': '0'}
    df.replace(mapping, regex=True, inplace=True)

    # 필요한 컬럼만 선택
    selected_columns = ['종목코드', '시가', '고가', '저가', '현재가', '거래량']
    df_selected = df[selected_columns].rename(columns={'종목코드': 'code', '시가': 'open', '고가': 'high', '저가': 'low', '현재가': 'close', '거래량': 'volume'})

    return df_selected



if __name__ == "__main__":
    print('Start!')
    kospi = set_kospi()
    # print(kospi)
    print('End')
    
