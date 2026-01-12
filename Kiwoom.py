
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
from datetime import datetime
import pandas as pd
import numpy as np
from urllib3.connection import RECENT_DATE

from RSI_app.kiwoom.util.const import *
from RSI_app.kiwoom.util.db import *
import json


# from util.const import *
# from db import *



class Kiwoom(QAxWidget):   # QAxWidget: Open API 연결
    def __init__(self):
        super().__init__()
        self._make_kiwoom_instance()
        self._set_signal_slots()
        self._comm_connect()
        self.tr_event_loop = QEventLoop()

        self.order = {}
        self.balance = {}
        self.universe_realtime_transaction_info = {}

        self.request_queue = []
        self.response_dict = {}
        self.tr_data = None


        # --- 실시간 캐시 초기화 ---
        self.real_cache = {
            "items": {},    # 종목별
            "total": {      # 총합
                "총매입금액": "a",
                "총평가금액": "a",
                "총평가손익": "a",
                "총수익률": "a",        
                "예수금": "a",
                "대주금액": "a",
                "추정자산": "a"
            },
            "order": {},    # 주문 체결/상태
        }


        self.real_hoga_cache = {} 

        








    def _make_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")   # QAxContainer.QAxWidget의 setControl

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._login_slot)   # 로그인 결과를 받는 슬롯
        self.OnReceiveTrData.connect(self._on_tr_slot)
        self.OnReceiveMsg.connect(self._on_msg_slot)
        self.OnReceiveChejanData.connect(self._on_chejan_slot)
        self.OnReceiveRealData.connect(self._on_real_slot)

    def _comm_connect(self):
        self.dynamicCall("CommConnect()")   # 로그인 팝업
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()   # 로그인 입력 후 응답 대기




    def process_requests(self):   # zmq TR
        while self.request_queue:
            msg = self.request_queue.pop(0)
            print("[TR] Process_requests 가 main.py zmq소캣으로부터 받은 request msg: ", msg)

            if msg == "get_account_list":
                self.response_dict[msg] = self.get_account_list()  # ['8112023511']
                print("[TR] Process_requests 가 main.py zmq소캣으로 보내는 response_dict[msg] ( => zmq => 뷰) get_account_list : ", self.response_dict[msg])




            elif msg == "get_balance":
                # 잔고 dict 가져오기, None이면 기본 구조로 초기화
                balance = self.get_balance() or {
                    "balance": {},
                    "summary": {
                        "총매입금액": 0,
                        "총평가금액": 0,
                        "총평가손익금액": 0,
                        "총수익률": 0,
                        "총대주금액": 0,
                        "추정자산": 0
                    }
                }
                deposit = self.get_deposit() or 0
                balance["deposit"] = deposit
                print("[TR] Process_requests 가 main.py zmq소캣으로 보내는 response_dict[msg] ( => zmq => 뷰) get_deposit : ", balance)

                self.response_dict[msg] = [balance]


            elif msg.startswith("set_account:"):
                self.account_number = msg.split(":", 1)[1]
                self.response_dict[msg] = self.account_number
                print("[TR] Process_requests 가 main.py zmq소캣으로 보내는 response_dict[msg] ( => zmq => 뷰) set_account : ", self.account_number)

                self.response_dict[msg] = [self.account_number]




            elif msg.startswith("get_hoga:"):
                # msg에서 필요한 거 TR 호출
                print(msg)
                print(msg.split(":", 1)[1])
                hoga = self.get_hoga(msg.split(":", 1)[1]) or {
                    "매도호가": [],
                    "매도잔량": [],
                    "매수호가": [],
                    "매수잔량": [],
                    "현재가": None
                }

                print("[TR] Process_requests 가 main.py zmq소캣으로 보내는 response_dict[msg] ( => zmq => 뷰) get_hoga : ", hoga)

                self.response_dict[msg] = [hoga]
    














    def _login_slot(self, err_code):

        print("connected")
        self.account_number = self.get_account_list()[2]
            
        print(">>> LOGIN SLOT CALLED")
        print(self.account_number)


        # 1) 잔고/예수금 실시간 (9001:수익률, 9201:잔고수량, 900:평가금액)
        self.set_real_reg("1000", self.account_number, "9001;9201;900", "0")

        # 2) 종목별 체결/호가 실시간 (10:체결가, 11:체결량)
        self.set_real_reg("1001", "005930", "10;11", "1")

        # 3) 주문/체결(체잔) 필수 실시간 3종 (9001/9201/9203)
        self.set_real_reg("9000", self.account_number, "9001;9201;9203", "0")

        # 잔고
        self.set_real_reg("6000", self.account_number, "930;931;10;302;932;933;8019", "0")


        self.login_event_loop.exit()




    def get_comm_real_data(self, code, fid):
        return self.dynamicCall("GetCommRealData(QString, int)", code, fid)




    def _on_tr_slot(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):

        tr_data_cnt = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        print("TR 슬롯 : [" + trcode + "] " + next + " " + record_name + " " + str(tr_data_cnt) + "건")
        
        if next=='2':
            self.has_next_tr_data = True
        else:
            self.has_next_tr_data = False


        if rqname == "opt10081_req": # 일봉 600건
            ohlcv = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[], 'volume':[]}

            # for i in range(tr_data_cnt):
            for i in range(300):
                date = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "일자")
                open = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "시가")
                high = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "고가")
                low = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "저가")
                close = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "현재가")
                volume = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "거래량")


                try:
                    ohlcv['date'].append(date.strip())
                    ohlcv['open'].append((int(open)))
                    ohlcv['high'].append((int(high)))
                    ohlcv['low'].append((int(low)))
                    ohlcv['close'].append((int(close)))
                    ohlcv['volume'].append((int(volume)))

                except ValueError:
                    if ohlcv['date']:
                        ohlcv['date'].pop()                    
                    print(f"[경고] {i}번째 데이터 변환 실패 (상장 초기 데이터일 가능성 있음)")
                    break
                

            self.tr_data = ohlcv




        elif rqname == "opt10081_req_1day":
            ohlcv = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[], 'volume':[]}

            date = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "일자")
            open = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "시가")
            high = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "고가")
            low = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "저가")
            close = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "현재가")
            volume = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "거래량")

            ohlcv['date'].append(date.strip())
            ohlcv['open'].append((int(open)))
            ohlcv['high'].append((int(high)))
            ohlcv['low'].append((int(low)))
            ohlcv['close'].append((int(close)))
            ohlcv['volume'].append((int(volume)))

            self.tr_data = ohlcv

        elif rqname == "opw00001_req":
            deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "주문가능금액")
            self.tr_data = int(deposit)
            self.real_cache["total"]["예수금"] = int(deposit)
            

        elif rqname=="opt10075_req":

            if not hasattr(self, 'tr_data'):  # 첫 페이지이면 초기화
                self.tr_data = {}
        
            for i in range(tr_data_cnt):
                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "종목코드")
                code_name = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "종목명")
                order_number = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "주문번호")
                order_status = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "주문상태")
                order_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "주문수량")
                order_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "주문가격")
                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "현재가")
                order_type = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "주문구분")
                left_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "미체결수량")
                executed_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "체결량")
                ordered_at = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "시간")
                fee = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "수수료")
                
                tax = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "세금")

                code = code.strip()
                code_name = code_name.strip()
                order_number = str(int(order_number.strip()))
                order_status = order_status.strip()
                order_quantity = int(order_quantity.strip())
                order_price = int(order_price.strip())
                current_price = int(current_price.strip().lstrip('+').lstrip('-'))
                order_type = order_type.strip().lstrip('+').lstrip('-')
                left_quantity = int(left_quantity.strip())
                executed_quantity = int(executed_quantity.strip())
                ordered_at = ordered_at.strip()
                fee = int(fee) if fee else 0
                tax = int(tax) if tax else 0

                self.order[order_number] = {
                    '주문번호': order_number,
                    '종목코드': code,
                    '종목명': code_name,
                    '주문수량': order_quantity,
                    '주문가격': order_price,
                    '현재가': current_price,
                    '주문구분': order_type,
                    '미체결수량': left_quantity,
                    '체결량': executed_quantity,
                    '주문시간': ordered_at,
                    '당일매매수수료': fee,
                    '당일매매세금': tax,
                }

            self.tr_data.update(self.order)

        elif rqname == "opw00018_req":

            if tr_data_cnt == 0:
                print('[TR] opw00018 잔고 계좌 없음')
                self.balance = {}
                self.balance_summary = {
                    '총매입금액': 0,
                    '총평가금액': 0,
                    '총평가손익금액': 0,
                    '총수익률': 0.0,
                    '추정자산': 0,
                    '총대주금액': 0
                }

                # --- TR에서 받은 데이터로 real_cache 갱신 ---
                self.real_cache["total"]["총매입금액"] = 0
                self.real_cache["total"]["총평가금액"] = 0
                self.real_cache["total"]["총평가손익"] = 0
                self.real_cache["total"]["총수익률"] = 0
                self.real_cache["total"]["대주금액"] = 0
                self.real_cache["total"]["추정자산"] = 0

                self.real_cache["items"] = {}
















                

                
            else:


                
                for i in range(tr_data_cnt):
                    code = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "종목번호")
                    code_name = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "종목명")
                    quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "보유수량")
                    purchase_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "매입가")
                    return_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "수익률(%)")
                    current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "현재가")
                    total_purchase_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "매입금액")
                    total_valuation_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "평가금액")
                    valuation_profit = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "평가손익")                                
                    # available_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, i, "매매가능수량")

                    code = code.strip()[1:]
                    code_name = code_name.strip()
                    quantity = int(quantity)
                    purchase_price = int(purchase_price)
                    return_rate = float(return_rate)
                    current_price = int(current_price)
                    total_purchase_price = int(total_purchase_price)
                    total_valuation_price = int(total_valuation_price)
                    valuation_profit = int(valuation_profit)                
                    # available_quantity = int(available_quantity)


                    self.balance[code] = {
                        '종목명': str(code_name),
                        '보유수량': int(quantity),
                        '매입가': int(purchase_price),
                        '수익률': float(return_rate),
                        '현재가': int(current_price),
                        '매입금액': int(total_purchase_price),
                        '평가금액': int(total_valuation_price),
                        '평가손익': int(valuation_profit),                    
                        # '매매가능수량': int(available_quantity),
                    }




                self.balance_summary = {
                    '총매입금액': int(self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "총매입금액").strip()),
                    '총평가금액': int(self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "총평가금액").strip()),
                    '총평가손익금액': int(self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "총평가손익금액").strip()),
                    '총수익률': float(self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "총수익률(%)").strip()),
                    '추정자산': int(self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "추정예탁자산").strip()),                
                    '총대주금액': int(self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "총대주금액").strip())
                }


                # --- TR에서 받은 데이터로 real_cache 갱신 ---
                self.real_cache["total"]["총매입금액"] = self.balance_summary['총매입금액']
                self.real_cache["total"]["총평가금액"] = self.balance_summary['총평가금액']
                self.real_cache["total"]["총평가손익"] = self.balance_summary['총평가손익금액']
                self.real_cache["total"]["총수익률"] = self.balance_summary['총수익률']
                self.real_cache["total"]["대주금액"] = self.balance_summary['총대주금액']
                self.real_cache["total"]["추정자산"] = self.balance_summary['추정자산']

                # 종목별도 원하면
                for code, info in self.balance.items():
                    self.real_cache["items"][code] = {
                        "종목명": info["종목명"],
                        "보유수량": info["보유수량"],
                        "매입가": info["매입가"],
                        "수익률": info["수익률"],
                        "현재가": info["현재가"],
                        "매입금액": info["매입금액"],
                        "평가금액": info["평가금액"],
                        "평가손익": info["평가손익"],
                    }




            self.tr_data = {
                'balance': self.balance,
                'summary': self.balance_summary
            }






        
            # self.tr_data = self.balance



        elif rqname == "opt10004_req":   # "주식호가조회":
            hoga = {
                "매도호가": [],
                "매도잔량": [],
                "매수호가": [],
                "매수잔량": [],
                "현재가": None
            }

            # 현재가
            cur = self.dynamicCall(
                "GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "현재가"
            ).strip()
            hoga["현재가"] = int(cur) if cur else 0

            # ★ 10단계가 아니라 20단계 있음 (키움은 20호가)
            for i in range(1, 21):
                ask_price = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", trcode, rqname, 0, f"매도{i}호가"
                ).strip()
                ask_vol = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", trcode, rqname, 0, f"매도{i}잔량"
                ).strip()

                bid_price = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", trcode, rqname, 0, f"매수{i}호가"
                ).strip()
                bid_vol = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", trcode, rqname, 0, f"매수{i}잔량"
                ).strip()

                hoga["매도호가"].append(int(ask_price) if ask_price else 0)
                hoga["매도잔량"].append(int(ask_vol) if ask_vol else 0)
                hoga["매수호가"].append(int(bid_price) if bid_price else 0)
                hoga["매수잔량"].append(int(bid_vol) if bid_vol else 0)

            print(hoga)
            print(8888888888888888888)

            self.tr_data = hoga

        





        if rqname == "opt10059_req":
            investor_data = {'date': [], '개인': [], '외국인': [], '기관': [], '연기금': []}
            for i in range(tr_data_cnt):  # 최대 10개의 데이터를 가져오는 예시
                date = self.CommGetData(trcode, "", rqname, i, "일자")
                개인 = self.CommGetData(trcode, "", rqname, i, "개인투자자")
                외국인 = self.CommGetData(trcode, "", rqname, i, "외국인투자자")
                기관 = self.CommGetData(trcode, "", rqname, i, "기관계")
                연기금 = self.CommGetData(trcode, "", rqname, i, "연기금등")

                investor_data['date'].append(date)
                investor_data['개인'].append(개인)
                investor_data['외국인'].append(외국인)
                investor_data['기관'].append(기관)
                investor_data['연기금'].append(연기금)

            self.tr_data = investor_data
            time.sleep(0.3)






        self.tr_event_loop.exit()
        time.sleep(0.5)




    def _on_msg_slot(self, screen_no, rqname, trcode, msg):
        print(f"MSG 슬롯 : [{trcode}] {msg} (screen_no: {screen_no}, rqname: {rqname})")



    def _on_chejan_slot(self, s_gubun, n_item_cnt, s_fid_list):
        print("체잔 슬롯 : [" + s_gubun + "] " + str(n_item_cnt) + " " + str(s_fid_list))

        for fid in s_fid_list.split(";"):
            if fid in FID_CODES:
                code = self.dynamicCall("GetChejanData(int)", '9001')[1:]   # 종목코드
                data = self.dynamicCall("GetChejanData(int)", fid)          # 9201계좌번호 9203주문번호

                data = data.strip().lstrip('+').lstrip('-')   # 매수가 등의 +, - 삭제
                if data.isdigit():
                    data = int(data)
                item_name = FID_CODES[fid]         # fid=9201 => 계좌번호
                # print(item_name + ": " + data)   # 주문가격: 37,6000
                print("{}: {}".format(item_name, data))

                if int(s_gubun) == 0:   # 0체결 self.order, 1잔고 self.balance
                    if code not in self.order.keys():   # order에 종목이 없으면 신규 생성
                        self.order[code] = {}           # self.order['007700']   {'007700': {}}
                    self.order[code].update({item_name: data})   # {'주문상태':'접수'} => {'007700': {'주문상태':'접수'}}   {'007700': {'주문상태':'체결'}}
                elif int(s_gubun) == 1:
                    if code not in self.balance.keys(): # balance에 종목이 없으면 신규 생성
                        self.balance[code] = {}
                    self.balance[code].update({item_name: data})

        if int(s_gubun)==0:
            print("[체잔] * 주문출력(self.order)")
            print(self.order)
        elif int(s_gubun)==1:
            print("[체잔] * 잔고출력(self.balance)")
            print(self.balance)








        # ------------------------------
        # 체결/잔고 로그 저장 추가 부분
        # ------------------------------
        try:
            # 어떤 체잔인지
            gubun_name = "체결" if int(s_gubun) == 0 else "잔고"

            # 기본 정보 획득
            code = self.dynamicCall("GetChejanData(int)", 9001)[1:]  # 종목코드(A 제거)
            name = self.dynamicCall("GetChejanData(int)", 302).strip()  # 종목명

            with open("order_log.txt", "a", encoding="utf-8") as log:
                log.write(f"\n[{gubun_name}] 종목:{code} {name}\n")

                for fid in s_fid_list.split(";"):
                    if fid in FID_CODES:
                        item_name = FID_CODES[fid]
                        data = self.dynamicCall("GetChejanData(int)", fid)
                        value = data.strip().lstrip("+").lstrip("-")
                        log.write(f"{item_name}: {value}\n")

                log.write("--------------------------------------\n")
        except Exception as e:
            print("로그 저장 오류:", e)









                



    def _on_real_slot(self, s_code, real_type, real_data):
        try:
            print(f"[REAL] {s_code} / {real_type}")

            # =====================================================
            # 1) 잔고 관련 REAL (900, 9001, 9201)
            # =====================================================
            if real_type in ("900", "9001", "9201"):
                total = self.real_cache.setdefault("total", {})
                items = self.real_cache.setdefault("items", {})
                item  = items.setdefault(s_code, {})

                # --- FID 900: 금액 계열 ---
                if real_type == "900":
                    total["총매입금액"] = int(real_data.get("총매입금액", total.get("총매입금액", 0)))
                    total["총평가금액"] = int(real_data.get("총평가금액", total.get("총평가금액", 0)))
                    total["총평가손익"] = int(real_data.get("총평가손익", total.get("총평가손익", 0)))
                    total["추정자산"]  = int(real_data.get("추정자산",  total.get("추정자산", 0)))

                    item["매입금액"]  = int(real_data.get("매입금액",  item.get("매입금액", 0)))
                    item["평가금액"]  = int(real_data.get("평가금액",  item.get("평가금액", 0)))
                    item["평가손익"]  = int(real_data.get("평가손익",  item.get("평가손익", 0)))

                # --- FID 9001: 수익률 ---
                elif real_type == "9001":
                    total["총수익률"] = float(real_data.get("총수익률", total.get("총수익률", 0)))
                    item["수익률"]   = float(real_data.get("수익률", item.get("수익률", 0)))

                # --- FID 9201: 잔고수량 / 예수금 ---
                elif real_type == "9201":
                    total["예수금"]   = int(real_data.get("예수금",   total.get("예수금", 0)))
                    total["대주금액"] = int(real_data.get("대주금액", total.get("대주금액", 0)))
                    item["잔고수량"]  = int(real_data.get("잔고수량", item.get("잔고수량", 0)))

                print("[REAL] 잔고 캐시 업데이트:", self.real_cache)


            # =====================================================
            # 2) 주식 호가잔량 (20단계, FID 41~80 / 51~90)
            # =====================================================
            if real_type == "주식호가잔량":

                hoga = {
                    "매도호가": [],
                    "매도잔량": [],
                    "매수호가": [],
                    "매수잔량": [],
                }

                # 20단계: index 0~19
                for i in range(20):
                    # ---- FID 계산 ----
                    # 매도호가: 41,43,45,... (41 + i*2)
                    # 매도잔량: 61,63,65,... (61 + i*2)
                    # 매수호가: 51,53,55,... (51 + i*2)
                    # 매수잔량: 81,83,85,... (81 + i*2)

                    try:
                        ask_price = int(self.dynamicCall("GetCommRealData(QString, int)", s_code, 41 + i*2))
                    except:
                        ask_price = 0
                    try:
                        ask_vol = int(self.dynamicCall("GetCommRealData(QString, int)", s_code, 61 + i*2))
                    except:
                        ask_vol = 0
                    try:
                        bid_price = int(self.dynamicCall("GetCommRealData(QString, int)", s_code, 51 + i*2))
                    except:
                        bid_price = 0
                    try:
                        bid_vol = int(self.dynamicCall("GetCommRealData(QString, int)", s_code, 81 + i*2))
                    except:
                        bid_vol = 0

                    # 음수 제거 (키움은 음수로 내려오기도 함)
                    ask_price = abs(ask_price)
                    bid_price = abs(bid_price)

                    hoga["매도호가"].append(ask_price)
                    hoga["매도잔량"].append(ask_vol)
                    hoga["매수호가"].append(bid_price)
                    hoga["매수잔량"].append(bid_vol)

                # 캐시에 저장
                self.real_hoga_cache[s_code] = hoga
                print("[REAL] 호가 캐시 업데이트:", hoga)

        except Exception as e:
            print("[REAL ERROR]", e)














    def set_price(self, code):

        # 일봉
        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10081_req", "opt10081", 0, "0001")
        self.tr_event_loop.exec_()


        '''
        self.has_next_tr_data = True
        while self.has_next_tr_data == True:
            self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
            self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
            self.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10081_req", "opt10081", 2, "0001")
            self.tr_event_loop.exec_()
        '''
        

        ohlcv = self.tr_data
        df_ohlcv = pd.DataFrame(ohlcv, columns=['open', 'high', 'low', 'close', 'volume'], index=ohlcv['date'])



        # print(df_ohlcv)



        # df_ohlcv = df_ohlcv[:300]

        # 5일 이동평균선
        df_ohlcv['a5'] = 0
        for i in range(0, len(df_ohlcv['a5'])-5+1):
            df_ohlcv.loc[df_ohlcv.index[i], 'a5'] = df_ohlcv['close'][i:5+i].mean()

        # 20일 이동평균선
        df_ohlcv['a20'] = 0
        for i in range(0, len(df_ohlcv['a20'])-20+1):
            df_ohlcv.loc[df_ohlcv.index[i], 'a20'] = df_ohlcv['close'][i:20+i].mean()

        # 60일 이동평균선
        df_ohlcv['a60'] = 0
        for i in range(0, len(df_ohlcv['a60'])-60+1):
            df_ohlcv.loc[df_ohlcv.index[i], 'a60'] = df_ohlcv['close'][i:60+i].mean()

        # 120일 이동평균선
        df_ohlcv['a120'] = 0
        for i in range(0, len(df_ohlcv['a120'])-120+1):
            df_ohlcv.loc[df_ohlcv.index[i], 'a120'] = df_ohlcv['close'][i:120+i].mean()


        # print(df_ohlcv)


        # RSI
        delta = df_ohlcv['close'] - df_ohlcv['close'].shift(-1)

        df_ohlcv['u'] = delta.apply(lambda x: x if x > 0 else 0)
        df_ohlcv['d'] = delta.apply(lambda x: x*(-1) if x < 0 else 0)

        df_ohlcv['au'] = pd.Series([0] * len(df_ohlcv), index=df_ohlcv.index)
        df_ohlcv['ad'] = pd.Series([0] * len(df_ohlcv), index=df_ohlcv.index)

        N = 14

        df_ohlcv.loc[df_ohlcv.index[len(df_ohlcv['au']) - N - 1], 'au'] = df_ohlcv['u'][len(df_ohlcv['u']) - N: len(df_ohlcv['u'])].mean()
        df_ohlcv.loc[df_ohlcv.index[len(df_ohlcv['ad']) - N - 1], 'ad'] = df_ohlcv['d'][len(df_ohlcv['d']) - N: len(df_ohlcv['d'])].mean()

        for i in range(2, len(df_ohlcv['au']) - N + 1):
            current_index = df_ohlcv.index[len(df_ohlcv['au']) - N - i]
            next_index = df_ohlcv.index[len(df_ohlcv['au']) - N - i + 1]
            df_ohlcv.loc[current_index, 'au'] = ((df_ohlcv.loc[next_index, 'au'] * (N - 1)) + df_ohlcv['u'].iloc[len(df_ohlcv['au']) - N - i]) / N

        for i in range(2, len(df_ohlcv['ad']) - N + 1):
            current_index = df_ohlcv.index[len(df_ohlcv['ad']) - N - i]
            next_index = df_ohlcv.index[len(df_ohlcv['ad']) - N - i + 1]
            df_ohlcv.loc[current_index, 'ad'] = ((df_ohlcv.loc[next_index, 'ad'] * (N - 1)) + df_ohlcv['d'].iloc[len(df_ohlcv['ad']) - N - i]) / N

        df_ohlcv['rsi'] = (df_ohlcv['au'] * 100) / (df_ohlcv['au'] + df_ohlcv['ad'])

        df_ohlcv['rsi9'] = 0
        for i in range(0, len(df_ohlcv['rsi9'])-9+1):
            df_ohlcv.loc[df_ohlcv.index[i], 'rsi9'] = df_ohlcv['rsi'][i:9+i].mean()


        # MACD (EMA12-EMA26)
        df_ohlcv['ema12'] = pd.Series([0] * len(df_ohlcv), index=df_ohlcv.index)
        N = 12
        df_ohlcv.loc[df_ohlcv.index[len(df_ohlcv)-N], 'ema12'] = df_ohlcv['close'].iloc[len(df_ohlcv['close']) - N: len(df_ohlcv['close'])].mean()
        for i in range(1, len(df_ohlcv['ema12'])-N+1):
            df_ohlcv.loc[df_ohlcv.index[len(df_ohlcv)-N-i], 'ema12'] = (df_ohlcv['close'].iloc[len(df_ohlcv['ema12'])-N-i] * (2/(N+1))) + (df_ohlcv['ema12'].iloc[len(df_ohlcv['ema12'])-N-i+1] * (1-(2/(N+1))))

        df_ohlcv['ema26'] = pd.Series([0] * len(df_ohlcv), index=df_ohlcv.index)
        N = 26
        df_ohlcv.loc[df_ohlcv.index[len(df_ohlcv)-N], 'ema26'] = df_ohlcv['close'].iloc[len(df_ohlcv['close']) - N: len(df_ohlcv['close'])].mean()
        for i in range(1, len(df_ohlcv['ema26'])-N+1):
            df_ohlcv.loc[df_ohlcv.index[len(df_ohlcv)-N-i], 'ema26'] = (df_ohlcv['close'].iloc[len(df_ohlcv['ema26'])-N-i] * (2/(N+1))) + (df_ohlcv['ema26'].iloc[len(df_ohlcv['ema26'])-N-i+1] * (1-(2/(N+1))))

        df_ohlcv['macd'] = df_ohlcv['ema12'] - df_ohlcv['ema26']


        # MACD9
        df_ohlcv['macd9'] = pd.Series([0] * len(df_ohlcv), index=df_ohlcv.index)
        N = 9
        df_ohlcv.loc[df_ohlcv.index[len(df_ohlcv)-N], 'macd9'] = df_ohlcv['macd'].iloc[len(df_ohlcv['macd']) - N: len(df_ohlcv['macd'])].mean()
        for i in range(1, len(df_ohlcv['macd9'])-N+1):
            df_ohlcv.loc[df_ohlcv.index[len(df_ohlcv)-N-i], 'macd9'] = (df_ohlcv['macd'].iloc[len(df_ohlcv['macd9'])-N-i] * (2/(N+1))) + (df_ohlcv['macd9'].iloc[len(df_ohlcv['macd'])-N-i+1] * (1-(2/(N+1))))
        

        # 볼린저밴드
        stddev_20 = df_ohlcv['close'][::-1].rolling(window=20).std()
        df_ohlcv['bol_u'] = df_ohlcv['a20'] + stddev_20*2
        df_ohlcv['bol_l'] = df_ohlcv['a20'] - stddev_20*2
        bol_mean = (df_ohlcv['bol_u']-df_ohlcv['bol_l']).mean()
        df_ohlcv['bol_size'] = (df_ohlcv['bol_u'] - df_ohlcv['bol_l']).apply(lambda x: 'Big' if x > bol_mean*(1.5) else 'Small')
        df_ohlcv['bol_dolpa'] = [
            '상향돌파' if close > bol_u else ('하향돌파' if close < bol_l else '보통')
            for close, bol_u, bol_l in zip(df_ohlcv['close'], df_ohlcv['bol_u'], df_ohlcv['bol_l'])
        ]

        # 일목균형표
        high_26 = df_ohlcv['high'][::-1].rolling(window=26).max()[::-1]
        low_26 = df_ohlcv['low'][::-1].rolling(window=26).min()[::-1]
        kijun = (high_26 + low_26) / 2

        high_9 = df_ohlcv['high'][::-1].rolling(window=9).max()[::-1]
        low_9 = df_ohlcv['low'][::-1].rolling(window=9).min()[::-1]
        tenkan = (high_9 + low_9) / 2

        df_ohlcv['ilmok_a'] = ((kijun+tenkan) / 2).shift(-26+1)


        high_52 = df_ohlcv['high'][::-1].rolling(window=52).max()[::-1]
        low_52 = df_ohlcv['low'][::-1].rolling(window=52).min()[::-1]
        df_ohlcv['ilmok_b'] = ((high_52 + low_52) / 2).shift(-26+1)

        df_ohlcv['ilmok_dolpa'] = "?"
        df_ohlcv['ilmok_dolpa'] = np.where(
            (df_ohlcv['high'] > df_ohlcv['ilmok_a']) & (df_ohlcv['high'] > df_ohlcv['ilmok_b']),
            "상향돌파",
            np.where(
                (df_ohlcv['low'] < df_ohlcv['ilmok_a']) & (df_ohlcv['low'] < df_ohlcv['ilmok_b']),
                "하향돌파",
                np.where(
                    ((df_ohlcv['low'] > df_ohlcv['ilmok_a']) & (df_ohlcv['low'] < df_ohlcv['ilmok_b'])) | ((df_ohlcv['low'] < df_ohlcv['ilmok_a']) & (df_ohlcv['low'] > df_ohlcv['ilmok_b'])) | ((df_ohlcv['high'] > df_ohlcv['ilmok_a']) & (df_ohlcv['high'] < df_ohlcv['ilmok_b'])) | ((df_ohlcv['high'] < df_ohlcv['ilmok_a']) & (df_ohlcv['high'] > df_ohlcv['ilmok_b'])),
                    "구름내부",
                    "?"
                )
            )
        )

        df_ohlcv['ilmok_yang'] = [
            '양운' if a > b else '음운'
            for a, b in zip(df_ohlcv['ilmok_a'], df_ohlcv['ilmok_b'])
        ]

        # 개인, 외국인, 기관 수급
        list_day = []
        for i in range(0, min(len(df_ohlcv), 300), 100):  # 최대 300까지만
        # for i in range(0, 100*3, 100):
            list_day.append(df_ohlcv.iloc[i].name)

        dic_day = { 'date': [] }

        for i in range(3):  # 0부터 5까지 (총 6회)
            date_range = df_ohlcv.index[i * 100:(i + 1) * 100].tolist()
            dic_day['date'].extend(date_range)  # 리스트에 추가

        investor_data_list = []

        investor_data_dict = {'date': [], '개인': [], '외국인': [], '기관': [], '연기금': []}
        for date in list_day:
            self.dynamicCall("SetInputValue(QString, QString)", "일자", date)  # YYYYMMDD 형식의 날짜
            self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)  # 종목 코드
            self.dynamicCall("SetInputValue(QString, QString)", "금액수량구분", "2")  # 수량 기준 요청
            self.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")  # 순매수
            self.dynamicCall("SetInputValue(QString, QString)", "단위구분", "1")  # 단주
            self.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10059_req", "opt10059", 0, "1001")


            self.tr_event_loop.exec_()

            개인_data = self.tr_data.get('개인', 0)  # '개인' 키로 데이터 추출
            외국인_data = self.tr_data.get('외국인', 0)  # '기관' 키로 데이터 추출
            기관_data = self.tr_data.get('기관', 0)  # '기관' 키로 데이터 추출
            연기금_data = self.tr_data.get('연기금', 0)  # '연기금' 키로 데이터 추출

            investor_data_dict['개인'].extend(개인_data)  # 개인 데이터 추가
            investor_data_dict['외국인'].extend(외국인_data)  # 개인 데이터 추가
            investor_data_dict['기관'].extend(기관_data)  # 기관 데이터 추가
            investor_data_dict['연기금'].extend(연기금_data)  # 연기금 데이터 추가

        investor_data_dict['date'].extend(dic_day['date'])  # 날짜 추가

        df_investor = pd.DataFrame(investor_data_dict)
        df_investor.set_index('date', inplace=True)
        df_ohlcv = pd.concat([df_ohlcv, df_investor], axis=1)

        insert_df_to_db(code, df_ohlcv)

        return





    def set_price_1day(self, code, recent_day, df_recent):

        df_1day = get_db_1day(code)
        df_1day = pd.concat([df_recent, df_1day])

        # 결과 확인
        df_1day.loc[df_1day.index[0], 'a5'] = df_1day['close'].iloc[:5].mean()
        df_1day.loc[df_1day.index[0], 'a20'] = df_1day['close'].iloc[:20].mean()
        df_1day.loc[df_1day.index[0], 'a60'] = df_1day['close'].iloc[:60].mean()
        df_1day.loc[df_1day.index[0], 'a120'] = df_1day['close'].iloc[:120].mean()

        # RSI
        delta = df_1day['close'][0] - df_1day['close'][1]
        df_1day.loc[df_1day.index[0], 'u'] = max(delta, 0)
        df_1day.loc[df_1day.index[0], 'd'] = max(-delta, 0)

        N = 14
        df_1day.loc[df_1day.index[0], 'au'] = ((df_1day.loc[df_1day.index[1], 'au'] * (N - 1)) + df_1day['u'].iloc[0]) / N
        df_1day.loc[df_1day.index[0], 'ad'] = ((df_1day.loc[df_1day.index[1], 'ad'] * (N - 1)) + df_1day['d'].iloc[0]) / N
        df_1day.loc[df_1day.index[0], 'rsi'] = (df_1day['au'][0] * 100) / (df_1day['au'][0] + df_1day['ad'][0])

        N = 9
        df_1day.loc[df_1day.index[0], 'rsi9'] = df_1day['rsi'][:9].mean()



        # MACD (EMA12-EMA26)
        N = 12
        df_1day.loc[df_1day.index[0], 'ema12'] = (df_1day['close'].iloc[0] * (2 / (N + 1))) + (df_1day['ema12'].iloc[1] * (1 - (2 / (N + 1))))
        N = 26
        df_1day.loc[df_1day.index[0], 'ema26'] = (df_1day['close'].iloc[0] * (2 / (N + 1))) + (df_1day['ema26'].iloc[1] * (1 - (2 / (N + 1))))
        df_1day.loc[df_1day.index[0], 'macd'] = df_1day['ema12'][0] - df_1day['ema26'][0]

        # MACD9 계산
        N = 9
        df_1day.loc[df_1day.index[0], 'macd9'] = df_1day.loc[df_1day.index[0], 'macd'] * (2/(N+1)) + df_1day['macd9'].iloc[1] * (1 - 2/(N+1))





        # 볼린저밴드
        stddev_20 = df_1day['close'][::-1].rolling(window=20).std()

        df_1day.loc[df_1day.index[0], 'bol_u'] = df_1day.loc[df_1day.index[0], 'a20'] + stddev_20[len(stddev_20)-1] * 2
        df_1day.loc[df_1day.index[0], 'bol_l'] = df_1day.loc[df_1day.index[0], 'a20'] - stddev_20[len(stddev_20)-1] * 2

        bol_mean = (df_1day['bol_u'][0] - df_1day['bol_l'][0]).mean()

        if (df_1day['bol_u'][0] - df_1day['bol_l'][0]) > bol_mean * (1.5):
            df_1day.loc[df_1day.index[0], 'bol_size'] = "Big"
        else:
            df_1day.loc[df_1day.index[0], 'bol_size'] = "small"

        if df_1day['close'][0] > df_1day['bol_u'][0]:
            df_1day.loc[df_1day.index[0], 'bol_dolpa'] = "상향돌파"
        elif df_1day['close'][0] < df_1day['bol_l'][0]:
            df_1day.loc[df_1day.index[0], 'bol_dolpa'] = "하향돌파"
        else:
            df_1day.loc[df_1day.index[0], 'bol_dolpa'] = "보통"

        # 일목균형표
        high_26 = df_1day['high'][::-1].rolling(window=26).max()[::-1][26-1]
        low_26 = df_1day['low'][::-1].rolling(window=26).min()[::-1][26-1]
        kijun = (high_26 + low_26) / 2

        high_9 = df_1day['high'][::-1].rolling(window=9).max()[::-1][26-1]
        low_9 = df_1day['low'][::-1].rolling(window=9).min()[::-1][26-1]
        tenkan = (high_9 + low_9) / 2
        df_1day.loc[df_1day.index[0], 'ilmok_a'] = (kijun + tenkan) / 2

        high_52 = df_1day['high'][::-1].rolling(window=52).max()[::-1][26-1]
        low_52 = df_1day['low'][::-1].rolling(window=52).min()[::-1][26-1]
        df_1day.loc[df_1day.index[0], 'ilmok_b'] = (high_52 + low_52) / 2


        if (df_1day['high'][0] > df_1day['ilmok_a'][0]) & (df_1day['high'][0] > df_1day['ilmok_b'][0]):
            df_1day.loc[df_1day.index[0], 'ilmok_dolpa'] = "상향돌파"
        elif (df_1day['low'][0] < df_1day['ilmok_a'][0]) & (df_1day['low'][0] < df_1day['ilmok_b'][0]):
            df_1day.loc[df_1day.index[0], 'ilmok_dolpa'] = "하향돌파"
        elif ((df_1day['low'][0] > df_1day['ilmok_a'][0]) & (df_1day['low'][0] < df_1day['ilmok_b'][0])) | ((df_1day['low'][0] < df_1day['ilmok_a'][0]) & (df_1day['low'][0] > df_1day['ilmok_b'][0])) | ((df_1day['high'][0] > df_1day['ilmok_a'][0]) & (df_1day['high'][0] < df_1day['ilmok_b'][0])) | ((df_1day['high'][0] < df_1day['ilmok_a'][0]) & (df_1day['high'][0] > df_1day['ilmok_b'][0])):
            df_1day.loc[df_1day.index[0], 'ilmok_dolpa'] = "구름내부"
        else:
            df_1day.loc[df_1day.index[0], 'ilmok_dolpa'] = "?"

        if df_1day['ilmok_a'][0] > df_1day['ilmok_b'][0]:
            df_1day.loc[df_1day.index[0], 'ilmok_yang'] = "양운"
        else:
            df_1day.loc[df_1day.index[0], 'ilmok_yang'] = "음운"



        self.dynamicCall("SetInputValue(QString, QString)", "일자", recent_day)  # YYYYMMDD 형식의 날짜
        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)  # 종목 코드
        self.dynamicCall("SetInputValue(QString, QString)", "금액수량구분", "2")  # 수량 기준 요청
        self.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")  # 순매수
        self.dynamicCall("SetInputValue(QString, QString)", "단위구분", "1")  # 단주
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10059_req", "opt10059", 0, "1001")

        self.tr_event_loop.exec_()

        df_1day.loc[df_1day.index[0], '개인'] = self.tr_data.get('개인', 0)[0]
        df_1day.loc[df_1day.index[0], '외국인'] = self.tr_data.get('외국인', 0)[0]
        df_1day.loc[df_1day.index[0], '기관'] = self.tr_data.get('기관', 0)[0]
        df_1day.loc[df_1day.index[0], '연기금'] = self.tr_data.get('연기금', 0)[0]




        # df_1day.loc[df_1day.index[0], '개인'] = 0
        # df_1day.loc[df_1day.index[0], '외국인'] = 0
        # df_1day.loc[df_1day.index[0], '기관'] = 0
        # df_1day.loc[df_1day.index[0], '연기금'] = 0



        with sqlite3.connect('stock.db') as con:
            df_1day.to_sql(code, con, if_exists="replace", index=True, index_label="date")
        return









    def get_account_number(self):
        return self.account_number





    def get_account_list(self, tag="ACCNO"):
        account_list = self.dynamicCall("GetLoginInfo(QString)", tag)
        account_list = account_list.split(';')[:-1]
        return account_list

    def get_code_list_by_market(self, market_type):   # "0" 코스피      "10" 코스닥
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market_type)
        code_list = code_list.split(';')[:-1]
        return code_list

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_deposit(self):   # 예수금 조회
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_number)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "2")   # 3:추정조회, 2:일반조회
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00001_req", "opw00001", 0, "0002")
        self.tr_event_loop.exec_()
        temp = self.tr_data
        self.tr_data = -1
        return temp




    def get_balance(self):   # 잔고 조회
        print("[TR] get_balance() 계좌번호:", self.account_number)
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_number)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")  # 1: 합산, 2: 개별
        self.tr_data = None   # get_deposit에서 tr_data를 -1 로 했는데, None으로 해야 Dictionary 입력 가능
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00018_req", "opw00018", 0, "0002")
        self.tr_event_loop.exec_()   # 이벤트 루프 실행 (TR 응답 대기)
        return self.tr_data


    def get_hoga(self, code):   # 호가틱
        print("[TR] get_hoga() :", code)
        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10004_req", "opt10004", 0, "0101")

        self.tr_event_loop.exec_()  # _on_tr_data에서 종료시킴

        # TR 데이터 반환
        return self.tr_data
    

        # --- TR 데이터 수신 후 처리 ---
        # TR 수신 콜백 함수에서 처리되어야 함
        # 예: _on_tr_data(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, data)
        # 여기서는 TR 요청만 하고, 실제 호가 갱신은 _on_tr_data에서











    def send_order(self, rqname, screen_no, order_type, code, qty, price, hoga, org_order_no=""):
        order_result = self.dynamicCall(
            "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
            rqname,
            screen_no,
            self.account_number,
            order_type,
            code,
            qty,
            price,
            hoga,
            org_order_no
        )
        self.tr_event_loop.exec_()
        return order_result












    def get_order(self):
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_number)
        self.dynamicCall("SetInputValue(QString, QString)", "전체종목구분", "0")
        self.dynamicCall("SetInputValue(QString, QString)", "체결구분", "0")   # 0:전체, 1:미체결, 2:체결
        self.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")   # 0:전체, 1:매도, 2: 매수
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10075_req", "opt10075", 0, "0002")
        self.tr_event_loop.exec_()
        return self.tr_data



    def set_hoga_callback(self, code, func):
        """특정 종목 코드의 호가틱 콜백 함수 등록"""
        self.hoga_callback[code] = func







    def set_real_reg(self, screen_no, code, fids, real_type):
        print(f"[REAL 등록] {screen_no} {code} {fids} {real_type}")
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", screen_no, code, fids, real_type)

























