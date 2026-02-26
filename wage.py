import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor

from s1 import Sheet1Page
from s2 import Sheet2Page
from s3 import Sheet3Page
from s4 import Sheet4Page
from s5 import Sheet5Page
from s6 import Sheet6Page
from s7 import Sheet7Page
from s8 import Sheet8Page
from s9 import Sheet9Page
from s10 import Sheet10Page
from s11 import Sheet11Page
from s12 import Sheet12Page
from s13 import Sheet13Page
from s14 import Sheet14Page
from s15 import Sheet15Page
from s16 import Sheet16Page
from s17 import Sheet17Page
from s18 import Sheet18Page

import os
import json
from datetime import datetime
import pyperclip
import re





# --- 1. 파란색 하이라이트 커스텀 메뉴 (우클릭용) ---
class CustomMenu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QDialog { background-color: white; border: 1px solid #888888; }
            QPushButton { 
                border: none; text-align: left; padding: 8px 25px; 
                background-color: white; color: black; font-family: 'Malgun Gothic'; 
            }
            QPushButton:hover { background-color: #0078d7; color: white; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)

        self.btn_copy = QPushButton("복사 (Ctrl+C)")
        self.btn_paste = QPushButton("붙여넣기 (Ctrl+V)")
        layout.addWidget(self.btn_copy)
        layout.addWidget(self.btn_paste)

        self.btn_copy.clicked.connect(self.accept)
        self.btn_paste.clicked.connect(self.reject)




# --- 2. 검증 결과 창 클래스 ---
class VerificationResultWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("검증 결과")
        self.resize(1500, 880)
        
        layout = QVBoxLayout(self)
        
        # 결과를 보여줄 텍스트 박스
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(False)
        self.text_edit.setFont(QFont("Consolas", 10))
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # [추가] 텍스트 에리어 스크롤바 스타일 설정
        self.text_edit.setStyleSheet("""
            QScrollBar:vertical {
                border: 1px solid #dcdcdc;
                background: #f0f0f0;
                width: 14px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #bcbcbc; /* 스크롤바 핸들 색상 (진한 회색) */
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #888888; /* 마우스 올렸을 때 더 진하게 */
            }
            QScrollBar:horizontal {
                border: 1px solid #dcdcdc;
                background: #f0f0f0;
                height: 14px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #bcbcbc;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #888888;
            }
        """)
        
        # [핵심] 텍스트 에리어의 우클릭 메뉴 정책을 커스텀으로 변경
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_custom_menu)
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        
        layout.addWidget(self.text_edit)



        # 하단 버튼 레이아웃 스타일 설정
        button_style = """
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                color: #212529;
                padding: 8px 20px;
                font-size: 13px;
                font-family: 'Malgun Gothic';
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #adb5bd;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
            /* '전체 복사' 버튼에 포인트 컬러 적용 (파란색 계열) */
            QPushButton#copy_all_btn {
                background-color: #0078d7;
                color: white;
                border: none;
                font-weight: bold;
            }
            QPushButton#copy_all_btn:hover {
                background-color: #005a9e;
            }
            /* '닫기' 버튼 스타일 */
            QPushButton#close_btn {
                background-color: #6c757d;
                color: white;
                border: none;
            }
            QPushButton#close_btn:hover {
                background-color: #5a6268;
            }
        """

        # 하단 버튼 레이아웃
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 10, 0, 10) # 버튼 주변 여백
        btn_layout.setSpacing(12) # 버튼 사이 간격

        self.copy_btn = QPushButton("전체 복사")
        self.copy_btn.setObjectName("copy_all_btn") # 스타일 적용을 위한 ID
        
        # [기능 연결] 전체 선택 후 복사
        self.copy_btn.clicked.connect(lambda: (self.text_edit.selectAll(), self.text_edit.copy()))

        self.close_btn = QPushButton("닫기")
        self.close_btn.setObjectName("close_btn") # 스타일 적용을 위한 ID
        self.close_btn.clicked.connect(self.close)
        
        self.setStyleSheet(button_style) # 윈도우 전체에 버튼 스타일 적용

        btn_layout.addStretch(1)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.close_btn)
        # layout.addLayout(btn_layout)

        

    # [핵심] 텍스트 에리어 전용 메뉴 호출 함수
    # 텍스트 에리어 전용 메뉴 호출 및 기능 실행
    def show_custom_menu(self, pos):
        menu = CustomMenu(self)
        menu.move(QCursor.pos())
        
        # 메뉴 실행 및 결과 받기
        result = menu.exec_()
        
        # 1. 복사 기능 실행
        if result == QDialog.Accepted:
            cursor = self.text_edit.textCursor()
            if cursor.hasSelection():
                # 선택 영역이 있으면 선택된 부분만 복사
                self.text_edit.copy()
            else:
                # 선택 영역이 없으면 전체 선택 후 복사
                self.text_edit.selectAll()
                self.text_edit.copy()
            print("복사 완료")

        # 2. 붙여넣기 기능 실행
        elif result == QDialog.Rejected:
            # 메뉴 창을 그냥 닫았을 때와 구별하기 위해 버튼 클릭 여부 확인이 필요할 수 있으나, 
            # 현재 구조상 '붙여넣기' 버튼 클릭 시 Rejected를 반환하도록 설계됨
            self.text_edit.paste()
            print("붙여넣기 완료")

    def set_content(self, text):
        self.text_edit.setPlainText(text)
        
    def get_content(self):
        return self.text_edit.toPlainText()










        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("인건비 집계")        
        self.setGeometry(150, 150, 1100, 850)
        self.setStyleSheet("background-color: white;") 
        
        widget = QWidget()
        self.setCentralWidget(widget)
        self.layout = QVBoxLayout(widget)
        self.layout.setContentsMargins(10, 5, 10, 5)

        # 1. 상단 버튼바 (간격 최소화: spacing=2)
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(2) # 버튼 사이 간격을 2픽셀로 고정
        self.layout.addLayout(nav_layout)
        


        # 2. 하단 시트 탭
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.South)

        self.tabs.setStyleSheet("""
    QTabWidget::pane { 
        border: 1px solid #f2f2f2; /* 본문 테두리와 만나는 선을 아주 연하게 */
    }
    QTabBar::tab {
        background: #f8f8f8; 
        border: 1px solid #dcdcdc;
        padding: 6px 20px; 
        margin-right: 2px;
        color: #666;
    }
    QTabBar::tab:selected { 
        background: white; 
        border-bottom: 2px solid white; /* 선택된 탭이 본문과 연결된 느낌 */
        font-weight: bold;
        color: #000;
    }
""")


        btn_style = """
            QPushButton {
                border: 1px solid #dcdcdc;
                border-radius: 2px;
                padding: 3px 8px;
                background-color: #f9f9f9;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """
        
        self.btns = {}

        for btn_name in ["열기", "저장", "다른 이름으로 저장"]:
            btn = QPushButton(btn_name)
            btn.setStyleSheet(btn_style)
            btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            nav_layout.addWidget(btn)
            self.btns[btn_name] = btn

        nav_layout.addStretch(1)


        self.btns["열기"].clicked.connect(self.load_json)
        self.btns["저장"].clicked.connect(lambda: self.save_json(False))
        self.btns["다른 이름으로 저장"].clicked.connect(lambda: self.save_json(True))






        # --- 중간을 비워서 다음 버튼을 오른쪽 끝으로 밀어냄 ---
        nav_layout.addStretch(1)

        # 3. 검증 버튼 추가 (오른쪽 끝)
        btn_verify = QPushButton("검증")


        btn_verify.setStyleSheet("""
            QPushButton {
                border: 2px solid #0056b3;     /* 테두리 약간 두껍게 */
                border-radius: 4px;             /* 모서리 곡률 증가 */
                padding: 5px 38px;              /* 좌우 여백을 대폭 늘려 가로로 길게 */
                background-color: #e7f3ff;
                font-family: "Malgun Gothic";   /* 맑은 고딕 */
                font-size: 13px;                /* 글자 크기 확대 */
                font-weight: bold;              /* 굵게 */
                letter-spacing: 2px;
                color: #0056b3;
            }
            QPushButton:hover { 
                background-color: #0056b3; 
                color: white;                   /* 마우스 올리면 반전 효과 */
            }
        """)
        
        # 주변 레이아웃에 영향을 주지 않도록 높이 고정 (선택 사항)
        btn_verify.setFixedHeight(32)

        nav_layout.addWidget(btn_verify)
        self.btns["검증"] = btn_verify

        # 시그널 연결 (검증 로직 함수 호출)
        self.btns["검증"].clicked.connect(self.run_verification)


        self.run_verification()



    def init_sheet(self):


        global company, year, list_years2, list_years3, check_3_5, check_3_6, check_4

        
        self.tabs.clear()
        
        sheet_names = {
            1: "(2)인건비집계", 2: "(3)총인건비인상률", 3: "(3-1)증원소요인건비", 4: "(3-2)직급별평균인원", 5: "(3-3)가.정원및현원", 
            6: "(3-3)나.근속승진", 7: "(3-3)다.증원", 8: "(3-4)직급별단가", 9: "(3-6)가.초임정원", 10: "(3-6)나.인건비효과",
            11: "(3-5)가.별도직군", 12: "(3-5)나.인원", 13: "(3-5)다.미승진자", 14: "(3-5)라.인건비효과",
            15: "(4)노동생산성", 16: "(6)일반관리비", 17: "4.총보수", 18: "4.기준보수"
        }





        

        # 각 번호에 맞는 시트 클래스를 연결
        for i in range(1, 19):

            page = None

            if i == 1:
                self.s1 = Sheet1Page(company, year, list_years2, list_years3, check_3_5, check_3_6, check_4)
                page = self.s1

            elif i == 2:
                self.s2 = Sheet2Page(company, year, list_years2, list_years3, check_3_5, check_3_6, check_4)
                page = self.s2
            elif i == 3:
                self.s3 = Sheet3Page(self)
                page = self.s3



            elif i == 4:
                self.s4 = Sheet4Page(self)
                page = self.s4

            elif i == 5:
                self.s5 = Sheet5Page(self)
                page = self.s5

            elif i == 6:
                self.s6 = Sheet6Page(self)
                page = self.s6
            elif i == 7:
                self.s7 = Sheet7Page(self)
                page = self.s7
            elif i == 8:
                self.s8 = Sheet8Page(self)
                page = self.s8




            elif i == 9 and check_3_6:
                self.s9 = Sheet9Page(self)
                page = self.s9
            elif i == 10 and check_3_6:
                self.s10 = Sheet10Page(self)
                page = self.s10




            elif i == 11 and check_3_5:
                self.s11 = Sheet11Page(self)
                page = self.s11
            elif i == 12 and check_3_5:
                self.s12 = Sheet12Page(self)
                page = self.s12
            elif i == 13 and check_3_5:
                self.s13 = Sheet13Page(self)
                page = self.s13
            elif i == 14 and check_3_5:
                self.s14 = Sheet14Page(self)
                page = self.s14



            # elif i == 15:
            #    self.s15 = Sheet15Page(self)
            #    page = self.s15
            # elif i == 16:
            #   self.s16 = Sheet16Page(self)
            #   page = self.s16
            

            elif i == 17 and check_4:
                self.s17 = Sheet17Page(self)
                page = self.s17
            elif i == 18 and check_4:
                self.s18 = Sheet18Page(self)
                page = self.s18






            '''   
            else:
                page = QWidget() # 나머지는 아직 빈 페이지
            '''

            if page:
                self.tabs.addTab(page, sheet_names.get(i, f"Sheet{i}"))


        self.tabs.setCurrentIndex(0)
        self.layout.addWidget(self.tabs)


        self.s5.table.itemChanged.connect(lambda: self.s6.sync_from_s5(self.s5.get_data_for_s6()))
        self.s6.table.itemChanged.connect(lambda: self.s7.sync_s7_data(self.s4.get_data_to7(), self.s6.get_data_to7()))




        def on_s4_changed():
            # 1. S4에서 평균 데이터를 가져와 S8 업데이트
            self.s8.sync_from_s4(self.s4.get_avg_data_to8())
            
            # 2. 업데이트된 S8의 단가를 S3(갑)와 S10(을)에 즉시 반영 (중요!)
            # S3(갑) 업데이트
            self.s3.sync_unit_price_from_s8(self.s8.get_unit_price_to3())
            self.s2.sync_from_s3(self.s3.get_gab_to_s2())

            if check_3_6:
                # S10(을) 업데이트 및 S2 전송
                self.s10.sync_unit_price_from_s8(self.s8.get_unit_price_to10())
                self.s10.calculate_s10()
                self.s2.sync_eul_from_s10(self.s10.get_eul_to_s2())

        # 기존의 단순 s8.sync_from_s4 연결을 위 함수로 교체
        self.s4.table.itemChanged.connect(on_s4_changed)
        
        # S7 연계는 기존처럼 유지 (인원 데이터)
        self.s4.table.itemChanged.connect(lambda: self.s7.sync_s7_data(self.s4.get_data_to7(), self.s6.get_data_to7()))
        



        # --- [1] S7(인원) -> S3 -> S2 (갑 전송) ---
        self.s7.table.itemChanged.connect(lambda: [
            self.s3.sync_from_s7(self.s7.get_average_personnel_to3()),
            self.s2.sync_from_s3(self.s3.get_gab_to_s2())
        ])



        # --- [3] S8(단가)은 S3(갑)와 S10(을) 모두에 영향을 주므로 통합 처리 ---
        def on_s8_changed(item):
            # 단가와 관련된 열(2~13열, 15열)이 바뀔 때만 작동
            if 2 <= item.column() <= 13 or item.column() == 15:
                # 1. S3(갑) 업데이트 및 S2 전송
                self.s3.sync_unit_price_from_s8(self.s8.get_unit_price_to3())
                self.s2.sync_from_s3(self.s3.get_gab_to_s2())


                if check_3_6:                
                    # 2. S10(을) 업데이트 및 S2 전송
                    self.s10.sync_unit_price_from_s8(self.s8.get_unit_price_to10())
                    self.s10.calculate_s10()
                    self.s2.sync_eul_from_s10(self.s10.get_eul_to_s2())

        self.s8.table.itemChanged.connect(on_s8_changed)



        self.s1.table.itemChanged.connect(lambda: self.s2.sync_from_s1(self.s1.get_data_to_s2()))
        
        self.s3.table.itemChanged.connect(lambda item: self.s2.sync_from_s3(self.s3.get_gab_to_s2()))



        if check_3_5:
            self.s5.table.itemChanged.connect(lambda: self.s11.sync_from_s5(self.s5.send_to_s11_from_s5()))
            self.s11.table.itemChanged.connect(lambda: self.s12.get_from_s11(self.s11.send_to_s12()))
            self.s13.table.itemChanged.connect(lambda: self.s12.get_from_s13(self.s13.send_to_s12()))
            self.s13.table.itemChanged.connect(lambda: self.s14.get_from_s13(self.s13.send_to_s14()))
            self.s8.table.itemChanged.connect(lambda: self.s14.get_from_s8(self.s8.send_to_s14()))




        if check_3_6:
            self.s10.table.itemChanged.connect(lambda item: self.s2.sync_eul_from_s10(self.s10.get_eul_to_s2()))

            # --- [2] S9(데이터) -> S10 -> S2 (을 전송) ---
            self.s9.table.itemChanged.connect(lambda: [
                self.s10.sync_from_s9(self.s9.get_data_to10()),
                self.s10.calculate_s10(), 
                self.s2.sync_eul_from_s10(self.s10.get_eul_to_s2())
            ])




        



    def save_json(self, is_save_as=False):
        import json, os
        
        if is_save_as or not hasattr(self, 'current_path') or not self.current_path:
            default_name = os.path.join(os.getcwd(), "인건비.json")
            path, _ = QFileDialog.getSaveFileName(self, "데이터 저장", default_name, "JSON Files (*.json);;Text Files (*.txt)")
            if not path: return
            self.current_path = path
        else:
            path = self.current_path

        total_data = {}
        total_data['active_tab_index'] = self.tabs.currentIndex()
        
        for i in range(self.tabs.count()):
            sheet_name = self.tabs.tabText(i)
            page = self.tabs.widget(i)
            
            if hasattr(page, 'table'):
                table = page.table
                rows_data = []
                for r in range(table.rowCount()):
                    cols_data = []
                    for c in range(table.columnCount()):
                        it = table.item(r, c)
                        cols_data.append(it.text() if it else "")
                    rows_data.append(cols_data)
                total_data[sheet_name] = rows_data

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(total_data, f, ensure_ascii=False, indent=4)
            
            self.setWindowTitle(f"인건비 집계 - {os.path.basename(path)}")
            QMessageBox.information(self, "완료", "데이터가 저장되었습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"저장 실패: {e}")




    def load_json(self, data=''):
        import json, os
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        from PyQt5.QtCore import Qt

        global check_3_6, check_3_5

        if data != 'excel_input':

            path, _ = QFileDialog.getOpenFileName(self, "데이터 불러오기", os.getcwd(), "JSON Files (*.json)")
            if not path: return

        try:
            rank_count_03 = len(list(self.list_title_03))
            rank_count_04 = len(list(self.list_title_04))
            rank_count_05 = len(list(self.list_title_05))
            rank_count_06 = len(list(self.list_title_06))
            rank_count_07 = len(list(self.list_title_07))
            rank_count_08 = len(list(self.list_title_08))

            if check_3_6:
                rank_count_09 = len(list(self.list_title_09))
                rank_count_10 = len(list(self.list_title_10))

            if data != 'excel_input':
                with open(path, 'r', encoding='utf-8') as f:
                    total_data = json.load(f)
            else:
                pass

            if 1==1:
                
                for i in range(self.tabs.count()):


                    if data != 'excel_input':
                        sheet_name = self.tabs.tabText(i)
                        if sheet_name in total_data:
                            page = self.tabs.widget(i)
                            table = page.table
                            sheet_content = total_data[sheet_name]

                            # 1. 데이터 입력 (신호 차단)
                            table.blockSignals(True)
                            for r_idx, row_values in enumerate(sheet_content):
                                if r_idx >= table.rowCount(): break
                                for c_idx, val in enumerate(row_values):
                                    if c_idx >= table.columnCount(): break
                                    item = table.item(r_idx, c_idx)
                                    if item:
                                        # [중요] Editable 체크를 빼야 ReadOnly 칸도 데이터를 불러옵니다.
                                        item.setData(Qt.EditRole, val)
                            table.blockSignals(False)
                    else:
                        page = self.tabs.widget(i)
                        table = page.table


                        # wage.py 의 load_json 함수 try 블록 맨 마지막
                        if hasattr(self, 's3'):
                            self.s3.calculate_s3(None) # 인자값으로 None을 주면 전체 계산 실행


                


                    # 2. 시트별 계산 함수 탐색
                    calc_func = None
                    for attr in dir(page):
                        if "calculate" in attr.lower():
                            calc_func = getattr(page, attr)
                            break
                    
                    if calc_func:

                        # --- 1. S1 (판관비) 트리거 로직 ---
                        if calc_func.__name__ == "calculate_s1":
                            for c in range(1, 6): # B~F열
                                # 사용자님이 강조하신 "소계 구간별 트리거" 적용
                                t_a = table.item(0, c)  # 소계a 구간
                                t_b = table.item(13, c) # 소계b (복리후생비) 구간
                                t_c = table.item(39, c) # 소계c 및 총계 구간
                                try:
                                    if t_a: calc_func(t_a)
                                    if t_b: calc_func(t_b)
                                    if t_c: calc_func(t_c)
                                except: pass
                            
                            # S1 계산 직후 S2로 데이터 전송 (연쇄 반응)
                            if hasattr(self, 's2'):
                                self.s2.sync_from_s1(self.s1.get_data_to_s2())


                        
                        if calc_func.__name__ == "calculate_s3":
                            # 3번 시트 데이터 행: 표1(0~7), 표2(11~18)
                            # active_rows = list(range(0, 8)) + list(range(11, 19))
                            active_rows = list(range(0, rank_count_03)) + list(range((rank_count_03+3), (rank_count_03*2)+3))
                            
                            # 1. 모든 데이터 행의 가로 평균(14열) 계산 (행 순회)
                            for r in active_rows:
                                # 1월(2열) 데이터를 트리거로 던져서 해당 행의 가로 연산을 먼저 끝냄
                                trigger = table.item(r, 2)
                                if trigger:
                                    try: calc_func(trigger)
                                    except: pass

                            # 2. 모든 열의 세로 합계(8행, 19행) 계산 (열 순회)
                            # 2열(1월)부터 14열(평균/합계열)까지 순차적으로 트리거
                            for c in range(2, 15):
                                # 표1의 마지막 데이터(7행)와 표2의 마지막 데이터(18행)를 찔러서
                                # 하단의 '계' 행이 현재 채워진 모든 가로 데이터를 합산하게 만듦
                                t1, t2 = table.item(rank_count_03-1, c), table.item((rank_count_03*2)+2, c)
                                try:
                                    if t1: calc_func(t1)
                                    if t2: calc_func(t2)
                                except: pass

                        elif calc_func.__name__ == "calculate_s4":
                            
                            # 데이터 행만 순회 (0~6, 11~17)
                            active_rows = list(range(0, len(self.list_title_04) - 1)) + list(range(len(self.list_title_04) + 3, len(self.list_title_04) + 3 + len(self.list_title_04) - 1))
                            
                            for r in active_rows:
                                # r이 현재 테이블의 행 수보다 적은지 확인하는 안전장치
                                if r < table.rowCount():
                                    trigger_item = table.item(r, 2) 
                                    if trigger_item:
                                        try: calc_func(trigger_item)
                                        except: pass

                            # 세로 합계 트리거
                            for c in range(2, 14):
                                # 전년도(0행), 당년도(11행) 기준
                                for base_r in [0, len(self.list_title_04) + 3]:
                                    if base_r < table.rowCount():
                                        trigger_it = table.item(base_r, c)
                                        if trigger_it:
                                            try: calc_func(trigger_it)
                                            except: pass

                            self.s8.sync_from_s4(self.s4.get_avg_data_to8())




                        elif calc_func.__name__ == "calculate_s5":
                            
                            # 1. 누적차 및 합계 트리거링할 행 (각 표의 첫 번째 데이터 행만 찔러도 전체 계산됨)
                            # 하지만 안전하게 데이터가 있는 첫 행인 0행과 11행만 사용
                            rows_to_trigger = [0, len(self.list_title_05) + 3] # [0, 11]
                            
                            # 2. 각 월의 시작 열 (정원 열: 2, 6, 10, 14, 18, 22)
                            month_cols = [2, 6, 10, 14, 18, 22] 

                            for r in rows_to_trigger:
                                if r < table.rowCount():
                                    for c in month_cols:
                                        trigger_item = table.item(r, c)
                                        if trigger_item:
                                            try:
                                                # 이 호출 한 번으로 해당 월 전체 누적차 + 세로 합계가 계산됨
                                                calc_func(trigger_item)
                                            except:
                                                pass

                            # 3. S6로 연계 데이터 전송 (참고 코드의 s5_changed 로직 반영)
                            # self.s5.get_data_for_s6()를 통해 음수 누적차를 절댓값으로 변환하여 전달
                            self.s6.sync_from_s5(self.s5.get_data_for_s6())



                        elif calc_func.__name__ in ["calculate_s7"]:
                        # elif "s7" in sheet_name or "s8" in sheet_name:
                            # 7번 시트 특성: 1~12월 데이터를 기반으로 14열(평균)과 8행/19행(합계) 계산
                            # 표 1: 0~7행 데이터, 8행 합계 / 표 2: 11~18행 데이터, 19행 합계
                            
                            # 1. 모든 데이터 행에 대해 '가로 평균' 계산 트리거
                            # active_rows = list(range(0, 8)) + list(range(11, 19))
                            active_rows = list(range(0, rank_count_07)) + list(range((rank_count_07+3), (rank_count_07*2)+3))

                            
                            for r in active_rows:
                                # 2열(1월) 아이템을 던져서 해당 행의 가로 평균(14열)을 계산하게 함
                                trigger = table.item(r, 2)
                                if trigger:
                                    try: calc_func(trigger)
                                    except: pass

                            # 2. 모든 열(1월~평균열)에 대해 '세로 합계' 계산 트리거
                            # 2열(1월)부터 14열(평균)까지
                            for c in range(2, 15):
                                # 표 1 합계 트리거 (0행의 셀을 던짐)
                                t1 = table.item(0, c)
                                if t1:
                                    try: calc_func(t1)
                                    except: pass
                                
                                # 표 2 합계 트리거 (11행의 셀을 던짐)
                                # t2 = table.item(11, c)
                                t2 = table.item(rank_count_07+3, c)

                                if t2:
                                    try: calc_func(t2)
                                    except: pass




                        elif calc_func.__name__ in ["calculate_s8"]:
                        # elif "s7" in sheet_name or "s8" in sheet_name:
                            # 7번 시트 특성: 1~12월 데이터를 기반으로 14열(평균)과 8행/19행(합계) 계산
                            # 표 1: 0~7행 데이터, 8행 합계 / 표 2: 11~18행 데이터, 19행 합계
                            
                            # 1. 모든 데이터 행에 대해 '가로 평균' 계산 트리거
                            # active_rows = list(range(0, 8)) + list(range(11, 19))
                            active_rows = list(range(0, rank_count_08)) + list(range((rank_count_08+3), (rank_count_08*2)+3))

                            
                            for r in active_rows:
                                # 2열(1월) 아이템을 던져서 해당 행의 가로 평균(14열)을 계산하게 함
                                trigger = table.item(r, 2)
                                if trigger:
                                    try: calc_func(trigger)
                                    except: pass

                            # 2. 모든 열(1월~평균열)에 대해 '세로 합계' 계산 트리거
                            # 2열(1월)부터 14열(평균)까지
                            for c in range(2, 15):
                                # 표 1 합계 트리거 (0행의 셀을 던짐)
                                t1 = table.item(0, c)
                                if t1:
                                    try: calc_func(t1)
                                    except: pass
                                
                                # 표 2 합계 트리거 (11행의 셀을 던짐)
                                t2 = table.item(rank_count_08+3, c)
                                if t2:
                                    try: calc_func(t2)
                                    except: pass

                            if calc_func.__name__ in ["calculate_s8"]:
                                self.s3.sync_unit_price_from_s8(self.s8.get_unit_price_to3())
                                self.s2.sync_from_s3(self.s3.get_gab_to_s2())

                                if check_3_6:
                                    self.s10.sync_unit_price_from_s8(self.s8.get_unit_price_to10())






                                    

                        elif calc_func.__name__ == "calculate_s9":
                            if check_3_6:
                                # 데이터 행: 표1(0~7), 표2(11~18)
                                # active_rows = list(range(0, 8)) + list(range(11, 19))
                                active_rows = list(range(0, rank_count_09)) + list(range((rank_count_09+3), (rank_count_09*2)+3))

                                # 1. 모든 데이터 행의 가로 평균(14열)부터 먼저 계산 (행 순회)
                                for r in active_rows:
                                    # 1월(2열) 데이터를 트리거로 던져서 해당 행의 평균을 먼저 뽑음
                                    trigger = table.item(r, 2)
                                    if trigger:
                                        try: calc_func(trigger)
                                        except: pass

                                # 2. 가로 평균들이 다 계산된 후, 각 열의 세로 합계(8행, 19행) 계산 (열 순회)
                                # 1월(2열)부터 평균열(14열)까지 전체 순회
                                for c in range(2, 15):
                                    # 상반기(8행)와 하반기(19행) 합계를 위해 데이터 끝 행인 7행과 18행을 트리거
                                    t1, t2 = table.item(rank_count_09-1, c), table.item((rank_count_09*2)+2, c)
                                    try:
                                        if t1: calc_func(t1)
                                        if t2: calc_func(t2)
                                    except: pass


                                self.s10.sync_from_s9(self.s9.get_data_to10())
                                self.s10.calculate_s10()
                                self.s2.sync_eul_from_s10(self.s10.get_eul_to_s2())


                                

                        elif calc_func.__name__ == "calculate_s10":
                            if check_3_6:
                                # 1. 가로 연산 (증감C, 효과E) 및 기본 합계 트리거
                                for r in range(rank_count_10):
                                    # 2열(개편)을 찔러서 가로 연산을 먼저 끝냄
                                    trigger_main = table.item(r, 2)
                                    if trigger_main:
                                        try: calc_func(trigger_main)
                                        except: pass
                                        
                                # 2. 단가 열(4열) 합계 트리거
                                # 4열 단가 데이터를 하나 찔러서 위에서 수정한 합계 루프(1~5열 전체)가 돌게 함
                                trigger_price = table.item(0, 4)
                                if trigger_price:
                                    try: calc_func(trigger_price)
                                    except: pass

                                self.s10.calculate_s10()
                                self.s2.sync_eul_from_s10(self.s10.get_eul_to_s2())
                                for c in [2, 3, 4]:
                                    # 각 열의 첫 번째 데이터 행(1행)만 딱 한 번씩 호출
                                    target = self.s2.table.item(1, c)
                                    if target:
                                        self.s2.calculate_s2(target)




                        elif calc_func.__name__ == "calculate_s2":
                            # 2열(당년), 3열(전년), 4열(전전년) 전체 순회
                            for c in range(2, 5):
                                # 소계 A, B, C를 각각 계산하도록 본체 함수 호출
                                calc_func(table.item(1, c))  # 소계(A) 트리거
                                calc_func(table.item(8, c))  # 소계(B) 트리거
                                calc_func(table.item(30, c)) # 최종(C) 및 인상률 트리거








            if data != 'excel_input':
                if 'active_tab_index' in total_data:
                    target_index = total_data['active_tab_index']
                    # 인덱스가 유효한지 확인 후 이동
                    if 0 <= target_index < self.tabs.count():
                        self.tabs.setCurrentIndex(target_index)
                self.current_path = path
                self.setWindowTitle(f"인건비 집계 검증 - {os.path.basename(path)}")

        except Exception as e:
            QMessageBox.critical(self, "오류", f"불러오기 실패: {e}")





    def notice(self, title='로봇 작업'):
        import tkinter as tk
        
        root = tk.Tk()

        root.overrideredirect(True)   # 타이틀바 없애기

        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()

        window_width = int(screenwidth / 1.0)
        window_height = int(screenheight / 1.0)   # 2.5
        
        position_top = int(screenheight / 2 - window_height / 2)
        position_right = int(screenwidth / 2 - window_width / 2)

        root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        root.config(bg='white')  # 배경 흰색

        label = tk.Label(root, text=title, font=("Helvetica", 145, "bold"), bg='white')    # 145
        label.pack(padx=20, pady=388)   # 118
        
        root.after(3000, root.destroy) # 3초 후에 창 닫기 3000
        root.mainloop()






















    def run_verification(self):

        current_index = self.tabs.currentIndex()+1

        global recent_temp, excel_temp, excel_original, excel_original_01, excel_original_02, excel_original_03, excel_original_04, excel_original_05, excel_original_06, excel_original_07, excel_original_08, excel_original_09, excel_original_10
        global excel_original_11, excel_original_12, excel_original_13, excel_original_14, excel_original_18
        recent_temp = ''
        excel_temp = ''
        excel_original = ''

        import pygetwindow as gw
        import win32gui
        import time

        try:
            rpa01 = self.rpa(1)

            if rpa01 in ["excel_original_no"]: return
            if rpa01 in ["open_found"]:   # 인건비 엑셀이 열려있는 경우
                excel_original += excel_temp.replace(' ', '').replace('\t-\t', '\t\t')
                recent_temp = excel_temp

                for i in range(2, 20):
                    
                    if self.rpa(i) in ["Excel", "excel_original_no"]:
                       return 
                    if recent_temp == excel_temp:
                        break
                    if '(2)-1. 임금관련 세부자료' in excel_temp:
                        continue




                    
                    excel_original += excel_temp.replace(' ', '').replace('\t-\t', '\t\t')
                    recent_temp = excel_temp

                    # if '나.초임직급' in excel_original: break






                for item in gw.getAllWindows():
                    if '인건비' in item.title and win32gui.GetClassName(item._hWnd) == 'XLMAIN':
                        win = item
                        break
                time.sleep(0.1)
                if win:
                    import win32con
                    win32gui.ShowWindow(win._hWnd, win32con.SW_SHOWMINIMIZED)

                self.notice('엑셀 탐색 완료')

            global company, year, list_years2, list_years3, check_3_5, check_3_6, check_4
            company = 'nhis'
            year = '2025'
            check_3_5 = False
            check_3_6 = False
            check_4 = False







            excel_original = excel_original.replace('2023년1월', '1월').replace('2023년1월', '1월').replace('2023년2월', '2월').replace('2023년3월', '3월').replace('2023년4월', '4월').replace('2023년5월', '5월').replace('2023년6월', '6월').replace('2023년7월', '7월').replace('2023년8월', '8월').replace('2023년9월', '9월').replace('2023년10월', '10월').replace('2023년11월', '11월').replace('2023년12월', '12월')
            excel_original = excel_original.replace('2024년1월', '1월').replace('2024년1월', '1월').replace('2024년2월', '2월').replace('2024년3월', '3월').replace('2024년4월', '4월').replace('2024년5월', '5월').replace('2024년6월', '6월').replace('2024년7월', '7월').replace('2024년8월', '8월').replace('2024년9월', '9월').replace('2024년10월', '10월').replace('2024년11월', '11월').replace('2024년12월', '12월')
            excel_original = excel_original.replace('2025년1월', '1월').replace('2025년1월', '1월').replace('2025년2월', '2월').replace('2025년3월', '3월').replace('2025년4월', '4월').replace('2025년5월', '5월').replace('2025년6월', '6월').replace('2025년7월', '7월').replace('2025년8월', '8월').replace('2025년9월', '9월').replace('2025년10월', '10월').replace('2025년11월', '11월').replace('2025년12월', '12월')
            excel_original = excel_original.replace('202301', '1월').replace('202301', '1월').replace('202302', '2월').replace('202303', '3월').replace('202304', '4월').replace('202305', '5월').replace('202306', '6월').replace('202307', '7월').replace('202308', '8월').replace('202309', '9월').replace('202310', '10월').replace('202311', '11월').replace('202312', '12월')
            excel_original = excel_original.replace('202401', '1월').replace('202401', '1월').replace('202402', '2월').replace('202403', '3월').replace('202404', '4월').replace('202405', '5월').replace('202406', '6월').replace('202407', '7월').replace('202408', '8월').replace('202409', '9월').replace('202410', '10월').replace('202411', '11월').replace('202412', '12월')
            excel_original = excel_original.replace('202501', '1월').replace('202501', '1월').replace('202502', '2월').replace('202503', '3월').replace('202504', '4월').replace('202505', '5월').replace('202506', '6월').replace('202507', '7월').replace('202508', '8월').replace('202509', '9월').replace('202510', '10월').replace('202511', '11월').replace('202512', '12월')
            excel_original = excel_original.replace('\t\t구분\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균\t정원\t', '')        

            list_s = excel_original.split('_$$$$$_')


            cnt_page = 0
            for i in range(cnt_page, len(list_s)):
                if ('인건비집계' in list_s[i] and '소계' in list_s[i] and '해당' in list_s[i]) or ('인건비항목' in list_s[i] and '소계' in list_s[i] and '해당' in list_s[i]) or ('판관비' in list_s[i] and '소계' in list_s[i] and '해당' in list_s[i]):
                    excel_original_01 = list_s[i]
                    cnt_page += 1
                    break
                cnt_page += 1


            for i in range(cnt_page, len(list_s)):
                if ('총인건비인상률' in list_s[i] and '소계' in list_s[i] and '가이드' in list_s[i]) or ('구분' in list_s[i] and '소계' in list_s[i] and '가이드' in list_s[i]) or ('인센티브' in list_s[i] and '소계' in list_s[i] and '가이드' in list_s[i]):
                    excel_original_02 = list_s[i]
                    cnt_page += 1
                    break
                cnt_page += 1

            for i in range(cnt_page, len(list_s)):
                if ('증원' in list_s[i] or '증감' in list_s[i] or '평균단가' in list_s[i]):
                    excel_original_03 = list_s[i]
                    cnt_page += 1
                    break
                cnt_page += 1






            for i in range(cnt_page, len(list_s)):
                if ('직급별' in list_s[i] or '평균인원' in list_s[i]):
                    excel_original_04 = list_s[i]
                    cnt_page += 1
                    break
                cnt_page += 1

             

            for i in range(cnt_page, len(list_s)):

                if ('복직' in list_s[i] or '누적' in list_s[i]):
                    excel_original_05 = list_s[i].split('\t1월\t')[1]

                    if list_s[i].count('\t1월\t') > 1:
                        excel_original_06 = list_s[i].split('\t1월\t')[2]
                        excel_original_07 = ''.join(list_s[i].split('\t1월\t')[3:])
                        cnt_page += 1
                        break
                    else:
                        excel_original_06 = list_s[i+1].split('\t1월\t')[1]
                        cnt_page += 1
                        excel_original_07 = list_s[i+2].split('\t1월\t')[1]
                        cnt_page += 1
                        break
                cnt_page += 1


            for i in range(cnt_page, len(list_s)):
                if ('직급별' in list_s[i] or '평균단가' in list_s[i]):
                    excel_original_08 = list_s[i]
                    cnt_page += 1
                    break
                cnt_page += 1


            for i in range(cnt_page, len(list_s)):

                if '당해' in repr(excel_original.split('_$$$$$_')[i][:300]):
                    check_3_5 = True
                    excel_original_11 = list_s[i].split('\t1월\t')[1]
                    excel_original_12 = list_s[i].split('\t1월\t')[2]
                    excel_original_13 = list_s[i].split('\t1월\t')[3] + list_s[i].split('\t1월\t')[4].split('미승진')[0]
                    excel_original_14 = list_s[i].split('\t1월\t')[4].split('미승진')[1].replace('인원', '')
                    cnt_page += 1
                    break
                else:
                    check_3_6 = True
                    if list_s[i].count('증감') > 0:
                        excel_original_09 = list_s[i].split('증감')[0]
                        excel_original_10 = list_s[i].split('증감')[1]
                        cnt_page += 1
                        break
                            
                    else:
                        excel_original_09 = list_s[i]
                        cnt_page += 1
                        excel_original_10 = list_s[i+1]
                        cnt_page += 1
                        break
                cnt_page += 1





            for i in range(cnt_page, len(list_s)):
                if '직무급' in list_s[i]:
                    check_4 = True
                    if '급료' in list_s[i]:
                        excel_original_18 = list_s[i]
                        break
                    else:
                        excel_original_18 = list_s[i].strip() + list_s[i+1].strip()
                        break




                        






            list_years2 = re.findall(r'20[0-8]\d', excel_original_01.split('기본급')[0])
            list_years3 = re.findall(r'20[0-8]\d', excel_original_02.split('인센')[0].replace('1.', '')) # (3) ['2024', '2023']

            year = max(list_years3)
            if year < '2023': year = '2023'

            list_years3 = list_years3[:3]








        
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()            
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] RPA 오류: " + str(current_index) + "번 표\n")
                f.write(f"{error_details}\n\n")
            print(error_details)
            QMessageBox.information(self, "RPA 오류: " + str(current_index) + "번 표", "RPA 오류: " + str(current_index) + "번 표\n\n해결되지 않는 경우, log.txt를 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")

            return

        excel_original_03 = excel_original_03.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')
        excel_original_04 = excel_original_04.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')
        excel_original_05 = excel_original_05.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')
        excel_original_06 = excel_original_06.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')
        excel_original_07 = excel_original_07.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')
        excel_original_08 = excel_original_08.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '').replace('통합직급', '').replace('인건비총계', '')

        list_not_page = ['정원', '현원', '복직', '복직자', '누적', '누적차', '인원', '초임직급정원', '평균정원', '평균인원']

        self.list_title_03 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_03))
        self.list_title_03 = [item for item in self.list_title_03 if item not in list_not_page]
        
        self.list_title_04 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_04))
        self.list_title_04 = [item for item in self.list_title_04 if item not in list_not_page]

        self.list_title_05 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|군|원|우))\t', excel_original_05))
        self.list_title_05 = [item for item in self.list_title_05 if item not in list_not_page]

        self.list_title_06 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_06))
        self.list_title_06 = [item for item in self.list_title_06 if item not in list_not_page]
        
        self.list_title_07 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_07))
        self.list_title_07 = [item for item in self.list_title_07 if item not in list_not_page]

        self.list_title_08 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_08))
        self.list_title_08 = [item for item in self.list_title_08 if item not in list_not_page]


        if check_3_5 == False and check_3_6 == True:
            excel_original_09 = excel_original_09.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')
            excel_original_10 = excel_original_10.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')            
            self.list_title_09 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_09))
            self.list_title_09 = [item for item in self.list_title_09 if item not in list_not_page]
            self.list_title_10 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_10))
            self.list_title_10 = [item for item in self.list_title_10 if item not in list_not_page]


        if check_3_5 == True and check_3_6 == False:
            excel_original_11 = excel_original_11.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')            
            excel_original_12 = excel_original_12.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')            
            excel_original_13 = excel_original_13.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')            
            excel_original_14 = excel_original_14.replace('\t직급', '').replace('\r\n직급', '').replace('직급별', '')                        
            self.list_title_11 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_11))
            self.list_title_11 = [item for item in self.list_title_11 if item not in list_not_page]
            self.list_title_12 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_12))
            self.list_title_12 = [item for item in self.list_title_12 if item not in list_not_page]
            self.list_title_13 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_13))
            self.list_title_13 = [item for item in self.list_title_13 if item not in list_not_page]
            self.list_title_14 = (lambda x: x[: (next((i for i,v in enumerate(x) if v in ('계','총계','합계')), len(x)-1)) + 1])(re.findall(r'(?m)^.*?\t*((?:계|총계|합계)|[가-힣0-9]+(?:급|직|장|사|원|군|우))\t', excel_original_14))
            self.list_title_14 = [item for item in self.list_title_14 if item not in list_not_page]




        self.init_sheet()


        if self.excel_input() == 'str_not':   # 엑셀 입력값 중 부적절한 인건비 항목이 있으면 종료
            return
        return









        '''        
        excel_original_01 = excel_original.split('\t2024')[0]
        excel_original_02 = re.split(r'\t1급\t|\t1직급\t|\r\n1급\t|\r\n1직급\t', excel_original.split('\t2024')[1])[0]
        excel_original_03 = "".join(excel_original.split('평균단가')[1]).split('\t1월\t')[0]
        excel_original_04 = "".join(excel_original.split('\t1월\t')[1:3])
        excel_original_05 = "".join(excel_original.split('\t1월\t')[3:4])
        # excel_original_05 = "".join(re.split(r'(\t1월\t|\t1월정원\t)', excel_original.split('\t2024')[1])[7:11])
        # excel_original_05 = "".join(re.split(r'(\t1월\t|\t1월정원\t)', excel_original.split('\t2024')[1])[5:7])            
        excel_original_06 = "".join(excel_original.split('\t1월\t')[4:5])
        excel_original_07 = "".join(excel_original.split('\t1월\t')[5:7])
        
        # excel_original_08 = "".join(excel_original.split('\t1월\t')[7:9])
        # excel_original_09 = "".join(excel_original.split('\t1월\t')[9:11])
        # excel_original_10 = "".join(excel_original.split('\t1월\t')[10:]).split('평균단가')[1]


        if '202401' in str(excel_original.split('\t1월\t')[6]):
            excel_original_08 = "".join(excel_original.split('\t202401\t')[1].split('\t1월\t')[0])
            excel_original_09 = "".join(excel_original.split('\t1월\t')[7:9])
            excel_original_10 = "".join(excel_original.split('\t1월\t')[8:]).split('평균단가')[1]
        else:
            excel_original_08 = "".join(excel_original.split('\t1월\t')[7:9])
            excel_original_09 = "".join(excel_original.split('\t1월\t')[9:11])
            excel_original_10 = "".join(excel_original.split('\t1월\t')[10:]).split('평균단가')[1]
        '''








        
        try:
            str_err = self.compare(current_index)
            return

            if not str_err:
                print("엑셀 데이터가 확보되지 않았습니다. [" + str(current_index) + "번 표]")

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(error_details)
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] Compare 오류: " + str(current_index) + "번 표\n")
                f.write(f"{error_details}\n\n")        
                QMessageBox.information(self, "RPA 오류: " + str(current_index) + "번 표", "엑셀과 프로그램 데이터 비교 오류: " + str(current_index) + "번 표\n\n해결되지 않는 경우, log.txt를 경영정보부로 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
            
            print(f"\n[!] 오류: {e}")
            return


        
        self.win_verify = VerificationResultWindow(None)   # 1. 검증 창 인스턴스 생성
        
        result_text = "-------------------------------------\n"
        result_text += "    인건비 집계 정합성 검증    \n"
        result_text += "-------------------------------------\n\n"
        result_text += str_err
        
        self.win_verify.set_content(result_text)   # 3. 텍스트 박스에 내용 설정
        # self.notice('엑셀 탐색 완료')


        self.win_verify.show()
        self.win_verify.raise_()
        self.win_verify.activateWindow()


        # win_verify.exec_()



























    def text_table(self, r, c):
        return self.tabs.currentWidget().table.item(r, c).text()


    def table_str(self, p, r, c):

        if not self.tabs.widget(p-1).table.item(r, c) or self.tabs.widget(p-1).table.item(r, c).text() in ['', '-', 'n/a']:

            if (p in [5, 6]) or (p in [4, 7] and c != 14):
                return '0.00'
            elif (p in [1, 8]) or (p == 9 and c != 14) or (p in [3, 10] and c in [4, 5]) or (p == 2 and r not in [43, 44]):
                return '0'
            elif p == 2 and r in [43, 44]:
                return '0.0' # 0.000
            elif (p == 3 and c in [1, 2, 3]):
                return '0.0'
            else:
                return '0.0'
            return '0'
        return self.tabs.widget(p-1).table.item(r, c).text().replace('%', '')


    def excel_str(self, text, p, r, c):
        if not text or text.strip() in ['-', '']:
            if (p in [5, 6]) or (p in [4, 7] and c != 13):
                return '0.00'
            elif (p in [1, 8]) or (p == 9 and c != 13) or (p in [3, 10] and c in [4, 5]) or (p == 2 and r not in [43, 44]):
                return '0'
            elif p == 2 and r in [43, 44]:
                return '0.0' # 0.000
            elif (p == 3 and c in [1, 2, 3]):
                return '0.0'
            else:
                return '0.0'
        return(text.replace('%', '').replace('△', '-'))






    def rpa(self, current_index):        

        import warnings
        warnings.filterwarnings("ignore", category=UserWarning, module="pywinauto")

        import pygetwindow as gw
        from pywinauto import Application
        import pywinauto.win32functions as win32functions
        import subprocess
        import keyboard
        from pynput.mouse import Controller, Button
        import time

        global excel_temp, excel_original



        if current_index == 1:

            open_found = False

            import win32gui

            for item in gw.getAllWindows():
                if '인건비' in item.title and win32gui.GetClassName(item._hWnd) == 'XLMAIN':
                    win = item
                    self.notice('엑셀 탐색 시작')

                    if win.isMinimized:
                        win.restore()
                    
                    app = Application().connect(handle=win._hWnd)
                    target_win = app.window(handle=win._hWnd)

                    try:
                        target_win.set_focus()
                    except Exception:
                        win32functions.ShowWindow(win._hWnd, 9)
                        win32functions.SetForegroundWindow(win._hWnd)

                    open_found = True
                    break
                    # time.sleep(0.3)


            if not open_found:

                import win32com.client as win32
                import win32clipboard
                
                # PyQt5 앱 실행 (이미 앱이 실행 중이면 QApplication.instance() 사용)
                app = QApplication.instance() or QApplication(sys.argv)

                selected_file, _ = QFileDialog.getOpenFileName(None, "엑셀 파일을 선택하세요", "", "Excel Files (*.xlsx *.xls *.xlsm)")

                if not selected_file:
                    print("파일 선택이 취소되었습니다.")
                    sys.exit()
                    return 'Excel'


                excel = win32.Dispatch("Excel.Application")
                excel.Visible = False

                file_path = os.path.abspath(selected_file)
                wb = excel.Workbooks.Open(file_path, False, True)
                # wb = excel.Workbooks.Open(file_path, False, True, None, '0025')

                list_all = []
                str_all = ""

                cnt = 0

                list_stop = ["(2)-1. 임금관련 세부자료", "계량관리업무비"]

                for sheet in wb.Sheets:
                    flag_stop = False
                    for word in list_stop:
                        if sheet.UsedRange.Find(word):
                            flag_stop = True
                            break
                    if flag_stop:
                        continue

                    sheet.UsedRange.Copy()
                    excel_original += pyperclip.paste()
                    excel_original += '_$$$$$_'
                    time.sleep(1)
                    
                                        
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.CloseClipboard()

                excel_original = excel_original.replace(' ', '')
                

                    
                wb.Close(False)
                excel.Quit()


                return
                


            app = Application().connect(handle=win._hWnd)
            target_win = app.window(handle=win._hWnd)

            try:
                target_win.set_focus()
            except Exception:
                win32functions.ShowWindow(win._hWnd, 9)
                win32functions.SetForegroundWindow(win._hWnd)
                time.sleep(0.3)
                
            keyboard.press_and_release('win + up')
            for _ in range(12): keyboard.press_and_release('ctrl + pageup')
            time.sleep(0.3)

        time.sleep(0.1)

        if current_index != 1:
            keyboard.press_and_release('ctrl + pagedown')



        import ctypes
                
        # 클립보드 조작을 위한 Windows API 상수
        user32 = ctypes.windll.user32
                
        for _ in range(3): # 실패 대비 3회 재시도
            try:
                # 1. 클립보드 열기 시도 (None은 현재 프로세스가 소유권을 가짐을 의미)
                if user32.OpenClipboard(None):
                    user32.EmptyClipboard()   # 2. 강제로 비우기
                    user32.CloseClipboard()   # 3. 반드시 닫아줘야 다른 작업 가능
            except Exception as e:
                time.sleep(0.1)
        time.sleep(0.3)

        mouse = Controller()
        mouse.position = (1500, 880)
        mouse.click(Button.left, 1)
        time.sleep(0.1)
        
        keyboard.press_and_release('ctrl + a')
        time.sleep(0.1)
        keyboard.press_and_release('ctrl + a')       
        keyboard.press_and_release('ctrl + c')


        from PyQt5.QtCore import QThread

        if current_index == 1:
            pyperclip.copy("")
            excel_temp = ""
            
            QThread.msleep(1000)
            for _ in range(10):
                try:
                    excel_temp = pyperclip.paste()
                    if excel_temp:
                        excel_temp += '_$$$$$_'
                        break  # 데이터를 가져오면 루프 탈출
                except:
                    QThread.msleep(100)  # 에러 발생 시 0.1초 대기 후 재시도

            keyboard.press_and_release('right')
            keyboard.press_and_release('esc')

            if not excel_temp:
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] 엑셀 Sheet1 데이터를 확보하지 못했습니다.\n")

                screen = QApplication.primaryScreen()
                screenshot = screen.grabWindow(0) # 전체 화면 캡처
                screenshot.save("log.jpg", "jpg")

                QMessageBox.information(self, "엑셀 Sheet1 데이터를 확보하지 못했습니다.", "(2) 인건비 집계\n\n엑셀 파일이 제대로 열렸는지 확인해주세요.\n엑셀 양식이 변경되었는지 확인해주세요.\n\n해결되지 않는 경우, log.txt, log.jpg 를 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
                return "excel_original_no"

            return 'open_found'



        if current_index != 1:

            pyperclip.copy("")
            excel_temp = ""

            QThread.msleep(1000)
            for _ in range(10):
                try:
                    excel_temp = pyperclip.paste()
                    if excel_temp:
                        excel_temp += '_$$$$$_'
                        break  # 데이터를 가져오면 루프 탈출
                except:
                    QThread.msleep(100)   # 에러 발생 시 0.1초 대기 후 재시도
                    

            if not excel_temp:
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] 엑셀 Sheet1 데이터를 확보하지 못했습니다.\n")
                screen = QApplication.primaryScreen()
                screenshot = screen.grabWindow(0) # 전체 화면 캡처
                screenshot.save("log.jpg", "jpg")
                QMessageBox.information(self, "엑셀 Sheet" + str(current_index) + " 데이터를 확보하지 못했습니다.", "엑셀 Sheet" + str(current_index) + "\n\n엑셀 파일이 제대로 열렸는지 확인해주세요.\n엑셀 양식이 변경되었는지 확인해주세요.\n\n해결되지 않는 경우, log.txt, log.jpg 를 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
                return "excel_original_no"

            keyboard.press_and_release('right')
            keyboard.press_and_release('esc')

        return
            










        

    def compare(self, current_index):

        global excel_original_01, excel_original_02, excel_original_03, excel_original_04, excel_original_05, excel_original_06, excel_original_07, excel_original_08, excel_original_09, excel_original_10
        global excel_original_11, excel_original_12, excel_original_13, excel_original_14, excel_original_18
        global str_err

        str_err = ''
        str_err_total = ''
        
        table = self.tabs.currentWidget().table

        if 1==1 or current_index == 1:
            current_index = 1


                
            if year == '2026':


                list_title_01 = ['기본급', '인센티브 상여금', '그 외 상여금', '법정수당', '해외근무수당', '그 외 제수당', '퇴직급여(명예퇴직금 포함)', '임원 인건비', '비상임이사 인건비',
                             '인상률 제외 인건비', '기타항목', '급료,임금,제수당 소계ⓐ',  '사내근로복지기금출연금', '국민연금사용자부담분',
                             '건강보험사용자부담분', '고용보험사용자부담분', '산재보험료사용자부담분', '급식비', '교통보조비', '자가운전보조금', '학자보조금','건강진단비',
                             '선택적복지', '행사비', '포상품(비)', '기념품(비)', '격려품(비)', '장기근속관련 비용', '육아보조비 및 출산장려금', '자기계발비', '특별근로의 대가',
                             '피복비', '경로효친비', '통신비', '축하금/조의금', '기타 항목', '복리후생비 소계ⓑ', '일반 급여 (1)', '인센티브 상여금', '순액', '청년인턴 급여 (2)', '인센티브 상여금', '순액', '무기계약직 급여 (3)',
                             '인센티브 상여금', '순액', '소계 ⓒ=(1)+(2)+(3)', '인건비 총계: ⓓ=ⓐ+ⓑ+ⓒ', '인센티브 상여금 ⓔ=ⓔ-1+ⓔ-2', '인센티브 전환금 (ⓔ-1)', '인센티브 추가금 (ⓔ-2)', '인건비 해당금액 : ⓓ-ⓔ']


                list_keyword = ['기본', '인센', '그외상여', '법정', '해외', '그외제수', '퇴직급여', '임원', '비상임', '제외', '기타', '급료', '근로', '국민', '건강보험', '고용', '산재', '급식', '교통', '운전', '학자', '건강진단', '선택', '행사', '포상', '기념',
                                '격려', '장기', '육아', '자기', '특별', '피복', '경로', '통신', '축하', '기타', '복리', '일반', '상여', '순액', '청년', '상여', '순액', '무기', '상여', '순액', '소계', '인건비', '상여', '전환', '추가', '해당']



            if year == '2025':

                list_title_01 = ['기본급', '인센티브 상여금', '그 외 상여금', '법정수당', '해외근무수당', '그 외 제수당', '퇴직급여(명예퇴직금 포함)', '임원 인건비', '비상임이사 인건비',
                                 '인상률 제외 인건비', '기타항목', '급료,임금,제수당 소계ⓐ',  '사내근로복지기금출연금', '국민연금사용자부담분',
                                 '건강보험사용자부담분', '고용보험사용자부담분', '산재보험료사용자부담분', '급식비', '교통보조비', '자가운전보조금', '학자보조금','건강진단비',
                                 '선택적복지', '행사비', '포상품(비)', '기념품(비)', '격려품(비)', '장기근속관련 비용', '육아보조비 및 출산장려금', '자기계발비', '특별근로의 대가',
                                 '피복비', '경로효친비', '통신비', '축하금/조의금', '기타 항목', '복리후생비 소계ⓑ', '일반 급여 (1)', '인센티브 상여금', '순액', '청년인턴 급여 (2)', '인센티브 상여금', '순액', '무기계약직 급여 (3)',
                                 '인센티브 상여금', '순액', '소계 ⓒ=(1)+(2)+(3)', '인건비 총계: ⓓ=ⓐ+ⓑ+ⓒ', '인센티브 상여금 ⓔ=ⓔ-1+ⓔ-2', '인센티브 전환금 (ⓔ-1)', '인센티브 추가금 (ⓔ-2)', '인건비 해당금액 : ⓓ-ⓔ']
                       
                list_keyword = ['기본', '인센', '그외상여', '법정', '해외', '그외제수', '퇴직급여', '임원', '비상임', '제외', '기타', '급료', '사내근로', '국민', '건강보험', '고용', '산재', '급식', '교통', '운전', '학자', '건강진단', '선택', '행사', '포상', '기념',
                                '격려', '장기', '육아', '자기', '특별', '피복', '경로', '통신', '축하', '기타', '복리', '일반', '상여', '순액', '청년', '상여', '순액', '무기', '상여', '순액', '소계', '인건비', '상여', '전환', '추가', '해당']

                readonly_rows = [11, 36, 37, 40, 43, 46, 47, 48, 51]


            if year in ['2024', '2023']:

                list_title_01 = ['기본급', '인센티브 상여금', '그 외 상여금', '법정수당', '해외근무수당', '그 외 제수당', '퇴직급여(명예퇴직금 포함)', '임원 인건비', '비상임이사 인건비',
                                 '인상률 제외 인건비(통상)', '인상률 제외 인건비(기타)', '기타항목', '급료,임금,제수당 소계ⓐ',  '사내근로복지기금출연금', '국민연금사용자부담분',
                                 '건강보험사용자부담분', '고용보험사용자부담분', '산재보험료사용자부담분', '급식비', '교통보조비', '자가운전보조금', '학자보조금','건강진단비',
                                 '선택적복지', '행사비', '포상품(비)', '기념품(비)', '격려품(비)', '장기근속관련 비용', '육아보조비 및 출산장려금', '자기계발비', '특별근로의 대가',
                                 '피복비', '경로효친비', '통신비', '축하금/조의금', '기타 항목', '복리후생비 소계ⓑ', '일반 급여 (1)', '인센티브 상여금', '순액', '청년인턴 급여 (2)', '인센티브 상여금', '순액', '무기계약직 급여 (3)',
                                 '인센티브 상여금', '순액', '소계 ⓒ=(1)+(2)+(3)', '인건비 총계: ⓓ=ⓐ+ⓑ+ⓒ', '인센티브 상여금 ⓔ=ⓔ-1+ⓔ-2', '인센티브 전환금 (ⓔ-1)', '인센티브 추가금 (ⓔ-2)', '인건비 해당금액 : ⓓ-ⓔ']
                       
                list_keyword = ['급료', '인센', '그외상여', '법정', '해외', '그외제수', '퇴직급여', '임원', '비상임', '통상', '기타제외', '기타', '급료', '사내근로', '국민', '건강보험', '고용', '산재', '급식', '교통', '운전', '학자', '건강진단', '선택', '행사', '포상', '기념',
                                '격려', '장기', '육아', '자기', '특별', '피복', '경로', '통신', '축하', '기타', '복리', '일반', '상여', '순액', '청년', '상여', '순액', '무기', '상여', '순액', '소계', '인건비', '상여', '전환', '추가', '해당']

                readonly_rows = [12, 37, 38, 41, 44, 47, 48, 49, 52]







            flag_gibon = False

            if not list_years2:    # 최근연도의 판관비 열 번호 (col_gibon)
                for item in excel_original_01.split('\r\n'):
                    col_gibon = 0
                    for item_col in item.split('\t'):
                        if '판관비' in item_col:
                            flag_gibon = True
                            break
                        col_gibon += 1
                    if flag_gibon:
                        break
            else:        
                for item in excel_original_01.split('\r\n'):
                    col_gibon = 0
                    for item_col in item.split('\t'):
                        if max(list_years2) in item_col:
                            flag_gibon = True
                            break
                        col_gibon += 1
                    if flag_gibon:
                        break







            if '판관비' in excel_original_01[:300]:
                list_temp = excel_original_01.split('판관비')[1:]
                list_temp = '판관비'.join(list_temp)
            elif '인건비항목' in excel_original_01[:300]:
                list_temp = excel_original_01.split('인건비항목')[1:]
                list_temp = '인건비항목'.join(list_temp)
            else:
                list_temp = excel_original_01.split('20')[1:]
                list_temp = '20'.join(list_temp)
                
            list_temp = list_temp.replace('급료\r\n', '').replace('임금\r\n', '')
            if '인센' not in list_temp:
                if '상여금' in list_temp:
                    list_temp = list_temp.replace('상여금', '상여금 인센티브')
            if '법정' not in list_temp and '해외근무' not in list_temp:
                if '제수당' in list_temp:
                    list_temp = list_temp.replace('제수당', '제수당 법정수당')



            list_temp = list_temp.split('\r\n')
            list_temp_clean = []
            for item in list_temp:
                if item.strip():
                    list_temp_clean.append(item)
            list_temp = list_temp_clean
            list_temp = list_temp[1:len(list_temp)-1]



            matches = re.findall(r'20\d+.*?\t+.*?20\d+', excel_original_01.replace('\t\t\t\t\t\t\t\t\t', '')[:188])
            if matches:
                col_gibon_width = len(matches[0].split('\t'))-2
            else:
                col_gibon_width = 5




            '''
            col_5 = 5
            if list_years2 and col_gibon_width != 5: # (2) 에서 판관비 등 5열이 없으면 col_5 =1 (1개 열만 판관비로 입력)
                col_5 = 1
                list_clean = []
                for item in list_temp:
                    list_clean.append(item.split('\t')[:col_gibon+1])

                for i in range(len(list_clean[0])):
                    if '제수당' in list_clean[0][i]:
                        list_clean[0][i] = ""

                list_temp = list_clean
            else:
                list_clean = []
                for item in list_temp:
                    list_clean.append(item.split('\t')[:col_gibon+5])
                list_temp = list_clean
            '''



            col_5 = 5
            if list_years2 and col_gibon_width != 5: # (2) 에서 판관비 등 5열이 없으면 col_5 =1 (1개 열만 판관비로 입력)
                col_5 = 1

            list_sogye = []
            for item in list_temp:
                if item.startswith('\t\t\t\t\t') or item.startswith('\t\t\t(가)\t') or item.startswith('\t\t\t(바)\t'):
                    continue
                if '소계' in str(item):
                    list_sogye.append(item.split('\t')[col_gibon:col_gibon+col_5+1])




            # print(excel_original_01.split('추가금')[1].split('\r\n')[1])
            list_hedang = excel_original_01.split('추가금')[1].split('\r\n')

            list_hedang_temp = []
            for item in list_hedang:
                if item.startswith('\t\t\t\t\t') or item.startswith('\t\t\t(가)\t') or item.startswith('\t\t\t(바)\t'):
                    continue
                list_hedang_temp.append(item)
            list_hedang = list_hedang_temp[1].split('\t')[col_gibon:col_gibon+col_5+1]



            global list_s1_01, list_s1_02, list_s1_03


            if col_5 == 5:

                list_total = list_s1_01
                list_total.append(list_sogye[0])
                list_total.extend(list_s1_02)
                list_total.append(list_sogye[1])
                list_total.extend(list_s1_03)
                list_total.append(list_hedang)


            if col_5 == 1:
                list_temp = []
                for item in list_s1_01:
                    list_temp.append([item[0], '', '', '', '', item[0]])
                list_s1_01 = list_temp

                list_temp = []
                for item in list_s1_02:
                    list_temp.append([item[0], '', '', '', '', item[0]])
                list_s1_02 = list_temp

                list_temp = []
                for item in list_s1_03:
                    list_temp.append([item[0], '', '', '', '', item[0]])
                list_s1_03 = list_temp


                list_total = list_s1_01
                list_total.append([list_sogye[0][0], '', '', '', '', list_sogye[0][0]])
                list_total.extend(list_s1_02)
                list_total.append([list_sogye[1][0], '', '', '', '', list_sogye[1][0]])
                list_total.extend(list_s1_03)
                list_total.append([list_hedang[0], '', '', '', '', list_hedang[0]])




            str_err += '(2) 인건비 집계\n\n'
            str_err += '급료임금제수당\n'
            str_err += f"{'판영제타이 합':>21}{'판관비':>35}{'영업외':>36}{'제조원가':>34}{'타계정대체':>34}{'이익잉여금':>34}{'합계':>35}\n"

            cnt_wrong = 0



            
            for i in range (0, len(list_title_01)):

                if year in ['2025']:
                    if i == 12: str_err += "\n복리후생비\n" + f"{'판영제타이 합':>21}{'판관비':>35}{'영업외':>36}{'제조원가':>34}{'타계정대체':>34}{'이익잉여금':>34}{'합계':>35}\n"
                    if i == 38: str_err += "\n잡급\n" + f"{'판영제타이 합':>21}{'판관비':>35}{'영업외':>36}{'제조원가':>34}{'타계정대체':>34}{'이익잉여금':>34}{'합계':>35}\n"

                if year in ['2024', '2023']:
                    if i == 13: str_err += "\n복리후생비\n" + f"{'판영제타이 합':>21}{'판관비':>35}{'영업외':>36}{'제조원가':>34}{'타계정대체':>34}{'이익잉여금':>34}{'합계':>35}\n"
                    if i == 39: str_err += "\n잡급\n" + f"{'판영제타이 합':>21}{'판관비':>35}{'영업외':>36}{'제조원가':>34}{'타계정대체':>34}{'이익잉여금':>34}{'합계':>35}\n"



                str_err += list_title_01[i][:6] + '\t   '


                list_temp = []
                for j in range(0, 6):

                    if self.excel_str(list_total[i][j], current_index, i, j).replace(',', '') == self.table_str(current_index, i, j+1).replace(',', ''):
                        str_err += 'O '
                        list_temp.append(' ' * 38)
                        
                    else:
                        str_err += 'X '
                        cnt_wrong += 1
                        list_temp.append((self.excel_str(list_total[i][j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(38))



                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(2) 인건비 집계', '(2) 인건비 집계\t불일치: [' + str(cnt_wrong) + '/318]')
            str_err_total += '(2) 인건비 집계\t\t불일치: [' + str(cnt_wrong) + '/318]\n'
            str_err += '\n\n\n'







        if 1==1 or current_index == 2:
            current_index = 2
            excel_original_02 = excel_original_02.replace(' ', '')

            if year == '2026':
                list_title_02 = ['1.인센티브상여금을제외한인건비총액', 'a.판관비로처리한인건비', 'b.영업외비용으로처리한인건비', 'c.제조원가로처리한인건비', 'd.타계정대체로처리한인건비', 'e.이익잉여금의증감으로처리한인건비', '소계:(A)=a+b+c+d+e',
                                 '2.총인건비인상률계산에서제외(조정)되는인건비', 'f.퇴직급여(명예퇴직금포함)', 'g.임원인건비', 'h.비상임이사인건비',
                                 'i.기타제외인건비', 'j.사내근로복지기금출연금', 'k.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)', 
                                 'l.공적보험사용자부담분', 'm.연월차수당등조정(㉠-㉡+㉢)', '-연월차수당등발생액(㉠)',
                                 '-연월차수당등지급액(㉡)', '-종업원저리대여금이자관련인건비(㉢)', 'n.저리,무상대여이익', 'o.지방이전관련직접인건비', 
                                 'p.법령에따른특수건강진단비', 'q.해외근무수당', 'r.직무발명보상금', 
                                 's.공무원수준내의자녀수당및출산격려금', 't.야간간호특별수당', 'u.비상진료체계운영에따른특별수당등',
                                 'v. 통상임금 판단기준 변경 판례의 영향으로 인한 법정수당 증가분(2024년 귀속분)', '소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s+t+u+v+w', 
                                 '3.실집행액기준총인건비발생액(C)=(A)-(B)', '4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)',
                                 '5.별도직군승진시기차이에따른인건비효과조정(E)', '6.초임직급정원변동에따른인건비효과조정(F)', 
                                 '7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)', '8.생산량증가25년추가지급인건비영향제거(H)', 
                                 '9.최저임금지급직원에대한인건비효과조정(I)', '10.파업등에따른인건비효과조정(J)', '11.통상임금판단기준변경판례의영향으로인한법정수당증가분(2025년귀속분)(K)<주30>', 
                                  '12.(C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)+(K)+(L)', '13.총인건비인상률가이드라인에따른총인건비상한액',
                                 '24년도총인건비상한액준수', '24년도총인건비상한액미준수', '24년도총인건비인상률가이드라인=2.5%)', '23년도총인건비인상률준수','23년도총인건비인상률미준수'
                                 ]



            if year == '2025':
                list_title_02 = [
                    '1.인센티브상여금을제외한인건비총액', 'a.판관비로처리한인건비', 'b.영업외비용으로처리한인건비', 'c.제조원가로처리한인건비', 
                    'd.타계정대체로처리한인건비', 'e.이익잉여금의증감으로처리한인건비', '소계:(A)=a+b+c+d+e', 
                    '2.총인건비인상률계산에서제외(조정)되는인건비', 'f.퇴직급여(명예퇴직금포함)', 'g.임원인건비', 'h.비상임이사인건비',
                    'i.기타제외인건비', 'j.사내근로복지기금출연금', 'k.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)', 
                    'l.공적보험사용자부담분', 'm.연월차수당등조정(㉠-㉡+㉢)', '-연월차수당등발생액(㉠)',
                    '-연월차수당등지급액(㉡)', '-종업원저리대여금이자관련인건비(㉢)', 'n.저리,무상대여이익', 'o.지방이전관련직접인건비', 
                    'p.법령에따른특수건강진단비', 'q.해외근무수당', 'r.직무발명보상금', 
                    's.공무원수준내의자녀수당및출산격려금', 't.야간간호특별수당', 'u.비상진료체계운영에따른특별수당등',
                    'v.통상임금판단기준변경판례의영향으로인한법정수당증가분(2024년귀속분)', '소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s+t+u+v+w', 
                    '3.실집행액기준총인건비발생액(C)=(A)-(B)', '4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)',
                    '5.별도직군승진시기차이에따른인건비효과조정(E)', '6.초임직급정원변동에따른인건비효과조정(F)', 
                    '7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)', '8.생산량증가25년추가지급인건비영향제거(H)', 
                    '9.최저임금지급직원에대한인건비효과조정(I)', '10.파업등에따른인건비효과조정(J)', '11.통상임금판단기준변경판례의영향으로인한법정수당증가분(2025년귀속분)(K)<주30>', 
                    '12.(C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)-(K)'
                ]


            if year == '2024':

                list_title_02 = [
                    '1.인센티브상여금을제외한인건비총액', 'a.판관비로처리한인건비', 'b.영업외비용으로처리한인건비', 'c.제조원가로처리한인건비', 
                    'd.타계정대체로처리한인건비', 'e.이익잉여금의증감으로처리한인건비', '소계:(A)=a+b+c+d+e', 
                    '2.총인건비인상률계산에서제외(조정)되는인건비', 'f.퇴직급여(명예퇴직금포함)', 'g.임원인건비', 'h.비상임이사인건비',
                    'i.통상제외인건비', 'i.기타제외인건비', 'j.사내근로복지기금출연금', 'k.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)', 
                    'l.공적보험사용자부담분', 'm.연월차수당등조정(㉠-㉡+㉢)', '-연월차수당등발생액(㉠)',
                    '-연월차수당등지급액(㉡)', '-종업원저리대여금이자관련인건비(㉢)', 'n저리,무상대여이익', 'o.지방이전관련직접인건비', 
                    'p.법령에따른특수건강진단비', 'q.해외근무수당', 'r.직무발명보상금', 
                    's.공무원수준내의자녀수당및출산격려금', 't.야간간호특별수당', 'u.비상진료체계운영에따른특별수당등',
                    'v.통상임금판단기준변경판례의영향으로인한법정수당증가분(2024년귀속분)', '소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s+t+u+v+w', 
                    '3.실집행액기준총인건비발생액(C)=(A)-(B)', '4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)',
                    '5.별도직군승진시기차이에따른인건비효과조정(E)', '6.초임직급정원변동에따른인건비효과조정(F)', 
                    '7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)', '8.생산량증가25년추가지급인건비영향제거(H)', 
                    '9.최저임금지급직원에대한인건비효과조정(I)', '10.파업등에따른인건비효과조정(J)', '11.코로나19로인한휴업의인건비효과조정(K)', 
                    '12.(C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)+(K)+(L)'
                ]


            if year == '2023':
                list_title_02 = [
                    '1.인센티브상여금을제외한인건비총액', 'a.판관비로처리한인건비', 'b.영업외비용으로처리한인건비', 'c.제조원가로처리한인건비', 
                    'd.타계정대체로처리한인건비', 'e.이익잉여금의증감으로처리한인건비', '소계:(A)=a+b+c+d+e', 
                    '2.총인건비인상률계산에서제외(조정)되는인건비', 'f.퇴직급여(명예퇴직금포함)', 'g.임원인건비', 'h.비상임이사인건비',
                    'i.통상제외인건비', 'i.기타제외인건비', 'j.사내근로복지기금출연금', 'k.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)', 
                    'l.공적보험사용자부담분', 'm.연월차수당등조정(㉠-㉡+㉢)', '-연월차수당등발생액(㉠)',
                    '-연월차수당등지급액(㉡)', '-종업원저리대여금이자관련인건비(㉢)', 'n.저리,무상대여이익', 'o.지방이전관련직접인건비', 
                    'p.법령에따른특수건강진단비', 'q.코로나19대응을위한시간외근로수당등', 'r.해외근무수당', 's.직무발명보상금', 
                    '소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s', 
                    '3.실집행액기준총인건비발생액(C)=(A)-(B)', '4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)',
                    '5.별도직군승진시기차이에따른인건비효과조정(E)', '6.초임직급정원변동에따른인건비효과조정(F)', 
                    '7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)', '8.생산량증가25년추가지급인건비영향제거(H)', 
                    '9.최저임금지급직원에대한인건비효과조정(I)', '10.파업등에따른인건비효과조정(J)', 
                    '11.코로나19로인한휴업의인건비효과조정(K)',
                    '12.(C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)+(K)'
                ]








            global list_s2_01, list_s2_02, list_s2_03, list_s2_04


            for item in excel_original_02.split('\r\n'):
                col_temp = 0
                flag_col = False
                for item_col in item.split('\t'):
                    if max(list_years3) in item_col:
                        flag_col = True
                        break
                    col_temp += 1   # 엑셀에서 몇 번째 열부터 금액 시작인지
                if flag_col:
                    break

            if len(list_years3) > 3: cnt_col = 3   # (3) ['2025', '2024', '2023'] 몇개 연도인지
            else: cnt_col = len(list_years3)







            list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('잉여금')[1].split('총인건비')[0].split('\r\n')   # 소계
            list_clean = []
            for item in list_temp:
                if item.startswith('\t\t\t\t\t') or item.startswith('\t\t\t(가)\t') or item.startswith('\t\t\t(바)\t'):
                    continue
                list_clean.append(item)
            list_temp = list_clean
            list_sogye01 = list_temp[1].split('\t')[col_temp:col_temp+cnt_col]


            list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('공적')[1].split('지급액')[0].split('\r\n')   # 연월차 소계
            list_clean = []
            for item in list_temp:
                if item.startswith('\t\t\t\t\t') or item.startswith('\t\t\t(가)\t') or item.startswith('\t\t\t(바)\t'):
                    continue
                list_clean.append(item)
            list_temp = list_clean
            list_sogye02 = list_temp[1].split('\t')[col_temp:col_temp+cnt_col]





            list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('해외')[1].split('실집행')[0].split('\r\n')   # 소계
            list_clean = []
            for item in list_temp:
                if '소계' in item:
                    list_clean.append(item)
                    break
            list_temp = list_clean
            list_sogye03 = list_temp[0].split('\t')[col_temp:col_temp+cnt_col]




            list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('소계')[2].split('연도별')[0].split('\r\n')   # 소계
            list_clean = []
            for item in list_temp:
                if '실집행' in item:
                    list_clean.append(item)
                    break
            list_temp = list_clean
            list_sogye03_sil = list_temp[0].split('\t')[col_temp:col_temp+cnt_col]





            list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('파업')[1].split('상한액')[0].split('\r\n')   # 소계
            list_clean = []
            for item in list_temp:
                if item.startswith('\t\t\t\t\t') or item.startswith('\t\t\t(가)\t') or item.startswith('\t\t\t(바)\t'):
                    continue
                list_clean.append(item)
            list_temp = list_clean
            list_sogye04 = list_temp[2].split('\t')[col_temp:col_temp+cnt_col]


            list_sogye05 = []
            list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('상한액')[1].split('인상률산출')[0].split('\r\n')   # 소계
            list_temp = list_temp[1:]
            list_clean = []
            for item in list_temp:
                if item.startswith('\t\t\t\t\t') or item.startswith('\t\t\t(가)\t') or item.startswith('\t\t\t(바)\t'):
                    continue
                list_clean.append(item.replace('\t-\t', '\t\t').replace(')-(', '').replace('n/a', '').replace('na', '').replace('Ⅰ', '').replace('Ⅲ', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('/', '').replace('%', ''))
            list_temp = list_clean[:2]
            list_sogye05.extend(list_temp)

            list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('인상률산출')[1].split('\r\n')   # 소계
            list_temp = list_temp[1:]
            list_clean = []
            for item in list_temp:
                if item.startswith('\t\t\t\t\t') or item.startswith('\t\t\t(가)\t') or item.startswith('\t\t\t(바)\t'):
                    continue
                list_clean.append(item.replace('\t-\t', '\t\t').replace(')-(', '').replace('n/a', '').replace('na', '').replace('Ⅰ', '').replace('Ⅲ', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('/', '').replace('%', ''))
            list_temp = list_clean[:2]
            list_sogye05.extend(list_temp)

            
            list_temp = []
            for item in list_sogye05:
                list_temp.append(item.replace('\t-\t', '\t\t').replace(')-(', '').replace('n/a', '').replace('na', '').replace('Ⅰ', '').replace('Ⅲ', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('/', '').replace('%', '').split('\t')[col_temp:col_temp+cnt_col])

            list_sogye05 = list_temp   # 총인건비 상한액, 인상률 가이드라인 준수, 미준수



            list_null = []
            for i in range(cnt_col):
                list_null.append('')


            list_total = []
            list_total.append(list_null)
            list_total.extend(list_s2_01)
            list_total.append(list_sogye01)
            list_total.append(list_null)            
            list_total.extend(list_s2_02)
            list_total.append(list_sogye02)
            list_total.extend(list_s2_03)
            list_total.append(list_sogye03)
            list_total.append(list_sogye03_sil)
            list_total.extend(list_s2_04)
            list_total.append(list_sogye04)









                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
            str_err += '(3) 총인건비 인상률 지표의 점수계산\n\n'
            str_err += '실집행액 기준 총인건비 발생액 산출\n\n'



            w_h = 28 
            w_d = 35
            str_err += f"{'5 4 3':>28}{'2025':>39}{'2024':>41}{'2023':>39}\n"

            cnt_wrong = 0

            global final_matrix

            # for i in range (0, 45):
            for i in range (0, len(list_total)):
                if year in ['2025']:
                    if i in [7, 29, 30]: str_err += '\n'
                    if i == 30: str_err += '\n전년대비 조정된 총인건비 발생액 산출\n\n' + f"{'5 4 3':>28}{'2025':>39}{'2024':>41}{'2023':>39}\n"
                    if i == 39: str_err += '\n\n당해연도 총인건비 인상률 계산\n\n' + f"{'5 4 3':>28}{'2025':>39}{'2024':>41}{'2023':>39}\n"
                if year in ['2024', '2023']:
                    if i in [7, 30, 31]: str_err += '\n'
                    if i == 31: str_err += '\n전년대비 조정된 총인건비 발생액 산출\n\n' + f"{'5 4 3':>28}{'2025':>39}{'2024':>41}{'2023':>39}\n"
                    if i == 40: str_err += '\n\n당해연도 총인건비 인상률 계산\n\n' + f"{'5 4 3':>28}{'2025':>39}{'2024':>41}{'2023':>39}\n"




                if year in ['2025']:
                    if i in [9, 19]:
                        str_err += list_title_02[i][:8] + '\t'
                    elif i in [6, 28]:
                        str_err += list_title_02[i][:12] + '\t'
                    elif i in [38]:
                        str_err += list_title_02[i][:8] + '\t'
                    else:
                        str_err += list_title_02[i][:8] + '\t'


                if year in ['2024', '2023']:
                    if i in [9, 20]:
                        str_err += list_title_02[i][:8] + '\t'
                    elif i in [6, 29]:
                        str_err += list_title_02[i][:12] + '\t'
                    elif i in [39]:
                        str_err += list_title_02[i][:12] + '\t'
                    else:
                        str_err += list_title_02[i][:8] + '\t'







                        


                if i in [0, 7]:
                    str_err += '\n'
                    continue


                list_temp = []


                list_temp = []                
                for j in range(0, len(list_total[0])): ####### (1, 4)

                    if year in ['2025']:
                        if (i in [30, 31, 32] and j == 0) or (i in [34] and j in [1, 2]):
                            str_err += '  '
                            list_temp.append(' ' * 41)
                            continue

                    if year in ['2024', '2023']:
                        if (i in [31, 32, 33] and j == 0) or (i in [35] and j in [1, 2]):
                            str_err += '  '
                            list_temp.append(' ' * 41)
                            continue




                    if self.excel_str(list_total[i][j], current_index, i, j).replace(',', '') == self.table_str(current_index, i, j+2).replace(',', ''):
                        str_err += 'O '
                        list_temp.append(' ' * 41)

                    else:
                        str_err += 'X '
                        cnt_wrong += 1
                        list_temp.append((self.excel_str(           str( f"{int(list_total[i][j]) if list_total[i][j] else 0:,}" )   , current_index, i, j) + f"__{self.table_str(current_index, i, j+2)}").rjust(41))



                str_err = str_err[:-1] + ''.join(list_temp) + '\n'





            if year in ['2025']: list_row = [40, 41, 43, 44]
            if year in ['2024']: list_row = [41, 42, 44, 45]
            if year in ['2023']: list_row = [38, 39, 41, 42]
            list_sogye05_title = ['24년상한액준수', '24년상한액미준수', '24년인상률준수','24년인상률미준수']



            
            list_temp = []  
            str_err += '13.(1)준수'[:8] + '\t'
            for j in range (0, len(list_sogye05[0])):
                if (j == 0):
                    str_err += '  '
                    list_temp.append(' ' * 41)
                    continue
                if self.excel_str(list_sogye05[0][j], current_index, 0, j).replace(',', '') == self.table_str(current_index, list_row[0], j+2).replace(',', ''):
                    str_err += 'O '
                    list_temp.append(' ' * 41)
                else:
                    str_err += 'X '
                    cnt_wrong += 1
                    list_temp.append((self.excel_str(           str( f"{float(list_sogye05[0][j].replace('%', '')) if list_sogye05[0][j] else 0:,}" )   , current_index, 0, j) + f"__{self.table_str(current_index, list_row[0], j+2)}").rjust(41))
            str_err = str_err[:-1] + ''.join(list_temp) + '\n'


            list_temp = []  
            str_err += '13.(2)미준수'[:8] + '\t'
            for j in range (0, len(list_sogye05[0])):
                if (j == 0):
                    str_err += '  '
                    list_temp.append(' ' * 41)
                    continue                
                if self.excel_str(list_sogye05[1][j], current_index, 1, j).replace(',', '') == self.table_str(current_index, list_row[1], j+2).replace(',', ''):
                    str_err += 'O '
                    list_temp.append(' ' * 41)
                else:
                    str_err += 'X '
                    cnt_wrong += 1
                    list_temp.append((self.excel_str(           str( f"{float(list_sogye05[1][j].replace('%', '')) if list_sogye05[1][j] else 0:,}" )   , current_index, 1, j) + f"__{self.table_str(current_index, list_row[1], j+2)}").rjust(41))
            str_err = str_err[:-1] + ''.join(list_temp) + '\n'





            list_temp = []  
            str_err += '14.(1)준수'[:8] + '\t'
            for j in range (0, len(list_sogye05[0])):
                if (j == 1):
                    str_err += '  '
                    list_temp.append(' ' * 41)
                    continue                
                if self.excel_str(list_sogye05[2][j], current_index, 2, j).replace(',', '') == self.table_str(current_index, list_row[2], j+2).replace(',', ''):
                    str_err += ' O'
                    list_temp.append(' ' * 41)
                else:
                    str_err += ' X'
                    cnt_wrong += 1
                    list_temp.append((self.excel_str(           str( f"{float(list_sogye05[2][j].replace('%', '')) if list_sogye05[2][j] else 0:,}" )   , current_index, 2, j) + f"__{self.table_str(current_index, list_row[2], j+2)}").rjust(41))
            str_err = str_err[:-1] + ''.join(list_temp) + '\n'



            list_temp = []  
            str_err += '14.(2)미준수'[:8] + '\t'
            for j in range (0, len(list_sogye05[0])):
                if (j == 1):
                    str_err += '  '
                    list_temp.append(' ' * 41)
                    continue                
                if self.excel_str(list_sogye05[3][j], current_index, 3, j).replace(',', '') == self.table_str(current_index, list_row[3], j+2).replace(',', ''):
                    str_err += ' O'
                    list_temp.append(' ' * 41)
                else:
                    str_err += ' X'
                    cnt_wrong += 1
                    list_temp.append((self.excel_str(           str( f"{float(list_sogye05[3][j].replace('%', '')) if list_sogye05[3][j] else 0:,}" )   , current_index, 3, j) + f"__{self.table_str(current_index, list_row[3], j+2)}").rjust(41))
            str_err = str_err[:-1] + ''.join(list_temp) + '\n'










            if len(list_total[0]) == 2:
                str_err = str_err.replace('5 4 3', '5 4  ')
                str_err = str_err.replace('2023', '')

            print(str_err)





            return






            # print(next((w for w in excel_original_02.split('준수')[1].split('\r\n')[0].split('\t') if any(c.isdigit() for c in w)), ""))
            # print(next((w for w in excel_original_02.split('준수')[2].split('\r\n')[0].split('\t') if any(c.isdigit() for c in w)), ""))
            # print(next((w for w in excel_original_02.split('준수')[3].split('\r\n')[0].split('\t') if any(c.isdigit() for c in w)), ""))
            # print(next((w for w in excel_original_02.split('준수')[4].split('\r\n')[0].split('\t') if any(c.isdigit() for c in w)), ""))




            r_39 = excel_original_02.split('파업')[1].split('준수')[1].split('\r\n')[0].split('\t')
            r_40 = excel_original_02.split('파업')[1].split('준수')[2].split('\r\n')[0].split('\t')

            r_41 = excel_original_02.split('파업')[1].split('준수')[3].split('\r\n')[0].split('\t')
            r_42 = excel_original_02.split('파업')[1].split('준수')[4].split('\r\n')[0].split('\t')

            cnt_except = 0


            global valid_indices

            for i in range(len(r_39)-1, 0, -1):
                if i in valid_indices:
                    continue
                r_39.pop(i)
                r_40.pop(i)
                r_41.pop(i)
                r_42.pop(i)


            list_temp = []
            str_err += '13.상한액(1)준수' + '\t'
            if str(r_39[len(r_39)-(len(final_matrix[0])-2)]).replace(',', '') == self.table_str(current_index, 40, 3).replace(',', ''):
                str_err += '  O '
                list_temp.append(' ' * 41)
                list_temp.append(' ' * 41)
            else:
                str_err += '  X '
                cnt_wrong += 1
                list_temp.append(' ' * 41)
                list_temp.append((self.excel_str(str(r_39[len(r_39)-(len(final_matrix[0])-2)]), current_index, 40, 3) + f"__{self.table_str(current_index, 40, 3)}").rjust(41))
            str_err = str_err[:-1] + ''.join(list_temp) + '\n'



            list_temp = []

            if (str(r_40[len(r_40)-(len(final_matrix[0])-2)]).replace(',', '') in ['', '-', '0']) or ('Ⅲ' in str(r_40)):
                cnt_except += 1
            elif str(r_40[len(r_40)-(len(final_matrix[0])-2)]).replace(',', '') == self.table_str(current_index, 41, 3).replace(',', ''):
                str_err += '13.상한액(2)미준수' + '\t'
                str_err += '  O '
                list_temp.append(' ' * 41)
                list_temp.append(' ' * 41)
            else:
                str_err += '13.상한액(2)미준수' + '\t'
                str_err += '  X '
                cnt_wrong += 1
                list_temp.append(' ' * 41)


                if 'Ⅲ' in str(r_40):
                    list_temp.append((self.excel_str('0', current_index, 41, 3) + f"__{self.table_str(current_index, 41, 3)}").rjust(41))                    
                else:
                    list_temp.append((self.excel_str(str(r_40[len(r_40)-(len(final_matrix[0])-2)]), current_index, 41, 3) + f"__{self.table_str(current_index, 41, 3)}").rjust(41))
                

                '''
                str_err += 'O   '
                list_temp.append(' ' * 41)
                '''




                
            str_err = str_err[:-1] + ''.join(list_temp) + '\n'


            '''
            list_temp = []
            str_err += '14.가이드(1)준수' + '\t'
            if str(r_41[len(r_41)-(len(final_matrix[0])-1)]).replace('%', '') == self.table_str(current_index, 43, 2).replace(',', ''):   # 14.가이드(1)준수
                str_err += 'O   '
                list_temp.append(' ' * 41)
            else:
                str_err += 'X   '
                cnt_wrong += 1
                list_temp.append((self.excel_str(str(r_41[len(r_41)-(len(final_matrix[0])-1)]).replace('%', ''), current_index, 43, 2) + "%" + f"__{self.table_str(current_index, 43, 2)}%").rjust(41))
            str_err = str_err[:-1] + ''.join(list_temp) + '\n'


            list_temp = []
            if (str(r_42[len(r_42)-(len(final_matrix[0])-1)]).replace('%', '') in ['', '-', '0']) or ('Ⅲ' in str(r_42)):
                cnt_except+= 1
            elif str(r_42[len(r_42)-(len(final_matrix[0])-1)]).replace('%', '') == self.table_str(current_index, 44, 2).replace(',', ''):   # 14.가이드(2)미준수
                str_err += '14.가이드(2)미준수' + '\t'
                str_err += 'O   '
                list_temp.append(' ' * 41)
            else:
                str_err += '14.가이드(2)미준수' + '\t'
                str_err += 'X   '
                cnt_wrong += 1
                list_temp.append((self.excel_str(str(r_42[len(r_42)-(len(final_matrix[0])-1)]).replace('%', ''), current_index, 44, 2) + "%" + f"__{self.table_str(current_index, 44, 2)}%").rjust(41))        
            str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            '''



            list_temp = []
            str_err += '14.가이드(1)준수' + '\t'
            if str(r_41[len(r_41)-(len(final_matrix[0])-1)]).replace('%', '') == self.table_str(current_index, 43, 2).replace(',', ''):   # 14.가이드(1)준수
                str_err += 'O   '
                list_temp.append(' ' * 41)
            else:
                str_err += 'X   '
                cnt_wrong += 1
                list_temp.append((self.excel_str(str(r_41[len(r_41)-(len(final_matrix[0])-1)]).replace('%', ''), current_index, 43, 2) + f"__{self.table_str(current_index, 43, 2)}").rjust(41))
            str_err = str_err[:-1] + ''.join(list_temp) + '\n' 

            list_temp = []
            if (str(r_42[len(r_42)-(len(final_matrix[0])-1)]).replace('%', '') in ['', '-', '0']) or ('Ⅲ' in str(r_42)):
                cnt_except+= 1
            elif str(r_42[len(r_42)-(len(final_matrix[0])-1)]).replace('%', '') == self.table_str(current_index, 44, 2).replace(',', ''):   # 14.가이드(2)미준수
                str_err += '14.가이드(2)미준수' + '\t'
                str_err += 'O   '
                list_temp.append(' ' * 41)
            else:
                str_err += '14.가이드(2)미준수' + '\t'
                str_err += 'X   '
                cnt_wrong += 1
                list_temp.append((self.excel_str(str(r_42[len(r_42)-(len(final_matrix[0])-1)]).replace('%', ''), current_index, 44, 2) + f"__{self.table_str(current_index, 44, 2)}").rjust(41))        
            str_err = str_err[:-1] + ''.join(list_temp) + '\n'








            str_err = str_err.replace('(3) 총인건비 인상률 지표의 점수계산', '(3) 총인건비 인상률 지표의 점수계산\t\t불일치: [' + str(cnt_wrong) + '/' + str((len(final_matrix[0])-1)*(39+9)+4-2 - cnt_except - ((len(final_matrix[0])-2))*1) + ']')
            str_err_total += '(3) 총인건비 인상률 지표\t\t불일치: [' + str(cnt_wrong) + '/' + str((len(final_matrix[0])-1)*(39+9)+4-2 - cnt_except - ((len(final_matrix[0])-2))*1) + ']\n'
            str_err += '\n\n\n'










        if 1 == 1 or current_index == 3:
            current_index = 3
            str_err += '(3-1) 증원 소요 인건비 계산\n\n'
            str_err += '           전당인전 증' + f"{'전년도인원(A)':>16}{'당년도인원(B)':>17}{'인원증감(C)':>18}{'전년도단가(D)':>25}{'증원인건비':>29}\n"






            excel_original_03 = excel_original_03.replace('△', '-')



            list_title_03 = list(self.list_title_03)
            rank_count_03 = len(list_title_03)


            
            cnt_wrong = 0
            for i in range (0, rank_count_03):


                excel = excel_original_03.split(list_title_03[i])[1] # (3-1)
                excel_item = excel.split('\r\n')[0]   
                str_err += list_title_03[i][:6] + '\t'
                
                list_temp = []                
                for j in range(1, 6):

                    if i in [rank_count_03-1] and j == 4:
                        str_err += '  '
                        list_temp.append(' ' * 25)
                        # list_temp.append(' ' * 41)
                        continue

                    if float(self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '')) == float(self.table_str(current_index, i, j).replace(',', '')):
                        str_err += 'O '
                        if j == 4: list_temp.append(' ' * 25)
                        elif j == 5: list_temp.append(' ' * 39)
                        else: list_temp.append(' ' * 21)
                    else:
                        str_err += 'X '
                        cnt_wrong += 1
                        if j == 4: list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j)}").rjust(25))
                        elif j == 5: list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j)}").rjust(39))
                        else: list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j)}").rjust(21))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-1) 증원 소요 인건비 계산', '(3-1) 증원 소요 인건비 계산\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_03*5-1) + ']')
            str_err_total += '(3-1) 증원 소요 인건비 계산\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_03*5-1) + ']\n'
            str_err += '\n\n\n'





        if 1 == 1 or current_index == 4:
            current_index = 4

            list_title_04 = list(self.list_title_04)
            rank_count_04 = len(list_title_04)

            str_err += '(3-2) 직급별 평균 인원 계산\n\n전년도\n'
            str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>20}{'2월':>20}{'3월':>20}{'4월':>20}{'5월':>20}{'6월':>20}{'7월':>20}{'8월':>21}{'9월':>20}{'10월':>20}{'11월':>20}{'12월':>20}{'평균인원':>18}\n"


            
            cnt_wrong = 0
            for i in range (0, rank_count_04*2):

                if i == rank_count_04:
                    str_err += '\n\n당년도\n'
                    str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>20}{'2월':>20}{'3월':>20}{'4월':>20}{'5월':>20}{'6월':>20}{'7월':>20}{'8월':>21}{'9월':>20}{'10월':>20}{'11월':>20}{'12월':>20}{'평균인원':>18}\n"

                if i < rank_count_04:   # 전년도 표

                    excel = excel_original_04.split(list_title_04[i%rank_count_04])[1]
                    excel_item = excel.split('\r\n')[0]

                    str_err += list_title_04[i%rank_count_04][:6] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 14):
                        if j == 13:
                            if self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '') == self.table_str(current_index, i, j+1).replace(',', ''):
                                str_err += 'O '
                                list_temp.append(' ' * 21)
                            else:
                                str_err += 'X '
                                cnt_wrong += 1
                                list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(21))
                        elif float(self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '')) == float(self.table_str(current_index, i, j+1).replace(',', '')):
                            str_err += 'O '
                            list_temp.append(' ' * 21)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(21))

                else:   # 당년도 표



                    excel = excel_original_04.split(list_title_04[i%rank_count_04])[2]
                    excel_item = excel.split('\r\n')[0]
                    
                    str_err += list_title_04[i%rank_count_04][:6] + '\t'
                    
                    list_temp = []
                    for j in range(1, 14):
                        if j == 13:
                            if self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '') == self.table_str(current_index, i+2, j+1).replace(',', ''):
                                str_err += 'O '
                                list_temp.append(' ' * 21)
                            else:
                                str_err += 'X '
                                cnt_wrong += 1
                                list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i+2, j+1)}").rjust(21))
                        elif float(self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '')) == float(self.table_str(current_index, i+2, j+1).replace(',', '')):
                            str_err += 'O '
                            list_temp.append(' ' * 21)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i+2, j+1)}").rjust(21))
                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-2) 직급별 평균 인원 계산', '(3-2) 직급별 평균 인원 계산\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_03*26) + ']')
            str_err_total += '(3-2) 직급별 평균 인원 계산\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_04*26) + ']\n'
            str_err += '\n\n\n'













        if 1 == 1 or current_index == 5:
            current_index = 5

            list_title_05 = list(self.list_title_05)
            rank_count_05 = len(list_title_05)

            str_err += '(3-3) 가. 정원 및 현원 차이\n\n당년도\n'
            str_err += '          1정현복 누      2월       3월        4월       5월       6월' + f"{'1월 정원':>25}{'1월 현원':>22}{'1월 복직자':>22}{'1월 누적차':>22}{'2월 정원':>22}{'2월 현원':>22}{'2월 복직자':>22}{'2월 누적차':>22}{'3월 정원':>22}{'3월 현원':>22}{'3월 복직자':>22}{'3월 누적차':>22}{'4월 정원':>22}{'4월 현원':>22}{'4월 복직자':>22}{'4월 누적차':>22}{'5월 정원':>22}{'5월 현원':>22}{'5월 복직자':>21}{'5월 누적차':>22}{'6월 정원':>22}{'6월 현원':>22}{'6월 복직자':>22}{'6월 누적차':>22}\n"

                        
            cnt_wrong = 0
            for i in range (0, (rank_count_05*2)+2):

                if i == rank_count_05:
                    continue
                
                if i == rank_count_05+1:
                    str_err += '\n\n당년도\n'
                    str_err += '          7정현복 누      8월       9월       10월      11월      12월' + f"{'7월 정원':>25}{'7월 현원':>22}{'7월 복직자':>22}{'7월 누적차':>22}{'8월 정원':>22}{'8월 현원':>22}{'8월 복직자':>22}{'8월 누적차':>22}{'9월 정원':>22}{'9월 현원':>22}{'9월 복직자':>22}{'9월 누적차':>22}{'10월 정원':>22}{'10월 현원':>22}{'10월 복직자':>22}{'10월 누적차':>22}{'11월 정원':>22}{'11월 현원':>22}{'11월 복직자':>21}{'11월 누적차':>22}{'12월 정원':>22}{'12월 현원':>22}{'12월 복직자':>22}{'12월 누적차':>22}\n"
                    continue
                
                if i < rank_count_05+1:   # 1~6월

                    excel = excel_original_05.split(list_title_05[i])[1] # (3-3) 가. 증원 근속 인원
                    excel_item = excel.split('\r\n')[0]
                    str_err += list_title_05[i][:6] + '\t'
                    
                    list_temp = []
                    for j in range(1, 25):
                        if i == rank_count_05-1 and j%4 == 0:
                            str_err += '  '
                            str_err += '  '
                            list_temp.append(' ' * 25)
                            continue
                        
                        if float(self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '')) == float(self.table_str(current_index, i, j+1).replace(',', '')):
                            str_err += 'O '
                            list_temp.append(' ' * 25)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append(f"{self.excel_str(excel_item.split('\t')[j], current_index, i, j)}"f"__{self.table_str(current_index, i, j+1)}".rjust(25))
                            
                        if j%4 == 0: str_err = str_err[:-1] + '   '

                else:   # 7~12월
                    
                    excel = excel_original_05.split(list_title_05[(i%rank_count_05)-2])[2] # (3-3) 가. 증원 근속 인원
                    excel_item = excel.split('\r\n')[0]
                    str_err += list_title_05[i%rank_count_05-2][:6] + '\t'

                    list_temp = []                
                    for j in range(1, 25):
                        if i == (rank_count_05*2) + 1 and j%4 == 0:
                            str_err += '  '
                            str_err += '  '
                            list_temp.append(' ' * 25)
                            continue                  
                        
                        if float(self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '')) == float(self.table_str(current_index, i, j+1).replace(',', '')):
                            str_err += 'O '
                            list_temp.append(' ' * 25)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append(f"{self.excel_str(excel_item.split('\t')[j], current_index, i, j)}"f"__{self.table_str(current_index, i, j+1)}".rjust(25))
                        if j%4 == 0: str_err = str_err[:-1] + '   '

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-3) 가. 정원 및 현원 차이', '(3-3) 가. 정원 및 현원 차이\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_05*48-12) + ']')
            str_err_total += '(3-3) 가. 정원 및 현원 차이\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_05*48-12) + ']\n'
            str_err += '\n\n\n'








        if 1 == 1 or current_index == 6:
            current_index = 6

            list_title_06 = list(self.list_title_06)
            rank_count_06 = len(list_title_06)


            
            str_err += '(3-3) 나. 근속승진\n\n'
            str_err += '           1 2 3 4 5 6 7 8 9101112평' + f"{'1월':>17}{'2월':>18}{'3월':>18}{'4월':>18}{'5월':>18}{'6월':>18}{'7월':>18}{'8월':>19}{'9월':>18}{'10월':>18}{'11월':>18}{'12월':>18}\n"


            cnt_wrong = 0
            for i in range (0, rank_count_06):
                
                excel = excel_original_06.split(list_title_06[i])[1] # (3-3) 나. 근속 승진
                excel_item = excel.split('\r\n')[0]

                str_err += list_title_06[i][:6] + '\t'
                
                list_temp = []                
                for j in range(1, 13):
                    if float(self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '')) == float(self.table_str(current_index, i, j+1).replace(',', '')):
                        str_err += 'O '
                        list_temp.append(' ' * 19)
                    else:
                        str_err += 'X '
                        cnt_wrong += 1
                        list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(19))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-3) 나. 근속승진', '(3-3) 나. 근속승진\t\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_06*12) + ']')
            str_err_total += '(3-3) 나. 근속승진\t\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_06*12) + ']\n'
            str_err += '\n\n\n'




        if 1 == 1 or current_index == 7:
            current_index = 7
            
            list_title_07 = list(self.list_title_07)
            rank_count_07 = len(list_title_07)

            
            str_err += '(3-3) 다. 증원 인건비 인원\n\n당년도\n'
            str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>20}{'2월':>20}{'3월':>20}{'4월':>20}{'5월':>20}{'6월':>20}{'7월':>20}{'8월':>21}{'9월':>20}{'10월':>20}{'11월':>20}{'12월':>20}{'평균인원':>18}\n"


            cnt_wrong = 0
            for i in range (0, (rank_count_07*2)):

                if i == rank_count_07:
                    str_err += '\n\n전년도\n'
                    str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>20}{'2월':>20}{'3월':>20}{'4월':>20}{'5월':>20}{'6월':>20}{'7월':>20}{'8월':>21}{'9월':>20}{'10월':>20}{'11월':>20}{'12월':>20}{'평균인원':>18}\n"

                if i < rank_count_07:   # 전년도 표



                    excel = excel_original_07.split(list_title_07[i])[1] # (3-3) 다
                    excel_item = excel.split('\r\n')[0]

                    str_err += list_title_07[i][:6] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 14):
                        if j == 13:
                            if self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '') == self.table_str(current_index, i, j+1).replace(',', ''):
                                str_err += 'O '
                                list_temp.append(' ' * 21)
                            else:
                                str_err += 'X '
                                cnt_wrong += 1
                                list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(21))
                        elif float(self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '')) == float(self.table_str(current_index, i, j+1).replace(',', '')):
                            str_err += 'O '
                            list_temp.append(' ' * 21)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(21))

                else:   # 당년도 표


                    if list_title_07[i%rank_count_07] == '심사위원':
                        excel = excel_original_07.split(list_title_07[i%rank_count_07])[3] # (3-3) 다
                    else:
                        excel = excel_original_07.split(list_title_07[i%rank_count_07])[2] # (3-3) 다
                    excel_item = excel.split('\r\n')[0]


                    str_err += list_title_07[i%rank_count_07][:6] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 14):
                        if j == 13:
                            if self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '') == self.table_str(current_index, i+2, j+1).replace(',', ''):
                                str_err += 'O '
                                list_temp.append(' ' * 21)
                            else:
                                str_err += 'X '
                                cnt_wrong += 1
                                list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i+2, j+1)}").rjust(21))
                        elif float(self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '')) == float(self.table_str(current_index, i+2, j+1).replace(',', '')):
                            str_err += 'O '
                            list_temp.append(' ' * 21)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i+2, j+1)}").rjust(21))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-3) 다. 증원 인건비 인원', '(3-3) 다. 증원 인건비 인원\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_07*26) + ']')
            str_err_total += '(3-3) 다. 증원 인건비 인원\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_07*26) + ']\n'
            str_err += '\n\n\n'


        if 1 == 1 or current_index == 8:

            current_index = 8
            
            list_title_08 = list(self.list_title_08)
            rank_count_08 = len(list_title_08)
            excel_original_08 = excel_original_08.replace('\r\n계\t', '\t계\t')

            
            str_err += '(3-4) 직급별 평균단가 계산\n전년도\n'
            str_err += '           1 2 3 4 5 6 7 8 9 101112인직' + f"{'1월':>36}{'2월':>36}{'3월':>36}{'4월':>36}{'5월':>36}{'6월':>36}{'7월':>37}{'8월':>36}{'9월':>36}{'10월':>36}{'11월':>36}{'12월':>36}{'인건비총계':>33}{'직급별평균단가':>31}\n"


            cnt_wrong = 0


            for i in range (0, rank_count_08*2):

                if i == rank_count_08:
                    str_err += '\n\n당년도\n'
                    str_err += '           1 2 3 4 5 6 7 8 9 101112인직' + f"{'1월':>36}{'2월':>36}{'3월':>36}{'4월':>36}{'5월':>36}{'6월':>36}{'7월':>37}{'8월':>36}{'9월':>36}{'10월':>36}{'11월':>36}{'12월':>36}{'인건비총계':>33}{'직급별평균단가':>31}\n"


                if i < rank_count_08:   # 전년도 표


                    excel = excel_original_08.split('\t' + list_title_08[i%rank_count_08] + '\t')[1] # (3-4) 직급별 평균단가
                    excel_item = excel.split('\r\n')[0]

                    str_err += list_title_08[i][:6] + '\t'
                    
                    list_temp = []





                    
                    for j in range(1, 14):
                        if self.excel_str(excel_item.split('\t')[j-1], current_index, i, j-1).replace(',', '') == self.table_str(current_index, i, j+1).replace(',', ''):
                            str_err += 'O '
                            list_temp.append(' ' * 37)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j-1], current_index, i, j-1) + f"__{self.table_str(current_index, i, j+1)}").rjust(37))

                    list_avg = excel_original_08.split('총계')[1].split('\r\n')[0].split('\t')

                    if '단가' in list_avg[1]:
                        if self.excel_str(excel_item.split('\t')[14-1], current_index, i, 14-1).replace(',', '') == self.table_str(current_index, i, 14+1).replace(',', ''):
                            str_err += 'O '
                            list_temp.append(' ' * 37)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[14-1], current_index, i, 14-1) + f"__{self.table_str(current_index, i, 14+1)}").rjust(37))
                    else:
                        if self.excel_str(excel_item.split('\t')[14-1+1], current_index, i, 14-1+1).replace(',', '') == self.table_str(current_index, i, 14+1).replace(',', ''):
                            str_err += 'O '
                            list_temp.append(' ' * 37)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[14-1+1], current_index, i, 14-1) + f"__{self.table_str(current_index, i, 14+1)}").rjust(37))
                    
              


                else:   # 당년도 표


                    excel = excel_original_08.split('\t' + list_title_08[i%rank_count_08] + '\t')[2]
                    excel_item = excel.split('\r\n')[0]

                    str_err += list_title_08[i%rank_count_08][:6] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 14):
                        
                        if self.excel_str(excel_item.split('\t')[j-1], current_index, i, j-1).replace(',', '') == self.table_str(current_index, i+2, j+1).replace(',', ''):
                            str_err += 'O '
                            list_temp.append(' ' * 37)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j-1], current_index, i, j-1) + f"__{self.table_str(current_index, i+2, j+1)}").rjust(37))


                    if '단가' in list_avg[1]:
                        if self.excel_str(excel_item.split('\t')[14-1], current_index, i, 14-1).replace(',', '') == self.table_str(current_index, i+2, 14+1).replace(',', ''):
                            str_err += 'O '
                            list_temp.append(' ' * 37)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[14-1], current_index, i, 14-1) + f"__{self.table_str(current_index, i+2, 14+1)}").rjust(37))
                    else:
                        if self.excel_str(excel_item.split('\t')[14-1+1], current_index, i, 14-1+1).replace(',', '') == self.table_str(current_index, i+2, 14+1).replace(',', ''):
                            str_err += 'O '
                            list_temp.append(' ' * 37)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[14-1+1], current_index, i, 14-1) + f"__{self.table_str(current_index, i+2, 14+1)}").rjust(37))
                    

                            

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-4) 직급별 평균단가 계산', '(3-4) 직급별 평균단가 계산\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_08*28) + ']')
            str_err_total += '(3-4) 직급별 평균단가 계산\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_08*28) + ']\n'
            str_err += '\n\n\n'






        if 1 == 1 or current_index == 9:

            current_index = 9
            
            list_title_09 = list(self.list_title_09)
            rank_count_09 = len(list_title_09)

            str_err += '(3-6) 가. 초임직급 정원\n\n당년도\n'
            str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>19}{'2월':>19}{'3월':>19}{'4월':>19}{'5월':>19}{'6월':>19}{'7월':>19}{'8월':>20}{'9월':>19}{'10월':>19}{'11월':>19}{'12월':>19}{'평균인원':>18}\n"


            cnt_wrong = 0
            
            for i in range (0, rank_count_09*2):


                if i == rank_count_09:
                    str_err += '\n\n전년도\n'
                    str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>19}{'2월':>19}{'3월':>19}{'4월':>19}{'5월':>19}{'6월':>19}{'7월':>19}{'8월':>20}{'9월':>19}{'10월':>19}{'11월':>19}{'12월':>19}{'평균인원':>18}\n"

                if i < rank_count_09:   # 전년도 표
                    excel = excel_original_09.split(list_title_09[i])[1] # (3-3) 가. 초임직급 인원
                    excel_item = excel.split('\r\n')[0]

                    str_err += list_title_09[i][:6] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 14):
                        if j == 13:
                            if self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '') == self.table_str(current_index, i, j+1).replace(',', ''):
                                str_err += 'O '
                                list_temp.append(' ' * 20)
                            else:
                                str_err += 'X '
                                cnt_wrong += 1
                                list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(20))

                        
                        elif float(self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '')) == float(self.table_str(current_index, i, j+1).replace(',', '')):
                            str_err += 'O '
                            list_temp.append(' ' * 20)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(20))

                else:   # 당년도 표

                    excel = excel_original_09.split(list_title_09[(i%rank_count_09)])[2] # (3-3) 가. 초임직급 인원
                    excel_item = excel.split('\r\n')[0]
                    
                    # str_err += self.text_table(i+2, 1) + '\t'
                    str_err += list_title_09[(i%rank_count_09)][:6] + '\t'

                    list_temp = []                
                    for j in range(1, 14):
                        if j == 13:
                            if self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '') == self.table_str(current_index, i+2, j+1).replace(',', ''):
                                str_err += 'O '
                                list_temp.append(' ' * 20)
                            else:
                                str_err += 'X '
                                cnt_wrong += 1
                                list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i+2, j+1)}").rjust(20))
                            
                        elif float(self.excel_str(excel_item.split('\t')[j], current_index, i, j).replace(',', '')) == float(self.table_str(current_index, i+2, j+1).replace(',', '')):
                            str_err += 'O '
                            list_temp.append(' ' * 20)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i+2, j+1)}").rjust(20))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-6) 가. 초임직급 정원', '(3-6) 가. 초임직급 정원\t\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_09*26) + ']')
            str_err_total += '(3-6) 가. 초임직급 정원\t\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_09*26) + ']\n'
            str_err += '\n\n\n'






        if 1 == 1 or current_index == 10:
            current_index = 10

            list_title_10 = list(self.list_title_10)
            rank_count_10 = len(list_title_10)

            
            str_err += '(3-6) 나. 초임직급 인건비\n\n'
            str_err += '           전당인전 증' + f"{'전년도인원(A)':>18}{'당년도인원(B)':>18}{'인원증감(C)':>18}{'전년도단가(D)':>22}{'증원인건비':>28}\n"


            cnt_wrong = 0
            for i in range (0, rank_count_10):

                
                excel = excel_original_10.split(list_title_10[i])[1] # (3-3) 나. 초임직급 인건비
                excel_item = excel.split('\r\n')[0]   
                str_err += list_title_10[i][:6] + '\t'
                
                list_temp = []
                for j in range(1, 6):
                    if i in [rank_count_10-1] and j == 4:
                        str_err += '  '
                        list_temp.append(' ' * 41)
                        continue
                
                    if float(self.excel_str(excel_item.split('\t')[j], 10, i, j).replace(',', '')) == float(self.table_str(10, i, j).replace(',', '')):
                        str_err += 'O '
                        if j == 4: list_temp.append(' ' * 26)
                        elif j == 5: list_temp.append(' ' * 33)
                        else: list_temp.append(' ' * 22)
                    else:
                        str_err += 'X '
                        cnt_wrong += 1

                        if j == 4: list_temp.append((self.excel_str(excel_item.split('\t')[j], 10, i, j) + f"__{self.table_str(10, i, j)}").rjust(26))
                        elif j == 5: list_temp.append((self.excel_str(excel_item.split('\t')[j], 10, i, j) + f"__{self.table_str(10, i, j)}").rjust(33))
                        else: list_temp.append((self.excel_str(excel_item.split('\t')[j], 10, i, j) + f"__{self.table_str(10, i, j)}").rjust(22))


                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-6) 나. 초임직급 인건비', '(3-6) 나. 초임직급 인건비\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_10*5-1) + ']')
            str_err += '\n'
            str_err_total += '(3-6) 나. 초임직급 인건비\t불일치: [' + str(cnt_wrong) + '/' + str(rank_count_10*5-1) + ']\n\n'


        str_err = str_err_total + '\n\n' + str_err

        return str_err












    def alert_tk(self, str_not):
        import tkinter as tk
        from tkinter import messagebox

        str_not = str_not.replace("'", "").replace("[,", "[")
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning('경고', str_not)
        root.destroy()



    def excel_input(self):



        


        global excel_original_01, excel_original_02, excel_original_04, excel_original_05, excel_original_07, excel_original_08, excel_original_09, excel_original_11, excel_original_12, excel_original_13, excel_original_14, excel_original_18


        # s1 ############################################################################


        excel_original_01 = excel_original_01.replace('△', '-').replace(' ', '')

        if year == '2025':

            list_title_01 = ['기본급', '인센티브 상여금', '그 외 상여금', '법정수당', '해외근무수당', '그 외 제수당', '퇴직급여(명예퇴직금 포함)', '임원 인건비', '비상임이사 인건비',
                             '인상률 제외 인건비', '기타항목', '급료,임금,제수당 소계ⓐ',  '사내근로복지기금출연금', '국민연금사용자부담분',
                             '건강보험사용자부담분', '고용보험사용자부담분', '산재보험료사용자부담분', '급식비', '교통보조비', '자가운전보조금', '학자보조금','건강진단비',
                             '선택적복지', '행사비', '포상품(비)', '기념품(비)', '격려품(비)', '장기근속관련 비용', '육아보조비 및 출산장려금', '자기계발비', '특별근로의 대가',
                             '피복비', '경로효친비', '통신비', '축하금/조의금', '기타 항목', '복리후생비 소계ⓑ', '일반 급여 (1)', '인센티브 상여금', '순액', '청년인턴 급여 (2)', '인센티브 상여금', '순액', '무기계약직 급여 (3)',
                             '인센티브 상여금', '순액', '소계 ⓒ=(1)+(2)+(3)', '인건비 총계: ⓓ=ⓐ+ⓑ+ⓒ', '인센티브 상여금 ⓔ=ⓔ-1+ⓔ-2', '인센티브 전환금 (ⓔ-1)', '인센티브 추가금 (ⓔ-2)', '인건비 해당금액 : ⓓ-ⓔ']
                   
            list_keyword = ['기본', '인센', '그외상여', '법정', '해외', '그외제수', '퇴직급여', '임원', '비상임', '제외', '기타', '급료', '사내근로', '국민', '건강보험', '고용', '산재', '급식', '교통', '운전', '학자', '건강진단', '선택', '행사', '포상', '기념',
                            '격려', '장기', '육아', '자기', '특별', '피복', '경로', '통신', '축하', '기타', '복리', '일반', '상여', '순액', '청년', '상여', '순액', '무기', '상여', '순액', '소계', '인건비', '상여', '전환', '추가', '해당']

            readonly_rows = [11, 36, 37, 40, 43, 46, 47, 48, 51]


        elif year in ['2024', '2023']:

            list_title_01 = ['기본급', '인센티브 상여금', '그 외 상여금', '법정수당', '해외근무수당', '그 외 제수당', '퇴직급여(명예퇴직금 포함)', '임원 인건비', '비상임이사 인건비',
                             '인상률 제외 인건비(통상)', '인상률 제외 인건비(기타)', '기타항목', '급료,임금,제수당 소계ⓐ',  '사내근로복지기금출연금', '국민연금사용자부담분',
                             '건강보험사용자부담분', '고용보험사용자부담분', '산재보험료사용자부담분', '급식비', '교통보조비', '자가운전보조금', '학자보조금','건강진단비',
                             '선택적복지', '행사비', '포상품(비)', '기념품(비)', '격려품(비)', '장기근속관련 비용', '육아보조비 및 출산장려금', '자기계발비', '특별근로의 대가',
                             '피복비', '경로효친비', '통신비', '축하금/조의금', '기타 항목', '복리후생비 소계ⓑ', '일반 급여 (1)', '인센티브 상여금', '순액', '청년인턴 급여 (2)', '인센티브 상여금', '순액', '무기계약직 급여 (3)',
                             '인센티브 상여금', '순액', '소계 ⓒ=(1)+(2)+(3)', '인건비 총계: ⓓ=ⓐ+ⓑ+ⓒ', '인센티브 상여금 ⓔ=ⓔ-1+ⓔ-2', '인센티브 전환금 (ⓔ-1)', '인센티브 추가금 (ⓔ-2)', '인건비 해당금액 : ⓓ-ⓔ']
                   
            list_keyword = ['기본', '인센', '그외상여', '법정', '해외', '그외제수', '퇴직급여', '임원', '비상임', '통상', '기타제외', '기타', '급료', '사내근로', '국민', '건강보험', '고용', '산재', '급식', '교통', '운전', '학자', '건강진단', '선택', '행사', '포상', '기념',
                            '격려', '장기', '육아', '자기', '특별', '피복', '경로', '통신', '축하', '기타', '복리', '일반', '상여', '순액', '청년', '상여', '순액', '무기', '상여', '순액', '소계', '인건비', '상여', '전환', '추가', '해당']

            readonly_rows = [12, 37, 38, 41, 44, 47, 48, 49, 52]









        flag_gibon = False

        if not list_years2:
            for item in excel_original_01.split('\r\n'):
                col_gibon = 0
                for item_col in item.split('\t'):
                    if '판관비' in item_col:
                        flag_gibon = True
                        break
                    col_gibon += 1
                if flag_gibon:
                    break


        else:        
            for item in excel_original_01.split('\r\n'):
                col_gibon = 0
                for item_col in item.split('\t'):
                    if max(list_years2) in item_col:
                        flag_gibon = True
                        break
                    col_gibon += 1
                if flag_gibon:
                    break


        matches = re.findall(r'20\d+.*?\t+.*?20\d+', excel_original_01.replace('\t\t\t\t\t\t\t\t\t', '')[:188])
        if matches:
            col_gibon_width = len(matches[0].split('\t'))-2
        else:
            col_gibon_width = 5




        if '판관비' in excel_original_01[:300]:
            list_temp = excel_original_01.split('판관비')[1:]
            list_temp = '판관비'.join(list_temp).split('소계')[0]
        elif '인건비항목' in excel_original_01[:300]:
            list_temp = excel_original_01.split('인건비항목')[1:]
            list_temp = '인건비항목'.join(list_temp).split('소계')[0]
        else:
            list_temp = excel_original_01.split('20')[1:]
            list_temp = '20'.join(list_temp).split('소계')[0]

        list_temp = list_temp.replace('급료\r\n', '').replace('임금\r\n', '')
        if '인센' not in list_temp:
            if '상여금' in list_temp:
                list_temp = list_temp.replace('상여금', '상여금 인센티브')
        if '법정' not in list_temp and '해외근무' not in list_temp:
            if '제수당' in list_temp:
                list_temp = list_temp.replace('제수당', '제수당 법정수당')




        list_temp = list_temp.split('\r\n')
        list_temp_clean = []
        for item in list_temp:
            if item.strip():
                list_temp_clean.append(item)
        list_temp = list_temp_clean
        list_temp = list_temp[1:len(list_temp)-1]


        col_5 = 5
        if list_years2 and col_gibon_width != 5: # (2) 에서 판관비 등 5열이 없으면 col_5 =1 (1개 열만 판관비로 입력)
            col_5 = 1
            list_clean = []
            for item in list_temp:
                list_clean.append(item.split('\t')[:col_gibon+1])

            for i in range(len(list_clean[0])):
                if '제수당' in list_clean[0][i]:
                    list_clean[0][i] = ""

            list_temp = list_clean
        else:
            list_clean = []
            for item in list_temp:
                list_clean.append(item.split('\t')[:col_gibon+5+1])
            list_temp = list_clean








            
        
        if year in ['2024', '2023']:   # (2) 부적절한 인건비항목이 있으면 list_not에 포함
            list_keyword_01 = list_keyword[:12]
            list_keyword_01_answer = [[] for _ in range(12)]

            for i in range(12):
                for j in range(len(list_temp)):
                    if list_keyword_01[i] in str(list_temp[j]):
                        list_keyword_01_answer[i] = list_temp[j][col_gibon:col_gibon+col_5+1]

            list_not = []
            for j in range(len(list_temp)):
                if not ''.join(list_temp[j][:col_gibon+col_5-1]):
                    continue
                flag_not = False
                for i in range(12):
                    if list_keyword_01[i] in str(list_temp[j]):
                        flag_not = True
                if not flag_not:
                    list_not.append(list_temp[j][:col_gibon+col_5-1])


        if year in ['2025']:
            list_keyword_01 = list_keyword[:11]
            list_keyword_01_answer = [[] for _ in range(11)]

            for i in range(11):
                for j in range(len(list_temp)):
                    if list_keyword_01[i] in str(list_temp[j]):
                        list_keyword_01_answer[i] = list_temp[j][col_gibon:col_gibon+col_5+1]

            list_not = []
            for j in range(len(list_temp)):
                if not ''.join(list_temp[j][:col_gibon+col_5-1]):
                    continue
                flag_not = False
                for i in range(11):
                    if list_keyword_01[i] in str(list_temp[j]):
                        flag_not = True
                if not flag_not:
                    list_not.append(list_temp[j][:col_gibon+col_5-1])


          
        str_not = ""
        for i in range(len(list_not)):
            if len(str(list_not[i])) > 60:
                str_not += str(list_not[i])[:60] + ' ...\n'
            else:
                str_not += str(list_not[i]) + '\n'

        if list_not:
            str_not = '(2) 인건비집계: 부적절한 인건비항목\n엑셀파일 (2)인건비집계를 변경하세요.\n\n' + str_not
            str_not += '\n인건비 항목:\n기본급, 인센티브, 그외상여금, 법정, 해외근무, 그외제수당,\n퇴직급여, 임원, 비상임, 통상, 기타제외, 기타항목'
            self.alert_tk(str_not)

            return 'str_not'



        list_temp = excel_original_01.replace('\t-\t', '\t\t').replace(',', '').replace('인건비\r\n', '인건비').split('소계')[1]   # (2) 사내근로 ~ 기타항목
        list_temp = list_temp.split('\r\n')
        list_temp_clean = []
        for item in list_temp:
            if item.strip():
                list_temp_clean.append(item.split('\t'))
        list_temp = list_temp_clean
        list_temp = list_temp[1:len(list_temp)-1]




        if year in ['2025']:
            list_keyword_02 = list_keyword[12:36]
            list_keyword_02_answer = [[] for _ in range(24)]

            for i in range(24):
                for j in range(len(list_temp)):
                    if list_keyword_02[i] in str(list_temp[j]):
                        list_keyword_02_answer[i] = list_temp[j][col_gibon:col_gibon+col_5+1]

            list_not = []
            for j in range(len(list_temp)):
                if not ''.join(list_temp[j][:col_gibon+col_5-1]):
                    continue
                flag_not = False
                for i in range(24):
                    if list_keyword_02[i] in str(list_temp[j]):
                        flag_not = True
                if not flag_not:
                    list_not.append(list_temp[j][:col_gibon+col_5-1])



        if year in ['2023', '2024']:
            list_keyword_02 = list_keyword[13:37]
            list_keyword_02_answer = [[] for _ in range(24)]

            for i in range(24):
                for j in range(len(list_temp)):
                    if list_keyword_02[i] in str(list_temp[j]):
                        list_keyword_02_answer[i] = list_temp[j][col_gibon:col_gibon+col_5+1]

            list_not = []
            for j in range(len(list_temp)):
                if not ''.join(list_temp[j][:col_gibon+col_5-1]):
                    continue
                flag_not = False
                for i in range(24):
                    if list_keyword_02[i] in str(list_temp[j]):
                        flag_not = True
                if not flag_not:
                    list_not.append(list_temp[j][:col_gibon+col_5-1])






        str_not = ""
        for i in range(len(list_not)):
            if len(str(list_not[i])) > 60:
                str_not += str(list_not[i])[:60] + ' ...\n'
            else:
                str_not += str(list_not[i]) + '\n'

        if list_not:
            str_not = '(2) 인건비집계: 부적절한 인건비항목\n엑셀파일 (2)인건비집계를 변경하세요.\n\n' + str_not
            str_not += '\n인건비 항목:\n사내근로, 국민, 건강보험, 고용, 산재, 급식, 교통, 운전, 학자,\n건강, 선택, 행사, 포상, 기념, 격려, 장기, 육아, 자기, 특별, 피복\n경로, 통신, 축하, 기타'
            self.alert_tk(str_not)

            return 'str_not'




        list_temp = excel_original_01.replace('\t-\t', '\t\t').replace(',', '').split('소계')[2:]   # (2) 일반급여 ~ 인센티브 추가금
        list_temp = '소계'.join(list_temp).split('해당')[0].replace('인센티브\t', '인센티브 상여금\t').replace('(가)', '').replace('(나)', '').replace('(다)', '').replace('(라)', '').replace('(마)', '')
        list_temp = list_temp.split('\r\n')
        list_temp_clean = []
        for item in list_temp:
            if item.strip():
                list_temp_clean.append(item.split('\t'))
        list_temp = list_temp_clean
        list_temp = list_temp[1:len(list_temp)-1]





        if year in ['2025']:
            list_keyword_03 = list_keyword[37:51]
            list_keyword_03_answer = [[] for _ in range(14)]


            for i in range(14):
                for j in range(len(list_temp)):
                    list_keyword_03_answer[i] = list_temp[i][col_gibon:col_gibon+col_5+1]


            list_not = []
            for j in range(len(list_temp)):
                if not ''.join(list_temp[j][:col_gibon+col_5-1]):
                    continue
                flag_not = False
                for i in range(14):
                    if list_keyword_03[i] in str(list_temp[j]):
                        flag_not = True
                if not flag_not:
                    list_not.append(list_temp[j][:col_gibon+col_5-1])



        if year in ['2024', '2023']:
            list_keyword_03 = list_keyword[38:52]
            list_keyword_03_answer = [[] for _ in range(14)]


            for i in range(14):
                for j in range(len(list_temp)):
                    
                    list_keyword_03_answer[i] = list_temp[i][col_gibon:col_gibon+col_5+1]


            list_not = []
            for j in range(len(list_temp)):
                if not ''.join(list_temp[j][:col_gibon+col_5-1]):
                    continue
                flag_not = False
                for i in range(14):
                    if list_keyword_03[i] in str(list_temp[j]):
                        flag_not = True
                if not flag_not:
                    list_not.append(list_temp[j][:col_gibon+col_5-1])





        str_not = ""
        for i in range(len(list_not)):
            if len(str(list_not[i])) > 60:
                str_not += str(list_not[i])[:60] + ' ...\n'
            else:
                str_not += str(list_not[i]) + '\n'

        if list_not:
            str_not = '(2) 인건비집계: 부적절한 인건비항목\n엑셀파일 (2)인건비집계를 변경하세요.\n\n' + str_not
            str_not += '\n인건비 항목:\n일반 급여, 청년인턴 급여, 무기계약직 급여, 순액,\n인센티브 상여금, 인센티브 전환금, 인센티브 추가금'
            self.alert_tk(str_not)

            return 'str_not'






	


        try:

            for i in range(len(list_keyword_01_answer)):   # (2) 기본급 ~ 기타항목
                for j in range(col_5):
                    if list_keyword_01_answer[i]:
                        self.s1.table.item(i, j+1).setText(list_keyword_01_answer[i][j])
           

            for i in range(len(list_keyword_02_answer)):   # (2) 사내근로 ~ 기타항목
                for j in range(col_5):
                    if list_keyword_02_answer[i]:
                        self.s1.table.item(i+len(list_keyword_01_answer)+1, j+1).setText(list_keyword_02_answer[i][j])


                
            for i in range(len(list_keyword_03_answer)):   # (2) 인센티브 전환금 ~ 인센티브 추가금
                if i in [0, 3, 6, 9, 10, 11]:
                    continue
                for j in range(col_5):
                    if list_keyword_03_answer[i]:
                        self.s1.table.item(i+len(list_keyword_01_answer)+1+len(list_keyword_02_answer)+1, j+1).setText(list_keyword_03_answer[i][j])



            global list_s1_01, list_s1_02, list_s1_03
            list_s1_01 = list_keyword_01_answer
            list_s1_02 = list_keyword_02_answer
            list_s1_03 = list_keyword_03_answer


            
        except Exception as e:
            print(f"(2) 인건비 집계 입력 오류 [항목: {list_title_01[i].strip()}]: {e}")
            return "excel_original_no"




        # 모든 입력 후 자동 계산 한 번 수행 (변경된 열 기준)
        for col_idx in range(1, 6):
            self.s1.calculate_s1(self.s1.table.item(0, col_idx))

        self.s1.table.blockSignals(False)
        self.s1.table.viewport().update()










        # s2 ############################################################################



        if year == '2025':

            list_title_02 = [
                '1.인센티브상여금을제외한인건비총액', 'a.판관비로처리한인건비', 'b.영업외비용으로처리한인건비', 'c.제조원가로처리한인건비', 
                'd.타계정대체로처리한인건비', 'e.이익잉여금의증감으로처리한인건비', '소계:(A)=a+b+c+d+e', 
                '2.총인건비인상률계산에서제외(조정)되는인건비', 'f.퇴직급여(명예퇴직금포함)', 'g.임원인건비', 'h.비상임이사인건비',
                '기타제외인건비', 'j.사내근로복지기금출연금', 'k.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)', 
                'l.공적보험사용자부담분', 'm.연월차수당등조정(㉠-㉡+㉢)', '연월차수당등발생액(㉠)',
                '연월차수당등지급액(㉡)', '종업원저리대여금이자관련인건비(㉢)', '무상대여이익', 'o.지방이전관련직접인건비', 
                'p.법령에따른특수건강진단비', 'q.해외근무수당', 'r.직무발명보상금', 
                's.공무원수준내의자녀수당및출산격려금', 't.야간간호특별수당', 'u.비상진료체계운영에따른특별수당등',
                'v. 통상임금 판단기준 변경 판례의 영향으로 인한 법정수당 증가분(2024년 귀속분)', '소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s+t+u+v+w', 
                '3.실집행액기준총인건비발생액(C)=(A)-(B)', '4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)',
                '5.별도직군승진시기차이에따른인건비효과조정(E)', '6.초임직급정원변동에따른인건비효과조정(F)', 
                '7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)', '추가로지급된인건비의영향제거(H)', 
                '최저임금지급직원에대한인건비효과조정(I)', '10.파업등에따른인건비효과조정(J)', '11.통상임금판단기준변경판례의영향으로인한법정수당증가분(2025년귀속분)(K)<주30>', 
                ' (C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)-(K)'
            ]

            list_keyword = [
                '티브', '판관비', '영업외', '제조원가', 
                '타계정', '이익', '소계', 
                '총인건비', '퇴직급여', '임원', '비상임',
                '인상률제외', '사내근로', '잡급', 
                '공적', '조정', '발생액',
                '지급액', '종업원', '무상', '지방', 
                '법령', '해외', '직무', 
                '공무원', '야간', '비상',
                '통상', '소계', 
                '실집행', '연도별',
                '별도', '초임', 
                '정년', '추가', 
                '최저', '파업', '통상', 
                '+'
            ]

            readonly_rows = [0, 6, 7, 15, 28, 29, 38] 
            yellow_rows = [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 30, 32]


        elif year == '2024':

            list_title_02 = [
                '1.인센티브상여금을제외한인건비총액', 'a.판관비로처리한인건비', 'b.영업외비용으로처리한인건비', 'c.제조원가로처리한인건비', 
                'd.타계정대체로처리한인건비', 'e.이익잉여금의증감으로처리한인건비', '소계:(A)=a+b+c+d+e', 
                '2.총인건비인상률계산에서제외(조정)되는인건비', 'f.퇴직급여(명예퇴직금포함)', 'g.임원인건비', 'h.비상임이사인건비',
                '인상률제외인건비(통상)', '인상률제외인건비(기타제외)', 'j.사내근로복지기금출연금', 'k.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)', 
                'l.공적보험사용자부담분', 'm.연월차수당등조정(㉠-㉡+㉢)', '연월차수당등발생액(㉠)',
                '연월차수당등지급액(㉡)', '종업원저리대여금이자관련인건비(㉢)', '무상대여이익', 'o.지방이전관련직접인건비', 
                'p.법령에따른특수건강진단비', 'q. 코로나19 대응을 위한 시간외근로수당 등', 'r.해외근무수당', 's.직무발명보상금', 
                't.공무원수준내의자녀수당및출산격려금', 'u.야간간호특별수당', 'v.비상진료체계운영에따른특별수당등',
                'w. 통상임금 판단기준 변경 판례의 영향으로 인한 법정수당 증가분(2024년 귀속분)', '소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s+t+u+v+w', 
                '3.실집행액기준총인건비발생액(C)=(A)-(B)', '4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)',
                '5.별도직군승진시기차이에따른인건비효과조정(E)', '6.초임직급정원변동에따른인건비효과조정(F)', 
                '7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)', '추가로지급된인건비의영향제거(H)', 
                '최저임금지급직원에대한인건비효과조정(I)', '10.파업등에따른인건비효과조정(J)', '11. 코로나19로 인한 휴업의 인건비 효과 조정 (K)', 
                '(C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)+(K)+(L)'
            ]

            list_keyword = [
                '티브', '판관비', '영업외', '제조원가', 
                '타계정', '이익', '소계', 
                '총인건비', '퇴직급여', '임원', '비상임',
                '통상', '기타제외', '사내', '잡급', 
                '공적', '조정', '발생액',
                '지급액', '종업원', '무상', '지방', 
                '법령', '코로나', '해외', '직무', 
                '공무원', '야간', '비상',
                '소계', 
                '실집행', '연도별',
                '별도', '초임', 
                '정년', '추가', 
                '최저', '파업', '코로나', 
                '+'
            ]

            readonly_rows = [0, 6, 7, 16, 29, 30, 39] 
            yellow_rows = [1, 2, 3, 4, 5, 8, 9, 10, 12, 13, 14, 15, 31, 33]



        elif year == '2023':
            list_title_02 = [
                '1.인센티브상여금을제외한인건비총액', 'a.판관비로처리한인건비', 'b.영업외비용으로처리한인건비', 'c.제조원가로처리한인건비', 
                'd.타계정대체로처리한인건비', 'e.이익잉여금의증감으로처리한인건비', '소계:(A)=a+b+c+d+e', 
                '2.총인건비인상률계산에서제외(조정)되는인건비', 'f.퇴직급여(명예퇴직금포함)', 'g.임원인건비', 'h.비상임이사인건비',
                '인상률제외인건비(통상)', '인상률제외인건비(기타제외)', 'j.사내근로복지기금출연금', 'k.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)', 
                'l.공적보험사용자부담분', 'm.연월차수당등조정(㉠-㉡+㉢)', '연월차수당등발생액(㉠)',
                '연월차수당등지급액(㉡)', '종업원저리대여금이자관련인건비(㉢)', '무상대여이익', 'o.지방이전관련직접인건비', 
                'p.법령에따른특수건강진단비', 'q. 코로나19 대응을 위한 시간외근로수당 등', 'r.해외근무수당', 's.직무발명보상금', 
                '소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s', 
                '3.실집행액기준총인건비발생액(C)=(A)-(B)', '4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)',
                '5.별도직군승진시기차이에따른인건비효과조정(E)', '6.초임직급정원변동에따른인건비효과조정(F)', 
                '7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)', '추가로지급된인건비의영향제거(H)', 
                '최저임금지급직원에대한인건비효과조정(I)', '10.파업등에따른인건비효과조정(J)', 
                '11. 코로나19로 인한 휴업의 인건비 효과 조정 (K)',
                '(C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)+(K)'
            ]

            list_keyword = [
                '티브', '판관비', '영업외', '제조원가', 
                '타계정', '이익', '소계', 
                '총인건비', '퇴직급여', '임원', '비상임',
                '통상', '기타제외', '사내', '잡급', 
                '공적', '조정', '발생액',
                '지급액', '종업원', '무상', '지방', 
                '법령', '코로나', '해외', '직무', 
                '소계',
                '실집행', '연도별',
                '별도', '초임', 
                '정년', '추가', 
                '최저', '파업', '코로나', 
                '+'
            ]


            readonly_rows = [0, 6, 7, 16, 26, 27, 36]
            yellow_rows = [1, 2, 3, 4, 5, 8, 9, 10, 12, 13, 14, 15, 28, 30]


        for item in excel_original_02.split('\r\n'):
            col_temp = 0
            flag_col = False
            for item_col in item.split('\t'):
                if max(list_years3) in item_col:
                    flag_col = True
                    break
                col_temp += 1   # 엑셀에서 몇 번째 열부터 금액 시작인지
            if flag_col:
                break

        if len(list_years3) > 3: cnt_col = 3   # (3) ['2025', '2024', '2023'] 몇개 연도인지
        else: cnt_col = len(list_years3)
        
        



        list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('인센')[1].split('소계')[0]   # (3) 판관비 ~ 이익잉여금
        list_temp = list_temp.split('\r\n')
        list_temp_clean = []
        for item in list_temp:
            if item.strip():
                list_temp_clean.append(item)
        list_temp = list_temp_clean
        list_temp = list_temp[1:len(list_temp)-1]

        if year in ['2025', '2024', '2023']:   # (3) 판관비 ~ 이익잉여금
            list_keyword_01 = list_keyword[1:6]
            list_keyword_01_answer = [[] for _ in range(5)]

            for i in range(5):
                for j in range(len(list_temp)):
                    if list_keyword_01[i] in list_temp[j]:
                        list_keyword_01_answer[i] = list_temp[j].split('\t')[col_temp:col_temp+cnt_col]
                    if not list_keyword_01_answer[i]:
                        list_keyword_01_answer[i] = ['' for _ in range(cnt_col)]





        list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('소계')[1]   # (3) 퇴직급여 ~ 공적보험
        list_temp = list_temp.split('\r\n')
        list_temp_clean = []
        for item in list_temp:
            if item.strip():
                list_temp_clean.append(item)
        list_temp = list_temp_clean
        list_temp = list_temp[1:len(list_temp)-1]

        if year in ['2024', '2023']:
            list_keyword_02 = list_keyword[8:16]
            list_keyword_02_answer = [[] for _ in range(8)]

            for i in range(8):
                for j in range(len(list_temp)):
                    if list_keyword_02[i] in list_temp[j]:
                        list_keyword_02_answer[i] = list_temp[j].split('\t')[col_temp:col_temp+cnt_col]
                    if not list_keyword_02_answer[i]:
                        list_keyword_02_answer[i] = ['' for _ in range(cnt_col)]

        if year in ['2025']:
            list_keyword_02 = list_keyword[8:15]
            list_keyword_02_answer = [[] for _ in range(7)]

            for i in range(7):
                for j in range(len(list_temp)):
                    if list_keyword_02[i] in list_temp[j]:
                        list_keyword_02_answer[i] = list_temp[j].split('\t')[col_temp:col_temp+cnt_col]
                    if not list_keyword_02_answer[i]:
                        list_keyword_02_answer[i] = ['' for _ in range(cnt_col)]






        list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('공적')[1].split('소계')[0]   # (3) 연월차 ~ 통상
        list_temp = list_temp.split('\r\n')
        
        list_temp_clean = []
        for item in list_temp:
            if item.strip():
                list_temp_clean.append(item)

        list_temp = list_temp_clean
        list_temp = list_temp[1:len(list_temp)-1]

        if year in ['2025']:
            list_keyword_03 = list_keyword[16:28]
            list_keyword_03_answer = [[] for _ in range(12)]

            for i in range(12):
                for j in range(len(list_temp)):
                    if list_keyword_03[i] in list_temp[j]:
                        list_keyword_03_answer[i] = list_temp[j].split('\t')[col_temp:col_temp+cnt_col]
                    if not list_keyword_03_answer[i]:
                        list_keyword_03_answer[i] = ['' for _ in range(cnt_col)]

        if year in ['2024']:
            
            list_keyword_03 = list_keyword[17:29]
            list_keyword_03_answer = [[] for _ in range(12)]

            for i in range(12):
                for j in range(len(list_temp)):
                    if list_keyword_03[i] in list_temp[j]:
                        list_keyword_03_answer[i] = list_temp[j].split('\t')[col_temp:col_temp+cnt_col]
                    if not list_keyword_03_answer[i]:
                        list_keyword_03_answer[i] = ['' for _ in range(cnt_col)]













        if year in ['2023']:
            list_keyword_03 = list_keyword[17:26]
            list_keyword_03_answer = [[] for _ in range(9)]

            for i in range(9):
                for j in range(len(list_temp)):
                    if list_keyword_03[i] in list_temp[j]:
                        list_keyword_03_answer[i] = list_temp[j].split('\t')[col_temp:col_temp+cnt_col]
                    if not list_keyword_03_answer[i]:
                        list_keyword_03_answer[i] = ['' for _ in range(cnt_col)]






        list_temp = excel_original_02.replace('\t-\t', '\t\t').replace(',', '').split('소계')[2].split('인상률')[0]   # (3) 연도별 ~ 통상
        list_temp = list_temp.split('\r\n')
        list_temp_clean = []
        for item in list_temp:
            if item.strip():
                list_temp_clean.append(item)
        list_temp = list_temp_clean
        list_temp = list_temp[2:len(list_temp)-1]


        if year in ['2025']:
            list_keyword_04 = list_keyword[30:38]
            list_keyword_04_answer = [[] for _ in range(8)]

            for i in range(8):
                for j in range(len(list_temp)):
                    if list_keyword_04[i] in list_temp[j]:
                        list_keyword_04_answer[i] = list_temp[j].split('\t')[col_temp:col_temp+cnt_col]
                    if not list_keyword_04_answer[i]:
                        list_keyword_04_answer[i] = ['' for _ in range(cnt_col)]

        if year in ['2024']:
            list_keyword_04 = list_keyword[31:39]
            list_keyword_04_answer = [[] for _ in range(8)]

            for i in range(8):
                for j in range(len(list_temp)):
                    if list_keyword_04[i] in list_temp[j]:
                        list_keyword_04_answer[i] = list_temp[j].split('\t')[col_temp:col_temp+cnt_col]
                    if not list_keyword_04_answer[i]:
                        list_keyword_04_answer[i] = ['' for _ in range(cnt_col)]

        if year in ['2023']:
            list_keyword_04 = list_keyword[28:36]
            list_keyword_04_answer = [[] for _ in range(8)]

            for i in range(8):
                for j in range(len(list_temp)):
                    if list_keyword_04[i] in list_temp[j]:
                        list_keyword_04_answer[i] = list_temp[j].split('\t')[col_temp:col_temp+cnt_col]
                    if not list_keyword_04_answer[i]:
                        list_keyword_04_answer[i] = ['' for _ in range(cnt_col)]




        '''
        print(list_keyword_01)
        print(list_keyword_01_answer)

        print(list_keyword_02)
        print(list_keyword_02_answer)

        print(list_keyword_03)
        print(list_keyword_03_answer)

        print(list_keyword_04)
        print(list_keyword_04_answer)
        '''



        self.s2.table.blockSignals(True)





        try:

            for i in range(len(list_keyword_01_answer)):    # (3) 판관비 ~ 이익잉여금
                for j in range(cnt_col):
                    self.s2.table.item(i+1, j+2).setText(list_keyword_01_answer[i][j])


            for i in range(len(list_keyword_02_answer)):    # (3) 퇴직급여 ~ 공적보험
                for j in range(cnt_col):
                    self.s2.table.item( len(list_keyword_01_answer)+1 +i+2, j+2).setText(list_keyword_02_answer[i][j])


            for i in range(len(list_keyword_03_answer)):    # (3) 연월차 ~ 통상
                for j in range(cnt_col):
                    self.s2.table.item( len(list_keyword_01_answer)+1 +len(list_keyword_02_answer)+2 + i+1, j+2).setText(list_keyword_03_answer[i][j])


            for i in range(len(list_keyword_04_answer)):    # (3) 연도별 ~ 통상
                for j in range(cnt_col):
                    self.s2.table.item( len(list_keyword_01_answer)+1 +len(list_keyword_02_answer)+2 + len(list_keyword_03_answer)+1 +i+2, j+2).setText(list_keyword_04_answer[i][j])




            global list_s2_01, list_s2_02, list_s2_03, list_s2_04
            list_s2_01 = list_keyword_01_answer
            list_s2_02 = list_keyword_02_answer
            list_s2_03 = list_keyword_03_answer
            list_s2_04 = list_keyword_04_answer













        except Exception as e:
            print(f"(3) 총인건비 인상률 입력 오류 [항목: {list_title_02[i].strip()}]: {e}")
            return "excel_original_no"




        # 모든 입력 후 자동 계산 한 번 수행 (변경된 열 기준)
        for col_idx in range(2, 2+cnt_col):
            self.s2.calculate_s2(self.s2.table.item(0, col_idx))




        self.s2.table.blockSignals(False)
        self.s2.table.viewport().update()




        











        # s4 ############################################################################


        list_title_04 = list(self.list_title_04)
        rank_count_04 = len(list_title_04)


        self.s4.table.blockSignals(True)

        for i in range(0, (rank_count_04*2)):

            excel_original_04 = excel_original_04[excel_original_04.find(list_title_04[i%rank_count_04]):]
            excel_item = excel_original_04.split('\r\n')[0].split('\t')

            try:
                if i < rank_count_04:   # 전년도 표
                    if i == rank_count_04-1: continue # '계' 제외
                    for j in range(1, 14): # 1월~12월 + 평균인원 (총 13개)
                        self.s4.table.item(i, j + 1).setText(excel_item[j])

                else:       # 당년도 표
                    if i == (rank_count_04*2)-1: continue # '계' 제외
                    for j in range(1, 14):
                        self.s4.table.item(i + 2, j + 1).setText(excel_item[j])

            except Exception as e:
                err_detail = f"S4 엑셀 입력 오류 [(3-2)직급별평균인원, 직급: {list_title_04[i%rank_count_04]}]: {e}"
                with open("log.txt", "a", encoding="utf-8") as f:                    
                    f.write(err_detail + "\n")
                print(err_detail)
                QMessageBox.information(self, "S4 엑셀 입력 오류", err_detail)
                return "excel_original_no" 




        self.s4.table.blockSignals(False)
        self.s4.table.viewport().update()












        # s5 ############################################################################

        list_title_05 = list(self.list_title_05)
        rank_count_05 = len(list_title_05)

        global check_nu
        global check_month_0708

        check_nu = False
        check_month_0708 = False

        if '\t누적\t누적차\t' in excel_original_05:
            check_nu = True

        if '7월\t\t\t\t\t8월' in excel_original_05 or '7월\t\t\t\t8월' in excel_original_05:
            check_month_0708 = True






        
        # print(repr(excel_original_05))


        self.s5.table.blockSignals(True)


        '''
        print(repr(excel_original_05))
        print(i)
        print(list_title_05)
        print(rank_count_05)
        '''

        if check_month_0708 and check_nu:
            print(7)
            for i in range(0, (rank_count_05)):
                print(list_title_05[i])
                print(i)
                
                try:
                    if i%rank_count_05 == rank_count_05-1: continue # '계' 행 제외
                    for j in range(1, 61): # 1월~12월
                        if j%5 == 3:   # 누적 제외
                            print(j)
                            continue
                            print(self.s5.table.item(i, j + 1))
                        self.s5.table.item(i, j + 1).setText(excel_item[j])



                except Exception as e:
                    err_detail = f"S5 엑셀 입력 오류 [(3-3)가.정원현원차이, 직급: {list_title_05[i%rank_count_05]}]: {e}"
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write(err_detail + "\n")
                    print(err_detail)
                    QMessageBox.information(self, "S5 엑셀 입력 오류", err_detail)
                    return "excel_original_no"







                


        else:
            for i in range(0, (rank_count_05*2)):

                try:
                    if i < rank_count_05:
                        if i%rank_count_05 == rank_count_05-1: continue # '계' 행 제외
                        for j in range(1, 25): # 1월~6월 (정/현/복/누 4개씩 6개월 = 24개)
                            self.s5.table.item(i, j + 1).setText(excel_item[j])
                    else:                  
                        if i == (rank_count_05*2)+1: continue # '계' 행 제외
                        for j in range(1, 25): # 7월~12월
                            self.s5.table.item(i+2, j + 1).setText(excel_item[j])


                except Exception as e:
                    err_detail = f"S5 엑셀 입력 오류 [(3-3)가.정원현원차이, 직급: {list_title_05[i%rank_count_05]}]: {e}"
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write(err_detail + "\n")
                    print(err_detail)
                    QMessageBox.information(self, "S5 엑셀 입력 오류", err_detail)
                    return "excel_original_no"
        return
















            

        for col_idx in range(2, 26):
            self.s5.calculate_s5(self.s5.table.item(0, col_idx))
            self.s5.calculate_s5(self.s5.table.item(rank_count_05+2, col_idx))

        if check_3_5:
            self.s11.sync_from_s5(self.s5.send_to_s11_from_s5())



        self.s5.table.blockSignals(False)
        self.s5.table.viewport().update()



        return

        # s7 ############################################################################

        list_title_07 = list(self.list_title_07)
        rank_count_07 = len(list_title_07)
        

        self.s7.table.blockSignals(True)

        # 8(전년도 1급)부터 14(전년도 연구직)까지 반복 (15번 '계' 자동 제외)
        for i in range(rank_count_07, (rank_count_07*2) - 1):
            try:
                excel_original_07 = excel_original_07[excel_original_07.find(list_title_07[i%rank_count_07]):]
                excel_item = excel_original_07.split('\r\n')[rank_count_07+2].split('\t')
                
                for j in range(1, 14): 
                    self.s7.table.item(i + 2, j + 1).setText(excel_item[j+1])

            except Exception as e:
                err_detail = f"S7 엑셀 입력 오류 [(3-3)다.증원인원, 직급: {list_title_07[i%rank_count_07]}]: {e}"
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(err_detail + "\n")
                print(err_detail)
                QMessageBox.information(self, "S7 엑셀 입력 오류", err_detail)
                return "excel_original_no" 

        self.s7.table.blockSignals(False)
        self.s7.table.viewport().update()





        # s8 ############################################################################


        list_title_08 = list(self.list_title_08)
        rank_count_08 = len(list_title_08)





        for i in range(0, (rank_count_08*2)):
            excel_original_08 = excel_original_08[excel_original_08.find(list_title_08[i%rank_count_08]):]
            excel_item = excel_original_08.split('\r\n')[0].split('\t')

            try:
                if i < rank_count_08:   # 전년도 표
                    for j in range(1, 13):
                        self.s8.table.item(i, j + 1).setText(excel_item[j])

                else:       # 당년도 표
                    for j in range(1, 13):
                        self.s8.table.item(i + 2, j + 1).setText(excel_item[j])

            except Exception as e:
                # 4. 예외 발생 시 3종 세트 알림 (S8 엑셀 입력 오류로 통일)
                err_detail = f"S8 엑셀 입력 오류 [(3-4)직급별평균단가, 직급: {list_title_08[i%rank_count_08]}]: {e}"
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(err_detail + "\n")
                print(err_detail)
                QMessageBox.information(self, "S8 엑셀 입력 오류", err_detail)
                return "excel_original_no"



        self.s8.table.blockSignals(False)
        self.s8.table.viewport().update()



        self.s8.calculate_s8(self.s8.table.item(0, 2))

        self.s8.sync_from_s4(self.s4.get_avg_data_to8())



        if check_3_5:
            self.s14.get_from_s8(self.s8.send_to_s14())


        # self.load_json('excel_input')

        # s9 ############################################################################



        if check_3_6:

            list_title_09 = list(self.list_title_09)
            rank_count_09 = len(list_title_09)

            self.s9.table.blockSignals(True)

            for i in range(0, (rank_count_09*2)):

                excel_original_09 = excel_original_09[excel_original_09.find(list_title_09[i%rank_count_09]):]
                excel_item = excel_original_09.split('\r\n')[0].split('\t')

                try:

                    if i < rank_count_09:   # 전년도 표
                        for j in range(1, 13): # 1월~12월 (j 인덱스 고정)
                            # i와 j+1 인덱스로 직접 입력
                            self.s9.table.item(i, j + 1).setText(excel_item[j])

                    else:       # 당년도 표
                        for j in range(1, 13):
                            self.s9.table.item(i + 2, j + 1).setText(excel_item[j])

                except Exception as e:
                    # 4. 예외 발생 시 상세 알림
                    err_detail = f"S9 엑셀 입력 오류 [(3-6)초임직급정원, 직급: {list_title_09[i%rank_count_09]}]: {e}"
                    with open("log.txt", "a", encoding="utf-8") as f:                    
                        f.write(err_detail + "\n")
                    print(err_detail)
                    QMessageBox.information(self, "S9 엑셀 입력 오류", err_detail)
                    return "excel_original_no" 

            self.s9.table.blockSignals(False)
            self.s9.table.viewport().update()







        # s11 ############################################################################

        if check_3_5:

            list_title_11 = list(self.list_title_11)
            rank_count_11 = len(list_title_11)

            self.s11.table.blockSignals(True)

            for i in range(0, (rank_count_11*2)):

                excel_original_11 = excel_original_11[excel_original_11.find(list_title_11[i%rank_count_11]):]
                excel_item = excel_original_11.split('\r\n')[0].split('\t')

                try:
                    if i < rank_count_11:
                        if i == rank_count_11-1: continue # '계' 행 제외                        
                        for j in range(1, 19): # 1월~6월 (정/현/복/누 4개씩 6개월 = 24개)
                            if j%3 == 1:
                                self.s11.table.item(i, j + 1).setText(excel_item[j])
                    else:
                        if i == (rank_count_11*2)-1: continue # '계' 행 제외
                        for j in range(1, 19): # 7월~12월
                            if j%3 == 1:
                                self.s11.table.item(i+2, j + 1).setText(excel_item[j])

                except Exception as e:
                    err_detail = f"S11 엑셀 입력 오류 [(3-5)가.별도직군 승진TO, 직급: {list_title_11[i%rank_count_11]}]: {e}"
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write(err_detail + "\n")
                    print(err_detail)
                    QMessageBox.information(self, "S11 엑셀 입력 오류", err_detail)
                    return "excel_original_no"


            for col_idx in range(1, 19):
                self.s11.calculate_s11(self.s11.table.item(0, col_idx))
                self.s11.calculate_s11(self.s11.table.item(rank_count_11+2, col_idx))

            self.s11.table.blockSignals(False)
            self.s11.table.viewport().update()






        # s12 ############################################################################


        if check_3_5:

            list_title_12 = list(self.list_title_12)
            rank_count_12 = len(list_title_12)

            self.s12.table.blockSignals(True)

            for i in range(0, (rank_count_12*2)):

                excel_original_12 = excel_original_12[excel_original_12.find(list_title_12[i%rank_count_12]):]
                excel_item = excel_original_12.split('\r\n')[0].split('\t')

                try:
                    if i < rank_count_12:
                        if i == rank_count_12-1: continue # '계' 행 제외                        
                        for j in range(1, 25): # 1월~6월 (정/현/복/누 4개씩 6개월 = 24개)
                            if j%4 == 2:
                                self.s12.table.item(i, j + 1).setText(excel_item[j])
                    else:
                        if i == (rank_count_12*2)-1: continue # '계' 행 제외
                        for j in range(1, 25): # 7월~12월
                            if j%4 == 2:
                                self.s12.table.item(i+2, j + 1).setText(excel_item[j])

                except Exception as e:
                    err_detail = f"S12 엑셀 입력 오류 [(3-5)나.미승진자 인원, 직급: {list_title_11[i%rank_count_11]}]: {e}"
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write(err_detail + "\n")
                    print(err_detail)
                    QMessageBox.information(self, "S12 엑셀 입력 오류", err_detail)
                    return "excel_original_no"


            self.s12.get_from_s11(self.s11.send_to_s12())
            for col_idx in range(1, 25):
                self.s12.calculate_s12(self.s12.table.item(0, col_idx))                
                self.s12.calculate_s12(self.s12.table.item(rank_count_12+2, col_idx))
            






            self.s12.table.blockSignals(False)
            self.s12.table.viewport().update()















        # s13 ############################################################################



        if check_3_5:

            list_title_13 = list(self.list_title_13)
            rank_count_13 = len(list_title_13)

            self.s13.table.blockSignals(True)

            for i in range(0, (rank_count_13*2)):

                excel_original_13 = excel_original_13[excel_original_13.find(list_title_13[i%rank_count_13]):]
                excel_item = excel_original_13.split('\r\n')[0].split('\t')


                try:
                    if i < rank_count_13:   # 전년도 표
                        if i == rank_count_13-1: continue # '계' 행 제외

                        for j in range(1, 13): # 1월~12월 (j 인덱스 고정)
                            # i와 j+1 인덱스로 직접 입력
                            self.s13.table.item(i, j + 1).setText(excel_item[j])

                    else:       # 당년도 표
                        if i == (rank_count_13*2)-1: continue # '계' 행 제외

                        for j in range(1, 13):
                            self.s13.table.item(i + 2, j + 1).setText(excel_item[j])

                except Exception as e:
                    err_detail = f"S13 엑셀 입력 오류 [(3-5)다.미승진자 평균인원, 직급: {list_title_11[i%rank_count_11]}]: {e}"
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write(err_detail + "\n")
                    print(err_detail)
                    QMessageBox.information(self, "S13 엑셀 입력 오류", err_detail)
                    return "excel_original_no"



            
            for col_idx in range(2, 14):
                self.s13.calculate_s13(self.s13.table.item(0, col_idx))
                self.s13.calculate_s13(self.s13.table.item(rank_count_13+2, col_idx))
            self.s12.get_from_s13(self.s13.send_to_s12())
            self.s14.get_from_s13(self.s13.send_to_s14())
            


            



            

            self.s13.table.blockSignals(False)
            self.s13.table.viewport().update()






        # 각 페이지 계산   ############################################################################



        self.load_json('excel_input')






if __name__ == "__main__":
    path = os.path.join(os.path.dirname(PyQt5.__file__), "Qt5", "plugins")
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = path


    app = QApplication(sys.argv)
    app.setFont(QFont("맑은 고딕", 9))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
