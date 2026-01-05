import sys
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




# --- 1. 파란색 하이라이트 전용 메뉴 클래스 ---
class CustomMenu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 테두리 없고 최상단 팝업 설정
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        
        # QPushButton:hover를 이용해 파란 배경 강제 적용
        self.setStyleSheet("""
            QDialog { 
                background-color: white; 
                border: 1px solid #888888; 
            }
            QPushButton { 
                border: none; 
                text-align: left; 
                padding: 8px 25px; 
                background-color: white; 
                color: black;
            }
            QPushButton:hover { 
                background-color: #0078d7; 
                color: white; 
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)

        # 메뉴 버튼 (참조하신 스타일 유지)
        self.btn_copy = QPushButton("복사 (Ctrl+C)")
        self.btn_paste = QPushButton("붙여넣기 (Ctrl+V)")
        
        layout.addWidget(self.btn_copy)
        layout.addWidget(self.btn_paste)

        # 클릭 시 메뉴 닫기 (결과값 반환)
        self.btn_copy.clicked.connect(self.accept)
        self.btn_paste.clicked.connect(self.reject)






import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, 
                             QTextEdit, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor

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
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)

        # 1. 상단 버튼바 (간격 최소화: spacing=2)
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(2) # 버튼 사이 간격을 2픽셀로 고정
        layout.addLayout(nav_layout)
        


        # 엑셀 버튼
        '''
        btn_excel = QPushButton("Excel 내보내기")
        btn_excel.setStyleSheet("""
            QPushButton {
                background-color: #217346; color: white; border-radius: 2px;
                padding: 3px 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #1a5a37; }
        """)
        nav_layout.addWidget(btn_excel)
        layout.addLayout(nav_layout)
        '''

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


        sheet_names = {
            1: "(2)인건비집계", 2: "(3)총인건비인상률", 3: "(3-1)증원소요인건비", 4: "(3-2)직급별평균인원", 5: "(3-3)근속및증원", 
            6: "나.근속승진", 7: "다.증원", 8: "(3-4)직급별단가", 9: "(3-6)초임직급", 10: "나.인건비효과",
            11: "(3-5)가.별도직군", 12: "(3-5)나.인원", 13: "(3-5)다.미승진자", 14: "(3-5)라.인건비효과",
            15: "(4)노동생산성", 16: "(6)일반관리비", 17: "4.총보수", 18: "직무급"
        }
        
        
        # 각 번호에 맞는 시트 클래스를 연결
        for i in range(1, 19):

            if i == 1:
                self.s1 = Sheet1Page()
                page = self.s1
            elif i == 2:
                self.s2 = Sheet2Page()
                page = self.s2
            elif i == 3:
                self.s3 = Sheet3Page()
                page = self.s3
            elif i == 4:
                self.s4 = Sheet4Page(self)
                page = self.s4
            elif i == 5:
                self.s5 = Sheet5Page()
                page = self.s5
            elif i == 6:
                self.s6 = Sheet6Page()
                page = self.s6
            elif i == 7:
                self.s7 = Sheet7Page()
                page = self.s7
            elif i == 8:
                self.s8 = Sheet8Page()
                page = self.s8
            elif i == 9:
                self.s9 = Sheet9Page(self)
                page = self.s9
            elif i == 10:
                self.s10 = Sheet10Page()
                page = self.s10
            elif i == 11:
                self.s11 = Sheet11Page()
                page = self.s11
            elif i == 12:
                self.s12 = Sheet12Page()
                page = self.s12
            elif i == 13:
                self.s13 = Sheet13Page()
                page = self.s13
            elif i == 14:
                self.s14 = Sheet14Page()
                page = self.s14
            elif i == 15:
                self.s15 = Sheet15Page()
                page = self.s15
            elif i == 16:
                self.s16 = Sheet16Page()
                page = self.s16
            elif i == 17:
                self.s17 = Sheet17Page()
                page = self.s17
            elif i == 18:
                self.s18 = Sheet18Page()
                page = self.s18
            else:
                page = QWidget() # 나머지는 아직 빈 페이지






                
                
            # self.tabs.addTab(page, f"Sheet{i}")
            self.tabs.addTab(page, sheet_names.get(i, f"Sheet{i}"))


        self.tabs.setCurrentIndex(0)
        layout.addWidget(self.tabs)



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










        self.s5.table.itemChanged.connect(lambda: self.s6.sync_from_s5(self.s5.get_data_for_s6()))
        self.s6.table.itemChanged.connect(lambda: self.s7.sync_s7_data(self.s4.get_data_to7(), self.s6.get_data_to7()))


        
        


        def on_s4_changed():
            # 1. S4에서 평균 데이터를 가져와 S8 업데이트
            self.s8.sync_from_s4(self.s4.get_avg_data_to8())
            
            # 2. 업데이트된 S8의 단가를 S3(갑)와 S10(을)에 즉시 반영 (중요!)
            # S3(갑) 업데이트
            self.s3.sync_unit_price_from_s8(self.s8.get_unit_price_to3())
            self.s2.sync_from_s3(self.s3.get_gab_to_s2())
            
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

        # --- [2] S9(데이터) -> S10 -> S2 (을 전송) ---
        self.s9.table.itemChanged.connect(lambda: [
            self.s10.sync_from_s9(self.s9.get_data_to10()),
            self.s10.calculate_s10(), 
            self.s2.sync_eul_from_s10(self.s10.get_eul_to_s2())
        ])

        # --- [3] S8(단가)은 S3(갑)와 S10(을) 모두에 영향을 주므로 통합 처리 ---
        def on_s8_changed(item):
            # 단가와 관련된 열(2~13열, 15열)이 바뀔 때만 작동
            if 2 <= item.column() <= 13 or item.column() == 15:
                # 1. S3(갑) 업데이트 및 S2 전송
                self.s3.sync_unit_price_from_s8(self.s8.get_unit_price_to3())
                self.s2.sync_from_s3(self.s3.get_gab_to_s2())
                
                # 2. S10(을) 업데이트 및 S2 전송
                self.s10.sync_unit_price_from_s8(self.s8.get_unit_price_to10())
                self.s10.calculate_s10()
                self.s2.sync_eul_from_s10(self.s10.get_eul_to_s2())

        self.s8.table.itemChanged.connect(on_s8_changed)



        self.s1.table.itemChanged.connect(lambda: self.s2.sync_from_s1(self.s1.get_data_to_s2()))
        
        self.s3.table.itemChanged.connect(lambda item: self.s2.sync_from_s3(self.s3.get_gab_to_s2()))
        self.s10.table.itemChanged.connect(lambda item: self.s2.sync_eul_from_s10(self.s10.get_eul_to_s2()))


        self.run_verification()






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

        if data != 'excel_input':

            path, _ = QFileDialog.getOpenFileName(self, "데이터 불러오기", os.getcwd(), "JSON Files (*.json)")
            if not path: return

        try:

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
                            active_rows = list(range(0, 8)) + list(range(11, 19))
                            
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
                                t1, t2 = table.item(7, c), table.item(18, c)
                                try:
                                    if t1: calc_func(t1)
                                    if t2: calc_func(t2)
                                except: pass

                        elif calc_func.__name__ == "calculate_s4":
                            s4_rank = 8 
                            # 데이터 행만 순회 (0~6, 11~17)
                            active_rows = list(range(0, s4_rank - 1)) + list(range(s4_rank + 3, s4_rank + 3 + s4_rank - 1))
                            
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
                                for base_r in [0, s4_rank + 3]:
                                    if base_r < table.rowCount():
                                        trigger_it = table.item(base_r, c)
                                        if trigger_it:
                                            try: calc_func(trigger_it)
                                            except: pass

                            self.s8.sync_from_s4(self.s4.get_avg_data_to8())                                




                        elif calc_func.__name__ == "calculate_s5":
                            # rank_count = 8 기준 (0~7행 데이터, 8행 계 / 11~18행 데이터, 19행 계)
                            s5_rank = 8 
                            
                            # 1. 누적차 및 합계 트리거링할 행 (각 표의 첫 번째 데이터 행만 찔러도 전체 계산됨)
                            # 하지만 안전하게 데이터가 있는 첫 행인 0행과 11행만 사용
                            rows_to_trigger = [0, s5_rank + 3] # [0, 11]
                            
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










                        elif calc_func.__name__ in ["calculate_s7", "calculate_s8"]:
                        # elif "s7" in sheet_name or "s8" in sheet_name:
                            # 7번 시트 특성: 1~12월 데이터를 기반으로 14열(평균)과 8행/19행(합계) 계산
                            # 표 1: 0~7행 데이터, 8행 합계 / 표 2: 11~18행 데이터, 19행 합계
                            
                            # 1. 모든 데이터 행에 대해 '가로 평균' 계산 트리거
                            active_rows = list(range(0, 8)) + list(range(11, 19))
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
                                t2 = table.item(11, c)
                                if t2:
                                    try: calc_func(t2)
                                    except: pass

                            if calc_func.__name__ in ["calculate_s8"]:
                                self.s3.sync_unit_price_from_s8(self.s8.get_unit_price_to3())
                                self.s2.sync_from_s3(self.s3.get_gab_to_s2())                                
                                self.s10.sync_unit_price_from_s8(self.s8.get_unit_price_to10())










                                    

                        elif calc_func.__name__ == "calculate_s9":
                            # 데이터 행: 표1(0~7), 표2(11~18)
                            active_rows = list(range(0, 8)) + list(range(11, 19))
                            
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
                                t1, t2 = table.item(7, c), table.item(18, c)
                                try:
                                    if t1: calc_func(t1)
                                    if t2: calc_func(t2)
                                except: pass


                            self.s10.sync_from_s9(self.s9.get_data_to10())
                            self.s10.calculate_s10()
                            self.s2.sync_eul_from_s10(self.s10.get_eul_to_s2())


                                

                        elif calc_func.__name__ == "calculate_s10":
                            # 1. 가로 연산 (증감C, 효과E) 및 기본 합계 트리거
                            for r in range(8):
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











    def run_verification(self):

        current_index = self.tabs.currentIndex()+1

        

        
        try:
            # if self.rpa(current_index) in ["Excel", "excel_original_no"]:
            #    return

            '''
            if self.rpa(1) in ["Excel", "excel_original_no"]: return
            if self.rpa(2) in ["Excel", "excel_original_no"]: return
            if self.rpa(3) in ["Excel", "excel_original_no"]: return
            if self.rpa(4) in ["Excel", "excel_original_no"]: return
            if self.rpa(5) in ["Excel", "excel_original_no"]: return
            if self.rpa(6) in ["Excel", "excel_original_no"]: return
            if self.rpa(7) in ["Excel", "excel_original_no"]: return
            '''


            import win32com.client as win32
            # 1. PyQt5 앱 실행 (이미 앱이 실행 중이면 QApplication.instance() 사용)
            app = QApplication.instance() or QApplication(sys.argv)

            # 2. 파일 선택 창 (PyQt5 스타일)
            selected_file, _ = QFileDialog.getOpenFileName(None, "엑셀 파일을 선택하세요", "", "Excel Files (*.xlsx *.xls *.xlsm)")

            if not selected_file:
                print("파일 선택이 취소되었습니다.")
                sys.exit()
                return 'Excel'

            # 3. 엑셀 조종 (이후는 동일)
            excel = win32.Dispatch("Excel.Application")
            file_path = os.path.abspath(selected_file)
            wb = excel.Workbooks.Open(file_path, False, True, None, '00258')

            def get_repr(ws):
                data = ws.UsedRange.Value
                if not data: return "''"
                txt = "".join(["\t".join([str(i) if i is not None else "" for i in row]) + "\r\n" for row in data])
                return repr(txt).replace('\\t', '\t').replace('\\n', '\n').replace('\\r', '\r').replace(' ', '').replace('\t-\t', '\t\t')

            global excel_original01, excel_original02, excel_original03, excel_original04, excel_original05, excel_original06, excel_original07

            excel_original01 = get_repr(wb.Sheets(1))
            excel_original02 = get_repr(wb.Sheets(2))
            excel_original03 = get_repr(wb.Sheets(3))
            excel_original04 = get_repr(wb.Sheets(4))
            excel_original05 = get_repr(wb.Sheets(5))
            excel_original06 = get_repr(wb.Sheets(6))
            excel_original07 = get_repr(wb.Sheets(7))


            def data(self, role):
                if role == Qt.ForegroundRole:
                    val = super().data(Qt.EditRole)
                    try:
                        if val is not None and float(str(val).replace(',', '')) < 0:
                            return QColor(Qt.red)
                    except:
                        pass
                    return super().data(role) # 음수가 아니면 기본 색상
                


            '''
            ¤£²¥ ¦§¨© ™š›œ ¡¢£¤ ¥¦§¨ ©ª«¬ ®¯°± ²³´µ ¶·¸¹ º»¼½ ¾¿ÀÁ ÂÃÄÅ ÆÇÈÉ ÊËÌÍ
            ÎÏÐÑ ÒÓÔÕ Ö×ØÙ ÚÛÜÝ Þßàá âãäå æçèé êëìí îïðñ òóôõ ö÷øù úûüý þÿ
            !@$%^&*()_+ ºÅ° °ªÀÌ ¾Æ´Ñ µ¥ÀÌÅÍ°¡ Æ÷Ç

            암호화: "기본급" → Êþº¾¤£ (사람이 읽을 수 없음)

            복호화: Êþº¾¤£ → "기본급" (DRM 엔진이 다시 계산해서 돌려줌)

            '''




            
            
            wb.Close(False)
            excel.Quit()


















        except Exception as e:
            import traceback
            error_details = traceback.format_exc()            
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] RPA 오류: " + str(current_index) + "번 표\n")
                f.write(f"{error_details}\n\n")
                print(error_details)
                QMessageBox.information(self, "RPA 오류: " + str(current_index) + "번 표", "RPA 오류: " + str(current_index) + "번 표\n\n해결되지 않는 경우, log.txt를 경영정보부로 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")

            
            print(f"\n[!] 오류: {e}")
            return





        
        self.excel_input()


        
        try:
            str_err = self.compare(current_index)

            if not str_err:
                print("엑셀 데이터가 확보되지 않았습니다. [" + str(current_index) + "번 표]")

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(error_details)
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] Compare 오류: " + str(current_index) + "번 표\n")
                f.write(f"{error_details}\n\n")
                if current_index == 4: f.write(str(excel_original04.split('당년도')))
                if current_index == 5: f.write(str(excel_original05.split('나.근속승진')))
                if current_index == 6: f.write(str(excel_original05.split('나.근속승진')))
                if current_index == 7: f.write(str(excel_original05.split('다.증원소요인건비대상인원')))
                if current_index == 8: f.write(str(excel_original06.split('당년도')))
                if current_index == 9: f.write(str(excel_original07.split('나.초임직급정원변동에따른인건비효과')))
                if current_index == 10: f.write(str(excel_original07.split('나.초임직급정원변동에따른인건비효과')))                
                QMessageBox.information(self, "RPA 오류: " + str(current_index) + "번 표", "엑셀과 프로그램 데이터 비교 오류: " + str(current_index) + "번 표\n\n해결되지 않는 경우, log.txt를 경영정보부로 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
            
            print(f"\n[!] 오류: {e}")
            return


        
        win_verify = VerificationResultWindow(self)   # 1. 검증 창 인스턴스 생성
        
        result_text = "-------------------------------------\n"
        result_text += "    인건비 집계 정합성 검증    \n"
        result_text += "-------------------------------------\n\n"
        result_text += str_err
        
        win_verify.set_content(result_text)   # 3. 텍스트 박스에 내용 설정
        win_verify.exec_()
        


























    def text_table(self, r, c):
        return self.tabs.currentWidget().table.item(r, c).text()


    def table_str(self, p, r, c):

        if not self.tabs.currentWidget().table.item(r, c) or self.tabs.currentWidget().table.item(r, c).text() in ['', '-', 'n/a']:
            if (p in [1, 8]) or (p == 9 and c != 14) or (p in [3, 10] and c in [4, 5]) or (p == 2 and r not in [43, 44]):
                return '0'
            elif p == 2 and r in [43, 44]:
                return '0.000'
            elif (p == 3 and c in [1, 2, 3]) or (p in [5, 6]) or (p == 7 and c != 14):
                return '0.0'
            else:
                return '0.00'
            return '0'
        # return self.tabs.currentWidget().table.item(r, c).text().replace('%', '')
        return self.tabs.widget(p-1).table.item(r, c).text().replace('%', '')


    def excel_str(self, text, p, r, c):

        if not text or text.strip() in ['-', '']:
            if (p in [1, 8]) or (p == 9 and c != 13) or (p in [3, 10] and c in [4, 5]) or (p == 2 and r not in [43, 44]):
                return '0'
            elif p == 2 and r in [43, 44]:
                return '0.000'
            elif (p == 3 and c in [1, 2, 3]) or (p in [5, 6]) or (p == 7 and c != 13):
                return '0.0'
            else:
                return '0.00'
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


        global excel_original01, excel_original02, excel_original03, excel_original04, excel_original05, excel_original06, excel_original07




        if current_index == 1:

            open_found = False

            for item in gw.getAllWindows():
                if item.title.startswith('★2024년도 계량지표_총인건비'):
                    win = item

                    if win.isMinimized:
                        win.restore()
                    
                    app = Application().connect(handle=win._hWnd)
                    target_win = app.window(handle=win._hWnd)

                    try:
                        target_win.set_focus()
                    except Exception:
                        win32functions.ShowWindow(win._hWnd, 9)
                        win32functions.SetForegroundWindow(win._hWnd)

                    # target_win.click_input(coords=(100, 10))
                    open_found = True
                    time.sleep(0.5)
                
            if not open_found:
                QMessageBox.information(self, "엑셀 파일을 열어주세요.", "★2024년도 계량지표_총인건비~ 엑셀 파일을 직접 열어주세요.\n\n기밀 문서라서 로봇이 자동으로 엑셀 데이터를 가져올 수 없습니다.\n파일에 걸린 암호를 RPA로 푸는 것은 보안 정책 위반이므로 직접 열어주세요.")
                return "Excel"

                '''
                try:
                    # 현재 폴더에서 해당 파일 찾기
                    target_file = [f for f in os.listdir('.') if f.startswith('★2024년도 계량지표_총인건비')][0]
                    os.startfile(target_file)
                    
                    # 파일이 열리고 창이 나타날 때까지 대기 (최대 10초)
                    for _ in range(20):
                        time.sleep(0.5)
                        for item in gw.getAllWindows():
                            if item.title.startswith('★2024년도 계량지표_총인건비'):
                                win = item
                                open_found = True
                                break
                        if open_found: 
                            # 창을 찾은 직후, '복구 팝업' 방지를 위해 ESC 입력
                            time.sleep(1) # 엑셀 로딩 대기
                            keyboard.press_and_release('esc') 
                            
                            # 다시 한번 포커스 잡아주기
                            app = Application().connect(handle=win._hWnd)
                            target_win = app.window(handle=win._hWnd)
                            target_win.set_focus()

                            target_win.click_input(coords=(100, 10))
                            break
                except IndexError:
                    QMessageBox.critical(self, "파일 오류", "현재 경로에 ★2024년도 계량지표_총인건비~ 엑셀 파일이 없습니다.\n\n이 파일을 run.bat와 같은 폴더에 놓으시면 열 수 있습니다.")
                    return
                '''
                    

            time.sleep(1)        
            keyboard.press_and_release('win + up')


            time.sleep(2)
            keyboard.press_and_release('ctrl + pageup')
            keyboard.press_and_release('ctrl + pageup')
            keyboard.press_and_release('ctrl + pageup')
            keyboard.press_and_release('ctrl + pageup')
            keyboard.press_and_release('ctrl + pageup')
            keyboard.press_and_release('ctrl + pageup')
            keyboard.press_and_release('ctrl + pageup')
            keyboard.press_and_release('ctrl + pageup')
            keyboard.press_and_release('ctrl + pageup')
            keyboard.press_and_release('ctrl + pageup')

        time.sleep(2)

        if current_index != 1:
            keyboard.press_and_release('ctrl + pagedown')

        '''
        if current_index in [2]:
            keyboard.press_and_release('ctrl + pagedown')
        if current_index in [3]:
            for i in range(2): keyboard.press_and_release('ctrl + pagedown')

        if current_index in [4]:
            for i in range(3): keyboard.press_and_release('ctrl + pagedown')

        if current_index in [5, 6, 7]:
            for i in range(4): keyboard.press_and_release('ctrl + pagedown')

        if current_index in [8]:
            for i in range(5): keyboard.press_and_release('ctrl + pagedown')

        if current_index in [9, 10]:
            for i in range(6): keyboard.press_and_release('ctrl + pagedown')

        time.sleep(0.3)
        '''

        mouse = Controller()

        '''
        if current_index >= 5 or current_index in [1, 2]:
            mouse.position = (1500, 880)
        else:
            mouse.position = (70, 800)
        '''

        mouse.position = (1500, 880)
        mouse.click(Button.left, 1)

        time.sleep(1)
        keyboard.press_and_release('ctrl + a')
        time.sleep(1)
        keyboard.press_and_release('ctrl + c')
        time.sleep(1)




        # global excel_original01, excel_original02, excel_original03, excel_original04, excel_original05, excel_original06, excel_original07

        from PyQt5.QtCore import QThread

        if current_index == 1:

            QThread.msleep(300)
            for _ in range(10):
                try:
                    excel_original01 = pyperclip.paste()
                    if excel_original01: break  # 데이터를 가져오면 루프 탈출
                except:
                    QThread.msleep(100)  # 에러 발생 시 0.1초 대기 후 재시도



            time.sleep(0.5)

            
            excel_original01 = excel_original01.replace(' ', '').replace('\t-\t', '\t\t')

            if not excel_original01 or excel_original01[0:2] not in ['(2', '(3']:
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] 엑셀 데이터를 확보하지 못했습니다.\n")
                    if not excel_original01:
                        f.write("excel_original01: None\n\n")
                    else:
                        f.write("excel_original01: " + repr(excel_original01[:30])  + '\n\n')

                screen = QApplication.primaryScreen()
                screenshot = screen.grabWindow(0) # 전체 화면 캡처
                screenshot.save("log.jpg", "jpg")

                # win.minimize()
                QMessageBox.information(self, "엑셀 데이터를 확보하지 못했습니다.", "(2) 인건비 집계\n\n엑셀 파일이 제대로 열렸는지 확인해주세요.\n엑셀 양식이 변경되었는지 확인해주세요.\n\n해결되지 않는 경우, log.txt, log.jpg 를 경영정보부로 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
                return "excel_original_no"
            
        if current_index == 2:

            QThread.msleep(300)
            for _ in range(10):
                try:
                    excel_original02 = pyperclip.paste()
                    if excel_original02: break  # 데이터를 가져오면 루프 탈출
                except:
                    QThread.msleep(100)  # 에러 발생 시 0.1초 대기 후 재시도
                    
            
            excel_original02 = excel_original02.replace(' ', '').replace('\t-\t', '\t\t')
            time.sleep(0.5)

            if not excel_original02 or excel_original02[0:2] not in ['(2', '(3']:
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] 엑셀 데이터를 확보하지 못했습니다.\n")
                    if not excel_original02:
                        f.write("excel_original02: None\n\n")
                    else:
                        f.write("excel_original02: " + repr(excel_original02[:100]) + '\n\n')

                screen = QApplication.primaryScreen()
                screenshot = screen.grabWindow(0) # 전체 화면 캡처
                screenshot.save("log.jpg", "jpg")

                # win.minimize()
                QMessageBox.information(self, "엑셀 데이터를 확보하지 못했습니다.", "(3) 총인건비 인상률\n\n엑셀 파일이 제대로 열렸는지 확인해주세요.\n엑셀 양식이 변경되었는지 확인해주세요.\n\n해결되지 않는 경우, log.txt, log.jpg 를 경영정보부로 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
                return "excel_original_no"            
            
        if current_index == 3:

            QThread.msleep(300)
            for _ in range(10):
                try:
                    excel_original03 = pyperclip.paste()
                    if excel_original03: break  # 데이터를 가져오면 루프 탈출
                except:
                    QThread.msleep(100)  # 에러 발생 시 0.1초 대기 후 재시도

            
            excel_original03 = excel_original03.replace(' ', '').replace('\t-\t', '\t\t')
            time.sleep(0.5)
            
            
            if not excel_original03 or excel_original03[0:2] not in ['(2', '(3']:
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] 엑셀 데이터를 확보하지 못했습니다.\n\n")
                    if not excel_original03:
                        f.write("excel_original03: None\n\n")
                    else:
                        f.write("excel_original03: " + repr(excel_original03[:100]) + '\n\n')

                screen = QApplication.primaryScreen()
                screenshot = screen.grabWindow(0) # 전체 화면 캡처
                screenshot.save("log.jpg", "jpg")

                # win.minimize()
                QMessageBox.information(self, "엑셀 데이터를 확보하지 못했습니다.", "(3-1) 증원소요 인건비\n\n엑셀 파일이 제대로 열렸는지 확인해주세요.\n엑셀 양식이 변경되었는지 확인해주세요.\n\n해결되지 않는 경우, log.txt, log.jpg 를 경영정보부로 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
                return "excel_original_no" 

            
            
        if current_index == 4:

            QThread.msleep(300)
            for _ in range(10):
                try:
                    excel_original04 = pyperclip.paste()
                    if excel_original04: break  # 데이터를 가져오면 루프 탈출
                except:
                    QThread.msleep(100)  # 에러 발생 시 0.1초 대기 후 재시도          

            
            excel_original04 = excel_original04.replace(' ', '').replace('\t-\t', '\t\t')
            time.sleep(0.5)

            if not excel_original04 or excel_original04[0:2] not in ['(2', '(3']:
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] 엑셀 데이터를 확보하지 못했습니다.\n\n")
                    if not excel_original04:
                        f.write("excel_original04: None\n\n")
                    else:
                        f.write("excel_original04: " + repr(excel_original04[:100]) + '\n\n')

                screen = QApplication.primaryScreen()
                screenshot = screen.grabWindow(0) # 전체 화면 캡처
                screenshot.save("log.jpg", "jpg")

                # win.minimize()
                QMessageBox.information(self, "엑셀 데이터를 확보하지 못했습니다.", "(3-2) 직급별 평균 인원\n\n엑셀 파일이 제대로 열렸는지 확인해주세요.\n엑셀 양식이 변경되었는지 확인해주세요.\n\n해결되지 않는 경우, log.txt, log.jpg 를 경영정보부로 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
                return "excel_original_no" 
            
            
        if current_index in [5, 6, 7]:

            QThread.msleep(300)
            for _ in range(10):
                try:
                    excel_original05 = pyperclip.paste()
                    if excel_original05: break  # 데이터를 가져오면 루프 탈출
                except:
                    QThread.msleep(100)  # 에러 발생 시 0.1초 대기 후 재시도


            
            excel_original05 = excel_original05.replace(' ', '').replace('\t-\t', '\t\t')
            time.sleep(0.5)
            
            if not excel_original05 or excel_original05[0:2] not in ['(2', '(3']:
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] 엑셀 데이터를 확보하지 못했습니다.\n\n")
                    if not excel_original05:
                        f.write("excel_original05: None\n\n")
                    else:
                        f.write("excel_original05: " + repr(excel_original05[:100]) + '\n\n')

                screen = QApplication.primaryScreen()
                screenshot = screen.grabWindow(0) # 전체 화면 캡처
                screenshot.save("log.jpg", "jpg")

                # win.minimize()
                QMessageBox.information(self, "엑셀 데이터를 확보하지 못했습니다.", "(3-3) 근속 및 증원\n\n엑셀 파일이 제대로 열렸는지 확인해주세요.\n엑셀 양식이 변경되었는지 확인해주세요.\n\n해결되지 않는 경우, log.txt, log.jpg 를 경영정보부로 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
                return "excel_original_no" 

            
            
        if current_index == 8:

            QThread.msleep(300)
            for _ in range(10):
                try:
                    excel_original06 = pyperclip.paste()
                    if excel_original06: break  # 데이터를 가져오면 루프 탈출
                except:
                    QThread.msleep(100)  # 에러 발생 시 0.1초 대기 후 재시도



            excel_original06 = excel_original06.replace(' ', '').replace('\t-\t', '\t\t')
            time.sleep(0.5)
            
            if not excel_original06 or excel_original06[0:2] not in ['(2', '(3']:
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] 엑셀 데이터를 확보하지 못했습니다.\n\n")
                    if not excel_original07:
                        f.write("excel_original06: None\n\n")
                    else:
                        f.write("excel_original06: " + repr(excel_original06[:100]) + '\n\n')

                screen = QApplication.primaryScreen()
                screenshot = screen.grabWindow(0) # 전체 화면 캡처
                screenshot.save("log.jpg", "jpg")

                # win.minimize()
                QMessageBox.information(self, "엑셀 데이터를 확보하지 못했습니다.", "(3-4) 증원소요 인건비\n\n엑셀 파일이 제대로 열렸는지 확인해주세요.\n엑셀 양식이 변경되었는지 확인해주세요.\n\n해결되지 않는 경우, log.txt, log.jpg 를 경영정보부로 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
                return "excel_original_no" 


            
            
        if current_index in [9, 10]:

            QThread.msleep(300)
            for _ in range(10):
                try:
                    excel_original07 = pyperclip.paste()
                    if excel_original07: break  # 데이터를 가져오면 루프 탈출
                except:
                    QThread.msleep(100)  # 에러 발생 시 0.1초 대기 후 재시도




            
            excel_original07 = excel_original07.replace(' ', '').replace('\t-\t', '\t\t')
            time.sleep(0.5)
            
            if not excel_original07 or excel_original07[0:2] not in ['(2', '(3']:
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now().strftime('%m/%d %H:%M')}] 엑셀 데이터를 확보하지 못했습니다.\n\n")
                    if not excel_original07:
                        f.write("excel_original07: None\n\n")
                    else:
                        f.write("excel_original07: " + repr(excel_original07[:100]) + '\n\n')

                screen = QApplication.primaryScreen()
                screenshot = screen.grabWindow(0) # 전체 화면 캡처
                screenshot.save("log.jpg", "jpg")

                # win.minimize()
                QMessageBox.information(self, "엑셀 데이터를 확보하지 못했습니다.", "(3-6) 초임직급\n\n엑셀 파일이 제대로 열렸는지 확인해주세요.\n엑셀 양식이 변경되었는지 확인해주세요.\n\n해결되지 않는 경우, log.txt, log.jpg 를 경영정보부로 보내주세요.\n\n(run.bat와 같은 폴더에 위치)")
                return "excel_original_no" 

            
            
        time.sleep(1)

        keyboard.press_and_release('right')
        time.sleep(0.5)
        keyboard.press_and_release('esc')
        time.sleep(0.5)




        if current_index == 9:
            for item in gw.getAllWindows():
                if item.title.startswith('★2024년도 계량지표_총인건비'):
                    win = item
            win.minimize()












        """
        global excel_original01, excel_original02, excel_original03, excel_original04, excel_original05, excel_original06, excel_original07
        
        excel_original01 = '(2) 인건비 집계를 위한 Template\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t(단위: 원)\r\n인건비 항목\t\t\t판관비\t영업외비용\t 제조원가\t타계정대체\t이익잉여금\t합계\r\n"급료\n임금\n제수당"\t기본급\t\t 744,433,839,400 \t\t\t\t\t 744,433,839,400 \r\n\t상여금\t인센티브 상여금\t 50,727,850,151 \t\t\t\t\t 50,727,850,151 \r\n\t\t그 외 상여금\t 48,367,494,910 \t\t\t\t\t 48,367,494,910 \r\n\t제수당\t법정수당\t 66,931,057,610 \t\t\t\t\t 66,931,057,610 \r\n\t\t해외근무수당\t 50,000,000 \t\t\t\t\t 50,000,000 \r\n\t\t그 외 제수당\t 202,750,281,360 \t\t\t\t\t 202,750,281,360 \r\n\t퇴직급여(명예퇴직금 포함)\t\t 168,793,866,818 \t\t\t\t\t 168,793,866,818 \r\n\t임원 인건비\t\t 983,482,250 \t\t\t\t\t 983,482,250 \r\n\t비상임이사 인건비\t\t 600,000,000 \t\t\t\t\t 600,000,000 \r\n\t"인상률 제외\n인건비"\t통상임금소송결과에 따른 실적급여 증가액\t 70,000,000 \t\t\t\t\t 70,000,000 \r\n\t\t기타 제외 인건비\t 8,000,000 \t\t\t\t\t 8,000,000 \r\n\t기타항목\t\t 74,870,000 \t\t\t\t\t 74,870,000 \r\n\t급료, 임금, 제수당 소계 ⓐ\t\t 1,283,790,742,499 \t - \t - \t - \t - \t 1,283,790,742,499 \r\n"복 리\n후생비"\t사내근로복지기금출연금\t\t 700,000,000 \t\t\t\t\t 700,000,000 \r\n\t국민연금사용자부담분\t\t 38,566,372,740 \t\t\t\t\t 38,566,372,740 \r\n\t건강보험사용자부담분\t\t 41,634,941,020 \t\t\t\t\t 41,634,941,020 \r\n\t고용보험사용자부담분\t\t 18,164,674,530 \t\t\t\t\t 18,164,674,530 \r\n\t산재보험료사용자부담분\t\t 5,325,440,550 \t\t\t\t\t 5,325,440,550 \r\n\t급식비\t\t 700,000,000 \t\t\t\t\t 700,000,000 \r\n\t교통보조비\t\t 800,000,000,000 \t\t\t\t\t 800,000,000,000 \r\n\t자가운전보조금\t\t 60,000,000 \t\t\t\t\t 60,000,000 \r\n\t학자보조금\t\t 49,525,720 \t\t\t\t\t 49,525,720 \r\n\t건강진단비 등(독감예방주사비용)\t\t 173,882,997 \t\t\t\t\t 173,882,997 \r\n\t선택적복지\t\t 9,194,447,060 \t\t\t\t\t 9,194,447,060 \r\n\t행사비\t\t 700,000,000 \t\t\t\t\t 700,000,000 \r\n\t포상품(비)\t\t 52,602,620 \t\t\t\t\t 52,602,620 \r\n\t기념품(비)\t\t 80,000,000 \t\t\t\t\t 80,000,000 \r\n\t격려품(비)\t\t 7,000,000 \t\t\t\t\t 7,000,000 \r\n\t장기근속관련 비용\t\t 8,000,000 \t\t\t\t\t 8,000,000 \r\n\t육아보조비 및 출산장려금\t\t 743,000,000 \t\t\t\t\t 743,000,000 \r\n\t자기계발비\t\t 80,000,000 \t\t\t\t\t 80,000,000 \r\n\t특별근로의 대가\t\t 8,000,000 \t\t\t\t\t 8,000,000 \r\n\t피복비\t\t 700,000,000 \t\t\t\t\t 700,000,000 \r\n\t경로효친비\t\t 800,000,000 \t\t\t\t\t 800,000,000 \r\n\t통신비\t\t 5,000,000 \t\t\t\t\t 5,000,000 \r\n\t축하금/조의금\t\t 70,000,000 \t\t\t\t\t 70,000,000 \r\n\t기타금품 등\t\t 100,927,240 \t\t\t\t\t 100,927,240 \r\n\t복리후생비 소계 ⓑ\t\t 917,923,814,477 \t - \t - \t - \t - \t 917,923,814,477 \r\n"\'잡급 및 무기계약직에\n대한 인건비\'\n(복리후생비, 인센티브포함) ⓒ"\t\t일반 급여(1)\t 15,823,215,150 \t - \t - \t - \t - \t 15,823,215,150 \r\n\t\t 인센티브 상여금\t 7,000,000 \t\t\t\t\t 7,000,000 \r\n\t\t 순액\t 15,816,215,150 \t\t\t\t\t 15,816,215,150 \r\n\t\t청년인턴 급여(2)\t 9,414,136,240 \t - \t - \t - \t - \t 9,414,136,240 \r\n\t\t 인센티브 상여금\t 8,000,000 \t\t\t\t\t 8,000,000 \r\n\t\t 순액\t 9,406,136,240 \t\t\t\t\t 9,406,136,240 \r\n\t\t무기계약직 급여(3)\t 26,694,838,746 \t - \t - \t - \t - \t 26,694,838,746 \r\n\t\t 인센티브 상여금\t 1,256,862,230 \t\t\t\t\t 1,256,862,230 \r\n\t\t 순액\t 25,437,976,516 \t\t\t\t\t 25,437,976,516 \r\n\t\t소계 ⓒ=(1)+(2)+(3)\t 51,932,190,136 \t - \t - \t - \t - \t 51,932,190,136 \r\n\t\t\t\t\t\t\t\t\r\n인건비 총계 : ⓓ=ⓐ+ⓑ+ⓒ\t\t\t 2,253,646,747,112 \t - \t - \t - \t - \t 2,253,646,747,112 \r\n인센티브 상여금 ⓔ=ⓔ-1+ⓔ-2\t\t\t 51,984,712,381 \t - \t - \t - \t - \t 51,984,712,381 \r\n- 인센티브 전환금 (ⓔ-1)\t\t\t 43,589,629,529 \t\t\t\t\t 43,589,629,529 \r\n- 인센티브 추가금 (ⓔ-2)\t\t\t 8,395,082,852 \t\t\t\t\t 8,395,082,852 \r\n인건비 해당금액 : ⓓ-ⓔ\t\t\t 2,201,662,034,731 \t - \t - \t - \t - \t 2,201,662,034,731 \r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\r\n'
        excel_original01 = excel_original01.replace(' ', '').replace('\t-\t', '\t\t')

        excel_original02 = '(3)총인건비인상률지표의점수계산을위한Template\t\t\t\t\r\n\t\t\t\t(단위:원)\r\n구분\t\t\t2024\t2023\r\n\t1.인센티브상여금을제외한인건비총액\t\t\t\r\n\ta.판관비로처리한인건비\t\t1,397,001,034,731\t1,298,932,744,191\r\n\tb.영업외비용으로처리한인건비\t\t-\t-\r\n\tc.제조원가로처리한인건비\t\t-\t-\r\n\td.타계정대체로처리한인건비\t\t-\t-\r\n\te.이익잉여금의증감으로처리한인건비\t\t-\t-\r\n\t소계:(A)=a+b+c+d+e\t\t1,397,001,034,731\t1,298,932,744,191\r\n\t\t\t\t\r\n\t2.총인건비 인상률계산에서제외(조정)되는인건비\t\t\t\r\n\tf.퇴직급여(명예퇴직금포함)\t\t168,793,866,818\t141,500,433,647\r\n\tg.임원인건비\t\t983,482,250\t771,999,300\r\n\th.비상임이사인건비\t\t-\t-\r\n\ti.인상률제외인건비\t통상임금소송결과에따른실 적급여증가액\t-\t-\r\n\t\t기타제외인건비\t-\t-\r\n\tj.사내근로복지기금출연금\t\t-\t-\r\n\tk.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)\t\t50,660,327,906\t50,195,933,210\r\n\tl.공적보험사용자부담분\t\t103,691,428,840\t104,545,198,290\r\n\tm.연월차수당등조정(㉠-㉡+㉢)\t\t71,795,906,667\t-2,930,735,981\r\n\t-연월차수당등발생액(㉠)\t\t123,325,995,917\t63,001,832,519\r\n\t-연월차수당등지급액(㉡)\t\t51,530,089,250\t65,932,568,500\r\n\t-종업원저리대여금이 자관련인건비(㉢)\t\t-\t-\r\n\tn.저리·무상대여이익\t\t4,725,943,920\t5,598,293,980\r\n\to.지방이전관련직접인건비\t\t-\t-\r\n\tp.법령에따른특수건강진단비\t\t-\t-\r\n\tq.코로나19대응을위한시간외근로수당등\t\t-\t-\r\n\tr.해외근무수당\t\t-\t-\r\n\ts.직무발명보상금\t\t-\t-\r\n\tt.공무원수준내의자녀수당및출산격려금\t\t3,051,903,476\t1,832,315,628\r\n\tu.야간간호특별수당\t\t-\t-\r\n\tv.비상진료체계운영에따른특별수당등\t\t-\t-\r\n\tu.국민건강보험공단2023년도총인건비초과액에따른상환금액\t\t-\t22,500,000,000\r\n\t소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s+t+u+v+w\t\t394,250,972,037\t312,816,850,114\r\n\t\t\t\t\r\n\t3.실집행액기준총인건비발생액(C)=(A)-(B)\t\t1,002,750,062,694\t986,115,894,077\r\n\t\t\t\t\r\n"전년대비\n조정된\n총인건비\n발생액\n산출"\t4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)\t\t\t-8,039,360,305\r\n\t5.별도직군승진시기차이에따른인건비효과조정(E)\t\t\t\r\n\t6.초임직급정원변동에따른인건비효과조정(F)\t\t\t-511,459,730\r\n\t7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)\t\t\t\r\n\t8.생산량증가로인하여\'23년도\'에추가로지급된인건비의영향제거(H)\t\t\tn/a\r\n\t9.최저임금지급직원에대한인건비효과조정(I)\t\t\t\r\n\t10.파업등에따른인건비효과조정(J)\t\t\t\r\n\t11.코로나19로인한휴업의인건비효과조정(K)\t\t\t\r\n\t"12.총인건비인상률계산대상총인건비발생액\n=(C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)+(K)+(L)"\t\t1,002,750,062,694\t978,587,993,501\r\n\t\t\t\t\r\n"당해연도\n총인건비\n인상률\n계산"\t13.총인건비인상률가이드라인에따른총인건비상한액\t\tn/a\tn/a\r\n\t(1)\'23년도총인건비인상률가이드라인을준수한경우\t\t\t978,587,993,501\r\n\t(2)\'23년도총인건비인상률가이드라인을준수경우하지않은경우\t\t\t-\r\n\t\t\t\t\r\n\t14.총인건비인상률 산출(\'24년도총인건비인상률가이드라인=2.5%)\t\tn/a\t\r\n\t(1)\'23년도총인건비인상률가이드라인을준수한경우\t\t2.469%\t\r\n\t(2)\'23년도총인건비인상률가이드라인을준수경우하지않은경우\t\t-\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n'
        excel_original02 = excel_original02.replace(' ', '').replace('\t-\t', '\t\t')
        
        excel_original03 = '(3-1) 증원소요 인건비 계산을 위한 Template\t\t\t\t\t\t\r\n\t\t\t\t\t(단위: 명, 원)\t\r\n직급\t인원\t\t\t"전년도의\n평균단가\n(D)"\t"증원소요 인건비\n(C) x (D)"\t\r\n\t"전년도\n(A)"\t"당년도\n(B)"\t"증감\n(C)=(B)-(A)"\t\t\t\r\n1급\t133.0 \t133.0 \t -  \t99,310,634 \t -  \t\r\n2급\t589.0 \t589.0 \t -  \t92,457,982 \t -  \t\r\n3급\t2,437.1 \t2,444.9 \t7.8 \t86,403,138 \t673,944,476 \t\r\n4급\t4,314.5 \t4,060.4 \t△254.1 \t77,428,700 \t△19,674,632,670 \t\r\n5급\t3,887.0 \t4,251.8 \t364.8 \t53,434,940 \t19,493,066,112 \t\r\n6급\t3,466.0 \t3,269.3 \t△196.7 \t44,091,356 \t△8,672,769,725 \t\r\n연 구직\t136.9 \t138.8 \t1.9 \t74,227,106 \t141,031,501 \t\r\n계\t14,963.5 \t14,887.2 \t△76.3 \t\t△8,039,360,305 \t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n'
        excel_original03 = excel_original03.replace(' ', '').replace('\t-\t', '\t\t')

        excel_original04 = '(3-2) 직급별 평균인원 계산을 위한 Template\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\r\n전년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균인원\t\r\n\t1급\t 166.0 \t 166.0 \t 167.0 \t 167.0 \t 167.0 \t 167.0 \t 159.0 \t 158.0 \t 158.0 \t 158.0 \t 158.0 \t 158.0 \t 162.4 \t\r\n\t2급\t 678.0 \t 678.0 \t 680.0 \t 680.0 \t 680.0 \t 678.0 \t 669.0 \t 669.0 \t 671.0 \t 670.0 \t 668.0 \t 670.0 \t 674.3 \t\r\n\t3급\t 2,598.0 \t 2,594.0 \t 2,591.0 \t 2,587.0 \t 2,584.0 \t 2,586.0 \t 2,555.0 \t 2,547.0 \t 2,548.0 \t 2,550.0 \t 2,549.0 \t 2,551.8 \t 2,570.1 \t\r\n\t4급\t 4,039.0 \t 4,189.8 \t 4,180.0 \t 4,174.5 \t 4,173.3 \t 4,168.3 \t 3,985.0 \t 3,967.5 \t 3,992.8 \t 3,981.3 \t 3,974.3 \t 3,977.5 \t 4,066.9 \t\r\n\t5급\t 4,011.3 \t 3,815.5 \t 3,797.0 \t 3,785.3 \t 3,773.5 \t 3,761.8 \t 3,966.8 \t 3,959.8 \t 3,988.0 \t 3,942.0 \t 3,916.0 \t 3,927.5 \t 3,887.0 \t\r\n\t6급\t 3,440.0 \t 3,432.0 \t 3,437.3 \t 3,440.5 \t 3,436.5 \t 3,439.8 \t 3,451.0 \t 3,439.0 \t 3,445.0 \t 3,423.5 \t 3,425.5 \t 3,782.0 \t 3,466.0 \t\r\n\t연구직\t 145.0 \t 140.0 \t 136.0 \t 133.0 \t 133.0 \t 133.0 \t 139.0 \t 138.0 \t 135.0 \t 135.0 \t 136.0 \t 139.8 \t 136.9 \t\r\n\t계\t 15,077.3 \t 15,015.3 \t 14,988.3 \t 14,967.3 \t 14,947.3 \t 14,933.8 \t 14,924.8 \t 14,878.3 \t 14,937.8 \t 14,859.8 \t 14,826.8 \t 15,206.5 \t 14,963.6 \t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\r\n당년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균인원\t\r\n\t1급\t 162.00 \t 162.00 \t 161.00 \t 160.00 \t 159.00 \t 158.00 \t 165.00 \t 165.00 \t 165.00 \t 165.00 \t 165.00 \t 165.00 \t 162.70 \t\r\n\t2급\t 678.00 \t 678.00 \t 678.00 \t 678.00 \t 678.00 \t 678.00 \t 670.00 \t 669.00 \t 669.00 \t 669.00 \t 669.00 \t 667.00 \t 673.40 \t\r\n\t3급\t 2,583.00 \t 2,579.00 \t 2,573.75 \t 2,566.50 \t 2,556.75 \t 2,561.00 \t 2,575.00 \t 2,571.75 \t 2,572.75 \t 2,569.75 \t 2,568.50 \t 2,569.50 \t 2,570.60 \t\r\n\t4급\t 3,877.75 \t 3,854.75 \t 3,847.75 \t 3,840.75 \t 3,835.00 \t 3,842.50 \t 3,526.50 \t 3,855.75 \t 3,853.00 \t 3,842.25 \t 3,834.50 \t 3,837.50 \t 3,820.70 \t\r\n\t5급\t 4,149.25 \t 4,126.25 \t 4,119.00 \t 4,117.75 \t 4,105.75 \t 4,119.50 \t 4,673.25 \t 4,325.50 \t 4,348.25 \t 4,318.50 \t 4,312.25 \t 4,306.75 \t 4,251.80 \t\r\n\t6급\t 3,319.75 \t 3,318.00 \t 3,307.50 \t 3,302.75 \t 3,292.50 \t 3,292.00 \t 3,155.25 \t 3,156.00 \t 3,160.00 \t 3,160.00 \t 3,160.75 \t 3,607.50 \t 3,269.30 \t\r\n\t연구직\t 138.00 \t 139.00 \t 136.00 \t 135.00 \t 134.00 \t 136.00 \t 137.00 \t 141.00 \t 139.00 \t 139.00 \t 146.00 \t 145.00 \t 138.80 \t\r\n\t계\t 14,907.75 \t 14,857.00 \t 14,823.00 \t 14,800.75 \t 14,761.00 \t 14,787.00 \t 14,902.00 \t 14,884.00 \t 14,907.00 \t 14,863.50 \t 14,856.00 \t 15,298.25 \t 14,887.30 \t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n'
        excel_original04 = excel_original04.replace(' ', '').replace('\t-\t', '\t\t')

        excel_original05 = '(3-3) 근속승진 및 증원소요인건비 대상 인원의 파악\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n가. 정원 및 현원 차이\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\t\t\t\t\t\t\t\r\n당년도\t직급\t1 월\t\t\t\t2월\t\t\t\t3월\t\t\t\t4월\t\t\t\t5월\t\t\t\t6월\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t\t\t\t\t\t\t\t\r\n\t1급\t133 \t162.0 \t0.0 \t-29.0 \t133 \t162.0 \t0.0 \t-29.0 \t133 \t161.0 \t0.0 \t-28.0 \t133 \t160.0 \t0.0 \t-27.0 \t133 \t159.0 \t0.0 \t-26.0 \t133 \t158.0 \t0.0 \t-25.0 \t\t\t\t\t\t\t\t\r\n\t2급\t589 \t678.0 \t0.0 \t-118.0 \t589 \t678.0 \t0.0 \t-118.0 \t589 \t678.0 \t0.0 \t-117.0 \t589 \t678.0 \t0.0 \t-116.0 \t589 \t678.0 \t0.0 \t-115.0 \t589 \t678.0 \t0.0 \t-114.0 \t\t\t\t\t\t\t\t\r\n\t3급\t2,382 \t2,583.0 \t51.0 \t-268.0 \t2,382 \t2,579.0 \t47.0 \t-268.0 \t2,382 \t2,573.8 \t46.0 \t-262.8 \t2,382 \t2,566.5 \t47.0 \t-253.5 \t2,382 \t2,556.8 \t46.0 \t-243.8 \t2,382 \t2,561.0 \t46.0 \t-247.0 \t\t\t\t\t\t\t\t\r\n\t4급\t8,518 \t3,877.8 \t0.0 \t4,372.3 \t8,518 \t3,854.8 \t0.0 \t4,395.3 \t8,518 \t3,847.8 \t0.0 \t4,407.5 \t8,518 \t3,840.8 \t0.0 \t4,423.8 \t8,518 \t3,835.0 \t0.0 \t4,439.3 \t8,518 \t3,842.5 \t0.0 \t4,428.5 \t\t\t\t\t\t\t\t\r\n\t5급\t1,280 \t4,149.3 \t0.0 \t1,503.0 \t1,280 \t4,126.3 \t0.0 \t1,549.0 \t1,280 \t4,119.0 \t0.0 \t1,568.5 \t1,280 \t4,117.8 \t0.0 \t1,586.0 \t1,280 \t4,105.8 \t0.0 \t1,613.5 \t1,280 \t4,119.5 \t0.0 \t1,589.0 \t\t\t\t\t\t\t\t\r\n\t6급\t2,479 \t3,319.8 \t0.0 \t662.3 \t2,479 \t3,318.0 \t0.0 \t710.0 \t2,479 \t3,307.5 \t0.0 \t740.0 \t2,479 \t3,302.8 \t0.0 \t762.3 \t2,479 \t3,292.5 \t0.0 \t800.0 \t2,479 \t3,292.0 \t0.0 \t776.0 \t\t\t\t\t\t\t\t\r\n\t연구직\t157 \t138.0 \t0.0 \t0.0 \t157 \t139.0 \t0.0 \t0.0 \t157 \t136.0 \t0.0 \t0.0 \t157 \t135.0 \t0.0 \t0.0 \t157 \t134.0 \t0.0 \t0.0 \t157 \t136.0 \t0.0 \t0.0 \t\t\t\t\t\t\t\t\r\n\t계\t15,538 \t14,907.8 \t51.0 \t\t15,538 \t14,857.0 \t47.0 \t\t15,538 \t14,823.0 \t46.0 \t\t15,538 \t14,800.8 \t47.0 \t\t15,538 \t14,761.0 \t46.0 \t\t15,538 \t14,787.0 \t46.0 \t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n당년도\t직급\t7월\t\t\t\t8월\t\t\t\t9월\t\t\t\t10월\t\t\t\t11월\t\t\t\t12월\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t정원\t 현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t\t\t\t\t\t\t\t\r\n\t1급\t133 \t165.0 \t0.0 \t-32.0 \t133 \t165.0 \t0.0 \t-32.0 \t133 \t165.0 \t0.0 \t-32.0 \t133 \t165.0 \t0.0 \t-32.0 \t133 \t165.0 \t0.0 \t-32.0 \t133 \t165.0 \t0.0 \t-32.0 \t\t\t\t\t\t\t\t\r\n\t2급\t589 \t670.0 \t0.0 \t-113.0 \t589 \t669.0 \t0.0 \t-112.0 \t589 \t669.0 \t0.0 \t-112.0 \t589 \t669.0 \t0.0 \t-112.0 \t589 \t669.0 \t0.0 \t-112.0 \t589 \t667.0 \t0.0 \t-110.0 \t\t\t\t\t\t\t\t\r\n\t3급\t2,399 \t2,575.0 \t66.0 \t-223.0 \t2,399 \t2,571.8 \t63.0 \t-221.8 \t2,399 \t2,572.8 \t60.0 \t-225.8 \t2,399 \t2,569.8 \t60.0 \t-222.8 \t2,399 \t2,568.5 \t60.0 \t-221.5 \t2,399 \t2,569.5 \t61.0 \t-219.5 \t\t\t\t\t\t\t\t\r\n\t4급\t8,547 \t3,526.5 \t0.0 \t4,797.5 \t8,547 \t3,855.8 \t0.0 \t4,469.5 \t8,547 \t3,853.0 \t0.0 \t4,468.3 \t8,547 \t3,842.3 \t0.0 \t4,482.0 \t8,547 \t3,834.5 \t0.0 \t4,491.0 \t8,547 \t3,837.5 \t0.0 \t4,490.0 \t\t\t\t\t\t\t\t\r\n\t5급\t1,284 \t4,673.3 \t0.0 \t1,408.3 \t1,284 \t4,325.5 \t0.0 \t1,428.0 \t1,284 \t4,348.3 \t0.0 \t1,404.0 \t1,284 \t4,318.5 \t0.0 \t1,447.5 \t1,284 \t4,312.3 \t0.0 \t1,462.8 \t1,284 \t4,306.8 \t0.0 \t1,467.3 \t\t\t\t\t\t\t\t\r\n\t6급\t2,551 \t3,155.3 \t0.0 \t804.0 \t2,551 \t3,156.0 \t0.0 \t823.0 \t2,551 \t3,160.0 \t0.0 \t795.0 \t2,551 \t3,160.0 \t0.0 \t838.5 \t2,551 \t3,160.8 \t0.0 \t853.0 \t2,551 \t3,607.5 \t0.0 \t410.8 \t\t\t\t\t\t\t\t\r\n\t연구직\t157 \t137.0 \t0.0 \t0.0 \t157 \t141.0 \t0.0 \t0.0 \t157 \t139.0 \t0.0 \t0.0 \t157 \t139.0 \t0.0 \t0.0 \t157 \t146.0 \t0.0 \t0.0 \t157 \t145.0 \t0.0 \t0.0 \t\t\t\t\t\t\t\t\r\n\t계\t15,660 \t14,902.0 \t66.0 \t\t15,660 \t14,884.0 \t63.0 \t\t15,660 \t14,907.0 \t60.0 \t\t15,660 \t14,863.5 \t60.0 \t\t15,660 \t14,856.0 \t60.0 \t\t15,660 \t15,298.3 \t61.0 \t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n'
        excel_original05 += '나. 근속승진\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n당년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t1급\t29.0\t29.0\t28.0\t27.0\t26.0\t25.0\t32.0\t32.0\t32.0\t32.0\t32.0\t32.0\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t2급\t89.0\t89.0\t89.0\t89.0\t89.0\t89.0\t81.0\t80.0\t80.0\t80.0\t80.0\t78.0\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t3급\t150.0\t150.0\t145.8\t137.5\t128.8\t133.0\t110.0\t109.8\t113.8\t110.8\t109.5\t109.5\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t4급\t-268.0\t-268.0\t-262.8\t-253.5\t-243.8\t-247.0\t-223.0\t-221.8\t-225.8\t-222.8\t-221.5\t-219.5\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t5급\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t6급\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t연구직\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t계\t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n다. 증원소요인건비 대상 인원\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n당년도\t직급\t1월\t2월\t3월\t4 월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균인원\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t1급\t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t2급\t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t3급\t2,433.0 \t2,429.0 \t2,428.0 \t2,429.0 \t2,428.0 \t2,428.0 \t2,465.0 \t2,462.0 \t2,459.0 \t2,459.0 \t2,459.0 \t2,460.0 \t2,444.9 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t4급\t4,145.8 \t4,122.8 \t4,110.5 \t4,094.3 \t4,078.8 \t4,089.5 \t3,749.5 \t4,077.5 \t4,078.8 \t4,065.0 \t4,056.0 \t4,057.0 \t4,060.4 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t5급\t4,149.3 \t4,126.3 \t4,119.0 \t4,117.8 \t4,105.8 \t4,119.5 \t4,673.3 \t4,325.5 \t4,348.3 \t4,318.5 \t4,312.3 \t4,306.8 \t4,251.8 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t6급\t3,319.8 \t3,318.0 \t3,307.5 \t3,302.8 \t3,292.5 \t3,292.0 \t3,155.3 \t3,156.0 \t3,160.0 \t3,160.0 \t3,160.8 \t3,607.5 \t3,269.3 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t연구직\t138.0 \t139.0 \t136.0 \t135.0 \t134.0 \t136.0 \t137.0 \t141.0 \t139.0 \t139.0 \t146.0 \t145.0 \t138.8 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t계\t14,907.8 \t14,857.0 \t14,823.0 \t14,800.8 \t14,761.0 \t14,787.0 \t14,902.0 \t14,884.0 \t14,907.0 \t14,863.5 \t14,856.0 \t15,298.3 \t14,887.2 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n전년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균인원\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t1급\t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t2급\t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t3급\t2,435.8 \t2,434.8 \t2,435.0 \t2,435.8 \t2,434.8 \t2,436.5 \t2,443.3 \t2,441.3 \t2,438.0 \t2,437.0 \t2,437.0 \t2,436.0 \t2,437.1 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t4급\t4,323.2 \t4,471.0 \t4,461.0 \t4,450.7 \t4,447.5 \t4,440.8 \t4,202.7 \t4,178.2 \t4,209.8 \t4,200.3 \t4,190.3 \t4,199.3 \t4,314.5 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t5급\t4,011.3 \t3,815.5 \t3,797.0 \t3,785.3 \t3,773.5 \t3,761.8 \t3,966.8 \t3,959.8 \t3,988.0 \t3,942.0 \t3,916.0 \t3,927.5 \t3,887.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t6급\t3,440.0 \t3,432.0 \t3,437.3 \t3,440.5 \t3,436.5 \t3,439.8 \t3,451.0 \t3,439.0 \t3,445.0 \t3,423.5 \t3,425.5 \t3,782.0 \t3,466.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t연구직\t145.0 \t140.0 \t136.0 \t133.0 \t133.0 \t133.0 \t139.0 \t138.0 \t135.0 \t135.0 \t136.0 \t139.8 \t136.9 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t계\t15,077.3 \t15,015.3 \t14,988.3 \t14,967.3 \t14,947.3 \t14,933.8 \t14,924.8 \t14,878.3 \t14,937.8 \t14,859.8 \t14,826.8 \t15,206.5 \t14,963.5 \t\tt\r\n'
        excel_original05 = excel_original05.replace(' ', '').replace('\t-\t', '\t\t')
        
        excel_original06 = '(3-4) 직급별 평균단가 계산을 위한 Template\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 원)\r\n전년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t 12월 \t"인건비\n총계"\t평균인원\t"직급별\n평균단가\n(수정 전)"\t"공무원 수준 내\n가족(자녀)수당"\t"공무원 수준 내\n출산축하금"\t"총인건비 차감 액\n(225억원)"\t"인건비 총계\n(수정 후)"\t"직급별\n평균단가"\r\n\t1급\t 1,321,802,810 \t 1,291,429,920 \t 1,326,000,290 \t 1,326,201,640 \t 1,268,376,330 \t 1,330,114,040 \t 1,733,986,960 \t 1,320,458,570 \t 1,312,172,040 \t 1,312,139,870 \t 1,315,490,040 \t 1,637,182,180 \t 16,495,354,690 \t 162.4 \t 101,572,381 \t - \t - \t 367,307,772 \t 16,128,046,918 \t 99,310,634 \r\n\t2급\t 4,948,980,180 \t 4,863,629,030 \t 4,953,343,590 \t 4,954,987,280 \t 4,769,837,630 \t 4,975,979,063 \t 6,451,898,160 \t 5,095,134,530 \t 5,091,679,310 \t 5,094,012,550 \t 5,088,037,870 \t 7,476,759,374 \t 63,764,278,567 \t 674.3 \t 94,563,664 \t\t - \t 1,419,861,260 \t 62,344,417,307 \t 92,457,982 \r\n\t3급\t 19,111,270,460 \t 17,320,263,020 \t 19,035,988,790 \t 17,316,149,340 \t 17,301,048,560 \t 20,258,047,323 \t 17,060,089,490 \t 17,042,175,518 \t 20,405,748,920 \t 17,024,524,280 \t 17,062,985,470 \t 28,690,840,311 \t 227,629,131,482 \t 2,570.1 \t 88,568,200 \t 493,728,590 \t 2,000,000 \t 5,068,696,653 \t 222,064,706,239 \t 86,403,138 \r\n\t4급\t 27,973,217,490 \t 25,314,121,630 \t 27,873,909,550 \t 25,211,744,390 \t 25,201,347,530 \t 26,581,898,988 \t 23,809,210,590 \t 23,736,133,130 \t 28,723,590,960 \t 23,824,586,280 \t 23,750,159,250 \t 40,926,953,862 \t 322,926,873,650 \t 4,066.9 \t 79,403,692 \t 796,369,178 \t 45,000,000 \t 7,190,724,460 \t 314,894,780,012 \t 77,428,700 \r\n\t5급\t 17,284,675,850 \t 15,464,665,320 \t 17,260,224,060 \t 15,372,935,600 \t 15,371,757,040 \t 17,199,384,134 \t 16,081,394,090 \t 16,153,774,921 \t 20,025,879,960 \t 16,191,904,800 \t 16,111,683,600 \t 30,354,439,609 \t 212,872,718,984 \t 3,887.0 \t 54,765,299 \t 329,995,920 \t 101,000,000 \t 4,740,110,509 \t 207,701,612,555 \t 53,434,940 \r\n\t6급\t 12,923,915,810 \t 11,492,535,180 \t 12,878,647,990 \t 11,552,605,610 \t 11,568,258,340 \t 13,256,094,043 \t 11,055,966,180 \t 11,589,625,850 \t 14,279,261,000 \t 11,550,381,140 \t 11,561,789,550 \t 22,657,653,654 \t 156,366,734,347 \t 3,466.0 \t 45,114,465 \t 47,221,940 \t 17,000,000 \t 3,481,872,192 \t 152,820,640,215 \t 44,091,356 \r\n\t연구직\t 858,793,160 \t 842,878,770 \t 819,288,680 \t 794,829,380 \t 788,109,900 \t 787,871,080 \t 804,115,530 \t 825,729,100 \t 807,479,280 \t 790,436,900 \t 810,932,730 \t 1,462,653,475 \t 10,393,117,985 \t 136.9 \t 75,917,589 \t - \t - \t 231,427,155 \t 10,161,690,830 \t 74,227,106 \r\n\t계\t 84,422,655,760 \t 76,589,522,870 \t 84,147,402,950 \t 76,529,453,240 \t 76,268,735,330 \t 84,389,388,671 \t 76,996,661,000 \t 75,763,031,619 \t 90,645,811,470 \t 75,787,985,820 \t 75,701,078,510 \t 133,206,482,465 \t 1,010,448,209,705 \t 14,963.6 \t 67,527,080 \t 1,667,315,628 \t 165,000,000 \t 22,500,000,000 \t 986,115,894,077 \t 65,900,979 \r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 원)\t\t\t\t\t\r\n당년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t 12월 \t"인건비\n총계"\t평균인원\t"직급별\n평균단가"\t\t\t\t\t\r\n\t1급\t 1,289,093,280 \t 1,301,470,470 \t 1,282,011,870 \t 1,294,314,070 \t 1,273,310,800 \t 1,266,833,110 \t 1,823,613,250 \t 1,377,821,680 \t 1,376,883,040 \t 1,377,071,790 \t 1,377,552,390 \t 1,543,436,610 \t 16,583,412,360 \t 162.7 \t 101,926,321 \t\t\t\t\t\r\n\t2급\t 5,041,228,250 \t 5,037,789,130 \t 5,038,918,830 \t 5,036,626,310 \t 5,028,001,270 \t 5,039,934,860 \t 6,644,537,710 \t 5,224,911,050 \t 5,219,179,220 \t 5,219,764,100 \t 5,220,681,520 \t 5,981,594,485 \t 63,733,166,735 \t 673.4 \t 94,643,847 \t\t\t\t\t\r\n\t3급\t 17,625,397,980 \t 19,344,193,980 \t 19,650,934,360 \t 17,536,858,650 \t 17,347,801,340 \t 19,553,311,730 \t 17,587,988,237 \t 17,519,558,340 \t 21,352,936,869 \t 17,542,838,840 \t 17,530,272,050 \t 24,306,822,638 \t 226,898,915,014 \t 2,570.6 \t 88,266,909 \t\t\t\t\t\r\n\t4급\t 23,541,146,470 \t 25,996,996,330 \t 26,409,785,160 \t 23,431,021,930 \t 23,228,242,220 \t 26,394,368,690 \t 21,477,194,120 \t 22,996,134,860 \t 28,449,719,510 \t 23,030,309,980 \t 23,019,346,970 \t 31,547,253,484 \t 299,521,519,724 \t 3,820.7 \t 78,394,409 \t\t\t\t\t\r\n\t5급\t 17,441,936,300 \t 19,518,492,260 \t 19,897,277,120 \t 17,437,728,740 \t 17,343,345,220 \t 19,981,102,910 \t 19,756,931,320 \t 18,280,688,130 \t 23,216,590,420 \t 18,386,888,560 \t 18,335,357,990 \t 27,101,369,172 \t 236,697,708,142 \t 4,251.8 \t 55,670,001 \t\t\t\t\t\r\n\t6급\t 11,643,907,510 \t 12,952,398,370 \t 13,176,416,364 \t 11,512,510,520 \t 11,503,845,320 \t 13,171,697,790 \t 10,234,872,400 \t 11,611,045,360 \t 13,778,287,160 \t 10,972,489,010 \t 10,996,629,300 \t 17,273,398,355 \t 148,827,497,459 \t 3,269.3 \t 45,522,741 \t\t\t\t\t\r\n\t연구직\t 879,506,520 \t 869,343,780 \t 865,985,430 \t 843,876,470 \t 826,613,590 \t 835,660,310 \t 841,369,650 \t 846,139,520 \t 869,109,910 \t 856,415,910 \t 853,742,870 \t 1,100,079,300 \t 10,487,843,260 \t 138.8 \t 75,560,830 \t\t\t\t\t\r\n\t계\t 77,462,216,310 \t 85,020,684,320 \t 86,321,329,134 \t 77,092,936,690 \t 76,551,159,760 \t 86,242,909,400 \t 78,366,506,687 \t 77,856,298,940 \t 94,262,706,129 \t 77,385,778,190 \t 77,333,583,090 \t 108,853,954,044 \t 1,002,750,062,694 \t 14,887.3 \t 67,356,073 \t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n'
        excel_original06 = excel_original06.replace(' ', '').replace('\t-\t', '\t\t')

        excel_original07 = '(3-6) 초임직급 정원변동에 따른 인건비 효과 조정을 위한 Template\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n가. 초임직급 정원\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\t\t\t\t\t\t\r\n당년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균정원\t\t\t\t\t\t\t\r\n\t1급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t2급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t3급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t4급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t5급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t6급\t575 \t575 \t575 \t575 \t575 \t642 \t642 \t642 \t642 \t642 \t642 \t642 \t614.1 \t\t\t\t\t\t\t\r\n\t연구직\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t기능직\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t계\t575 \t575 \t575 \t575 \t575 \t642 \t642 \t642 \t642 \t642 \t642 \t642 \t614.1 \t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n전년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균정원\t\t\t\t\t\t\t\r\n\t1급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t2급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t3급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t4급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t5급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t6급\t657 \t657 \t657 \t657 \t657 \t608 \t608 \t608 \t608 \t608 \t608 \t575 \t625.7 \t\t\t\t\t\t\t\r\n\t연구직\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t기능직\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t계\t657 \t657 \t657 \t657 \t657 \t608 \t608 \t608 \t608 \t608 \t608 \t575 \t625.7 \t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n나. 초임직급 정원 변동에 따른 인건비 효과\t\t\t\t\t\t(단위: 명, 원)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n구분\t정원\t\t\t"전년도의\n평균단가\n(D)"\t"인건비 효과\n(E) = (C) x (D)"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t"전년도\n(A)"\t"당년도\n(B)"\t"증감\n(C)=(B)-(A)"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n1급\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n2급\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n3급\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n4급\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n5급\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n6급\t 625.7 \t 614.1 \t-11.6 \t44,091,356 \t-511,459,730 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n연구직\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n기능직\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n계\t 625.7 \t 614.1 \t-11.6 \t\t-511,459,730 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n'
        excel_original07 = excel_original07.replace(' ', '').replace('\t-\t', '\t\t')
        """








        

    def compare(self, current_index):

        global excel_original01, excel_original02, excel_original03, excel_original04, excel_original05, excel_original06, excel_original07

        str_err = ''
        str_err_total = ''
        
        table = self.tabs.currentWidget().table

        if 1==1 or current_index == 1:
            current_index = 1
            list_title = ['기본급\t', '인센티브상여금', '그외상여금', '법정수당', '해외근무수당', '그외제수당', '퇴직급여(명예퇴직금포함)\t', '임원인건비\t', '비상임이사인건비\t',
                          '통상임금소송결과에따른실적급여증가액', '기타제외인건비', '기타항목\t', '급료,임금,제수당소계ⓐ\t',  '사내근로복지기금출연금\t', '국민연금사용자부담분\t',
                          '건강보험사용자부담분\t', '고용보험사용자부담분\t', '산재보험료사용자부담분\t', '급식비\t', '교통보조비\t', '자가운전보조금\t', '학자보조금\t','건강진단비등(독감예방주사비용)\t',
                          '선택적복지\t', '행사비\t', '포상품(비)\t', '기념품(비)\t', '격려품(비)\t', '장기근속관련비용\t', '육아보조비및출산장려금\t', '자기계발비\t', '특별근로의대가\t',
                          '피복비\t', '경로효친비\t', '통신비\t', '축하금/조의금\t', '기타금품등\t', '복리후생비소계ⓑ\t', '일반급여(1)', '인센티브상여금', '순액', '청년인턴급여(2)', '인센티브상여금', '순액', '무기계약직급여(3)',
                          '인센티브상여금', '순액', '소계ⓒ=(1)+(2)+(3)', '인건비총계:ⓓ=ⓐ+ⓑ+ⓒ\t\t', '인센티브상여금ⓔ=ⓔ-1+ⓔ-2\t\t', '인센티브전환금(ⓔ-1)\t\t', '인센티브추가금(ⓔ-2)\t\t', '인건비해당금액:ⓓ-ⓔ\t\t']

            str_err += '(2) 인건비 집계\n\n'
            str_err += '급료임금제수당\n'
            str_err += f"{'판영제타이 합':>21}{'판관비':>35}{'영업외':>36}{'제조원가':>34}{'타계정대체':>34}{'이익잉여금':>34}{'합계':>35}\n"

            excel = excel_original01
            cnt_wrong = 0
            
            for i in range (0, 53):
   
                if i == 39: excel = excel_original01.split('일반급여(1)')[1]
                if i == 42: excel = excel_original01.split('청년인턴급여(2)')[1]
                if i == 45: excel = excel_original01.split('무기계약직급여(3)')[1]
                if i == 49: excel = excel_original01.split('인건비총계:ⓓ=ⓐ+ⓑ+ⓒ')[1]

                if i == 13: str_err += "\n복리후생비\n" + f"{'판영제타이 합':>21}{'판관비':>35}{'영업외':>36}{'제조원가':>34}{'타계정대체':>34}{'이익잉여금':>34}{'합계':>35}\n"

                if i == 38: str_err += "\n잡급\n" + f"{'판영제타이 합':>21}{'판관비':>35}{'영업외':>36}{'제조원가':>34}{'타계정대체':>34}{'이익잉여금':>34}{'합계':>35}\n"
                if i == 49: str_err += "\n인건비\n" + f"{'판영제타이 합':>21}{'판관비':>35}{'영업외':>36}{'제조원가':>34}{'타계정대체':>34}{'이익잉여금':>34}{'합계':>35}\n"

                try:
                    excel.split(list_title[i])[1]
                except:
                    with open("log.txt", "a", encoding="utf-8") as f:                    
                        f.write("excel_original01 (2)인건비집계 오류: " + list_title[i]  + '\n')
                    print("excel_original01 (2)인건비집계 오류: " + list_title[i]  + '\n')
                    QMessageBox.information(self, "(2)인건비집계", "(2)인건비집계: " + list_title[i])
                    

                excel = excel.split(list_title[i])[1] # 기본급
                excel_item = excel.split('\r\n')[0]
                
                # str_err += self.text_table(i, 0)[:6] + '\t   '
                if i in [0, 7, 11, 18, 19, 21, 23, 24, 30, 32, 33, 34, 36]:
                    str_err += list_title[i][:6] + '   '
                else:
                    str_err += list_title[i][:6] + '\t   '

                list_temp = []                
                for j in range(1, 7):
                    if self.excel_str(excel_item.split('\t')[j], current_index, i, j) == self.table_str(current_index, i, j):
                        str_err += 'O '
                        list_temp.append(' ' * 38)
                        
                    else:
                        str_err += 'X '
                        cnt_wrong += 1
                        list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j)}").rjust(38))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(2) 인건비 집계', '(2) 인건비 집계\t불일치: [' + str(cnt_wrong) + '/318]')
            str_err_total += '(2) 인건비 집계\t\t불일치: [' + str(cnt_wrong) + '/318]\n'
            str_err += '\n\n\n'



        if 1==1 or current_index == 2:
            current_index = 2

            list_title = ['1.인센티브상여금을제외한인건비총액', 'a.판관비로처리한인건비', 'b.영업외비용으로처리한인건비', 'c.제조원가로처리한인건비', 'd.타계정대체로처리한인건비', 'e.이익잉여금의증감으로처리한인건비',
                          '소계:(A)=a+b+c+d+e', '2.총인건비인상률계산에서제외(조정)되는인건비', 'f.퇴직급여(명예퇴직금포함)', 'g.임원인건비', 'h.비상임이사인건비',
                          '기타제외인건비', 'j.사내근로복지기금출연금', 'k.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)', 'l.공적보험사용자부담분', 'm.연월차수당등조정(㉠-㉡+㉢)', '연월차수당등발생액(㉠)',
                          '연월차수당등지급액(㉡)', '종업원저리대여금이자관련인건비(㉢)', '무상대여이익', 'o.지방이전관련직접인건비', 'p.법령에따른특수건강진단비', 'q.코로나19대응을위한시간외근로수당등',
                          'r.해외근무수당', 's.직무발명보상금', 't.공무원수준내의자녀수당및출산격려금', 'v.비상진료체계운영에따른특별수당등',
                          'u.국민건강보험공단2023년도총인건비초과액에따른상환금액', '소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s+t+u+v+w', '3.실집행액기준총인건비발생액(C)=(A)-(B)', '4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)',
                          '5.별도직군승진시기차이에따른인건비효과조정(E)', '6.초임직급정원변동에따른인건비효과조정(F)', '7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)',
                          '추가로지급된인건비의영향제거(H)', '최저임금지급직원에대한인건비효과조정(I)', '10.파업등에따른인건비효과조정(J)',
                          '11.코로나19로인한휴업의인건비효과조정(K)', '(C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)+(K)+(L)', '13.총인건비인상률가이드라인에따른총인건비상한액',
                          '23년도총인건비인상률가이드라인을준수한경우', '23년도총인건비인상률가이드라인을준수경우하지않은경우', '24년도총인건비인상률가이드라인=2.5%)', '23년도총인건비인상률가이드라인을준수한경우',
                          '23년도총인건비인상률가이드라인을준수경우하지않은경우' ]

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
            str_err += '(3) 총인건비 인상률 지표의 점수계산\n\n'
            str_err += '실집행액 기준 총인건비 발생액 산출\n\n'



            w_h = 28 
            w_d = 35
            str_err += f"{'5 4 3':>28}{'2025':>39}{'2024':>41}{'2023':>39}\n"

            excel = excel_original02
            cnt_wrong = 0

            for i in range (0, 45):

                try:
                    excel.split(list_title[i])[1]
                except:
                    with open("log.txt", "a", encoding="utf-8") as f:                    
                        f.write("excel_original02 (3)총인건비인상률 오류: " + list_title[i]  + '\n')
                    print("excel_original02 (3)총인건비인상률 오류: " + list_title[i]  + '\n')
                    QMessageBox.information(self, "(3)총인건비인상률", "(3)총인건비인상률: " + list_title[i])


                
                if i in [7, 29, 30]: str_err += '\n'
                if i == 30: str_err += '\n전년대비 조정된 총인건비 발생액 산출\n\n' + f"{'5 4 3':>28}{'2025':>39}{'2024':>41}{'2023':>39}\n"
                if i == 39: str_err += '\n\n당해연도 총인건비 인상률 계산\n\n' + f"{'5 4 3':>28}{'2025':>39}{'2024':>41}{'2023':>39}\n"

                if i == 42:
                    excel = excel_original02.split('14.총인건비인상률')[1] # 기본급
                    excel_item = excel.split('\r\n')[0]
                else:
                    excel = excel.split(list_title[i])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]
                if i == 11: excel_item = '\t' + excel_item   

                # str_err += self.text_table(i, 1)[:12] + '\t'

                if i in [6, 9, 19, 28, 37, 38]:
                    str_err += list_title[i][:8] + '\t\t'
                else:
                    str_err += list_title[i][:8] + '\t'

                list_temp = []                
                for j in range(2, 5): ####### (2, 5)
                    if self.excel_str(excel_item.split('\t')[j], current_index, i, j) == self.table_str(current_index, i, j):
                        str_err += 'O '
                        list_temp.append(' ' * 41)
                        
                    else:
                        str_err += 'X '
                        cnt_wrong += 1
                        list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j)}").rjust(41))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3) 총인건비 인상률 지표의 점수계산', '(3) 총인건비 인상률 지표의 점수계산\t\t불일치: [' + str(cnt_wrong) + '/135]')
            str_err += '\n\n\n'




        if 1 == 1 or current_index == 3:
            current_index = 3
            list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계' ]
            str_err += '(3-1) 증원 요소 인건비 계산\n\n'
            str_err += '           전당인전 증' + f"{'전년도인원(A)':>16}{'당년도인원(B)':>17}{'인원증감(C)':>18}{'전년도단가(D)':>20}{'증원인건비':>27}\n"
            excel_original03.replace('△', '-')
            excel = excel_original03
            
            cnt_wrong = 0
            for i in range (0, 8):

                try:
                    excel.split(list_title[i])[1]
                except:
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write("excel_original03 (3-1)증원인건비 오류: " + list_title[i]  + '\n')
                    print("excel_original03 (3-1)증원인건비 오류: " + list_title[i]  + '\n')
                    QMessageBox.information(self, "(3-1)증원인건비 오류", "(3-1)증원인건비 오류: " + list_title[i])
                
                excel = excel.split(list_title[i])[1] # 기본급
                excel_item = excel.split('\r\n')[0]   
                # str_err += self.text_table(i, 0) + '\t'
                str_err += list_title[i] + '\t'
                
                list_temp = []                
                for j in range(1, 6):
                    if self.excel_str(excel_item.split('\t')[j], current_index, i, j) == self.table_str(current_index, i, j):
                        str_err += 'O '
                        
                        if j == 4: list_temp.append(' ' * 25)
                        elif j == 5: list_temp.append(' ' * 32)
                        else: list_temp.append(' ' * 21)
                    else:
                        str_err += 'X '
                        cnt_wrong += 1
                        if j == 4: list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j)}").rjust(25))
                        elif j == 5: list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j)}").rjust(32))
                        else: list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j)}").rjust(21))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-1) 증원 요소 인건비 계산', '(3-1) 증원 요소 인건비 계산\t불일치: [' + str(cnt_wrong) + '/40]')
            str_err_total += '(3-1) 증원 요소 인건비 계산\t불일치: [' + str(cnt_wrong) + '/40]\n'
            str_err += '\n\n\n'




        if 1 == 1 or current_index == 4:
            current_index = 4
            list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계', '1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계']
            str_err += '(3-2) 직급별 평균 인원 계산\n\n전년도\n'
            str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>20}{'2월':>20}{'3월':>20}{'4월':>20}{'5월':>20}{'6월':>20}{'7월':>20}{'8월':>21}{'9월':>20}{'10월':>20}{'11월':>20}{'12월':>20}{'평균인원':>18}\n"

            excel = excel_original04
            
            cnt_wrong = 0
            for i in range (0, 16):


                    
                
                if i == 8:
                    excel = excel_original04.split('당년도')[1]
                    str_err += '\n\n당년도\n'
                    str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>20}{'2월':>20}{'3월':>20}{'4월':>20}{'5월':>20}{'6월':>20}{'7월':>20}{'8월':>21}{'9월':>20}{'10월':>20}{'11월':>20}{'12월':>20}{'평균인원':>18}\n"

                if i < 8:   # 전년도 표

                    try:
                        a = excel.split(list_title[i])[1]
                    except:
                        with open("log.txt", "a", encoding="utf-8") as f:                    
                            f.write("excel_original04 (3-2)직급별평균인원 오류: " + list_title[i]  + '\n')
                        print("excel_original04 (3-2)직급별평균인원 오류: " + list_title[i]  + '\n')
                        QMessageBox.information(self, "(3-2)직급별평균인원 오류", "(3-2)직급별평균인원 오류: " + list_title[i])
                        

                    excel = excel.split(list_title[i])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]

                    # str_err += self.text_table(i, 1) + '\t'
                    str_err += list_title[i] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 14):
                        if self.excel_str(excel_item.split('\t')[j], current_index, i, j) == self.table_str(current_index, i, j+1):
                            str_err += 'O '
                            list_temp.append(' ' * 21)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(21))

                else:   # 당년도 표

                    try:
                        a = excel.split(list_title[i])[1]
                    except:
                        with open("log.txt", "a", encoding="utf-8") as f:                    
                            f.write("excel_original04 (3-2)직급별평균인원 오류: " + list_title[i]  + '\n')
                        print("excel_original04 (3-2)직급별평균인원 오류: " + list_title[i]  + '\n')
                        QMessageBox.information(self, "(3-2)직급별평균인원 오류", "(3-2)직급별평균인원 오류: " + list_title[i])
                        

                    

                    excel = excel.split(list_title[i])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]
                    
                    # str_err += self.text_table(i+2, 1) + '\t'
                    str_err += list_title[i] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 14):
                        if self.excel_str(excel_item.split('\t')[j], current_index, i, j) == self.table_str(current_index, i+2, j+1):
                            str_err += 'O '
                            list_temp.append(' ' * 21)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i+2, j+1)}").rjust(21))
                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-2) 직급별 평균 인원 계산', '(3-2) 직급별 평균 인원 계산\t불일치: [' + str(cnt_wrong) + '/208]')
            str_err_total += '(3-2) 직급별 평균 인원 계산\t불일치: [' + str(cnt_wrong) + '/208]\n'
            str_err += '\n\n\n'




        if 1 == 1 or current_index == 5:
            current_index = 5
            list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계', '1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계']
            str_err += '(3-3) 가. 정원 및 현원 차이\n\n당년도\n'
            str_err += '          1정현복 누      2월       3월        4월       5월       6월' + f"{'1월 정원':>25}{'1월 현원':>22}{'1월 복직자':>22}{'1월 누적차':>22}{'2월 정원':>22}{'2월 현원':>22}{'2월 복직자':>22}{'2월 누적차':>22}{'3월 정원':>22}{'3월 현원':>22}{'3월 복직자':>22}{'3월 누적차':>22}{'4월 정원':>22}{'4월 현원':>22}{'4월 복직자':>22}{'4월 누적차':>22}{'5월 정원':>22}{'5월 현원':>22}{'5월 복직자':>21}{'5월 누적차':>22}{'6월 정원':>22}{'6월 현원':>22}{'6월 복직자':>22}{'6월 누적차':>22}\n"
            
            excel_original05_05 = excel_original05.split('나.근속승진')[0]  
            excel = excel_original05_05


            
            cnt_wrong = 0
            for i in range (0, 16):

                if i == 8:
                    continue
                
                if i == 9:
                    excel = excel_original05_05.split('당년도')[2]
                    str_err += '\n\n당년도\n'
                    str_err += '          7정현복 누      8월       9월       10월      11월      12월' + f"{'7월 정원':>25}{'7월 현원':>22}{'7월 복직자':>22}{'7월 누적차':>22}{'8월 정원':>22}{'8월 현원':>22}{'8월 복직자':>22}{'8월 누적차':>22}{'9월 정원':>22}{'9월 현원':>22}{'9월 복직자':>22}{'9월 누적차':>22}{'10월 정원':>22}{'10월 현원':>22}{'10월 복직자':>22}{'10월 누적차':>22}{'11월 정원':>22}{'11월 현원':>22}{'11월 복직자':>21}{'11월 누적차':>22}{'12월 정원':>22}{'12월 현원':>22}{'12월 복직자':>22}{'12월 누적차':>22}\n"
                    continue
                
                if i < 9:   # 1~6월
                    try:
                        excel.split(list_title[i])[1]
                    except:
                        with open("log.txt", "a", encoding="utf-8") as f:                    
                            f.write("excel_original05 (3-3)가.정원현원차이 오류: " + list_title[i]  + '\n')
                        print("excel_original05 (3-3)나.근속승진 오류: " + list_title[i]  + '\n')
                        QMessageBox.information(self, "(3-3)가.정원현원차이 오류", "(3-3)가.정원현원차이 오류: " + list_title[i])
                    
                    
                    excel = excel.split(list_title[i])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]
                    # str_err += self.text_table(i, 1) + '\t'
                    str_err += list_title[i] + '\t'

                    
                    list_temp = []
                    for j in range(1, 25):
                        if self.excel_str(excel_item.split('\t')[j], current_index, i, j) == self.table_str(current_index, i%24, j+1):
                            str_err += 'O '
                            list_temp.append(' ' * 25)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append(f"{self.excel_str(excel_item.split('\t')[j], current_index, i, j)}"f"__{self.table_str(current_index, i, j+1)}".rjust(25))
                            
                        if j%4 == 0: str_err = str_err[:-1] + '   '

                else:   # 7~12월
                    
                    try:
                        excel.split(list_title[i])[1]
                    except:
                        with open("log.txt", "a", encoding="utf-8") as f:                    
                            f.write("excel_original05 (3-3)가.정원현원차이 오류: " + list_title[i]  + '\n')
                        print("excel_original05 (3-3)나.근속승진 오류: " + list_title[i]  + '\n')
                        QMessageBox.information(self, "(3-3)가.정원현원차이 오류", "(3-3)가.정원현원차이 오류: " + list_title[i])
                    
                    excel = excel.split(list_title[i-2])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]
                    # str_err += self.text_table(i, 1) + '\t'
                    str_err += list_title[i] + '\t'

                    list_temp = []                
                    for j in range(1, 25):
                        
                        if self.excel_str(excel_item.split('\t')[j], current_index, i, j) == self.table_str(current_index, i, j+1):
                            str_err += 'O '
                            list_temp.append(' ' * 25)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append(f"{self.excel_str(excel_item.split('\t')[j], current_index, i, j)}"f"__{self.table_str(current_index, i, j+1)}".rjust(25))
                        if j%4 == 0: str_err = str_err[:-1] + '   '

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-3) 가. 정원 및 현원 차이', '(3-3) 가. 정원 및 현원 차이\t불일치: [' + str(cnt_wrong) + '/384]')
            str_err_total += '(3-3) 가. 정원 및 현원 차이\t불일치: [' + str(cnt_wrong) + '/384]\n'
            str_err += '\n\n\n'







        if 1 == 1 or current_index == 6:
            current_index = 6
            list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계' ]
            str_err += '(3-3) 나. 근속승진\n\n'
            str_err += '           1 2 3 4 5 6 7 8 9101112평' + f"{'1월':>17}{'2월':>18}{'3월':>18}{'4월':>18}{'5월':>18}{'6월':>18}{'7월':>18}{'8월':>19}{'9월':>18}{'10월':>18}{'11월':>18}{'12월':>18}\n"

            excel_original05_06 = excel_original05.split('나.근속승진')[1].split('다.증원소요인건비대상인원')[0]
            
            excel = excel_original05_06

            cnt_wrong = 0
            for i in range (0, 8):

                try:
                    excel.split(list_title[i])[1]
                except:
                    with open("log.txt", "a", encoding="utf-8") as f:                    
                        f.write("excel_original05 (3-3)나.근속승진 오류: " + list_title[i]  + '\n')
                    print("excel_original05 (3-3)나.근속승진 오류: " + list_title[i]  + '\n')
                    QMessageBox.information(self, "(3-3)나.근속승진 오류", "(3-3)나.근속승진 오류: " + list_title[i])
                
                excel = excel.split(list_title[i])[1] # 기본급
                excel_item = excel.split('\r\n')[0]

                # str_err += self.text_table(i, 1) + '\t'
                str_err += list_title[i] + '\t'
                
                list_temp = []                
                for j in range(1, 13):
                    if self.excel_str(excel_item.split('\t')[j], current_index, i, j) == self.table_str(current_index, i, j+1):
                        str_err += 'O '
                        list_temp.append(' ' * 19)
                    else:
                        str_err += 'X '
                        cnt_wrong += 1
                        list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(19))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-3) 나. 근속승진', '(3-3) 나. 근속승진\t\t불일치: [' + str(cnt_wrong) + '/96]')
            str_err_total += '(3-3) 나. 근속승진\t\t불일치: [' + str(cnt_wrong) + '/96]\n'
            str_err += '\n\n\n'





        if 1 == 1 or current_index == 7:
            current_index = 7
            list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계', '1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계']
            str_err += '(3-3) 다. 증원 인건비 인원\n\n당년도\n'
            str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>20}{'2월':>20}{'3월':>20}{'4월':>20}{'5월':>20}{'6월':>20}{'7월':>20}{'8월':>21}{'9월':>20}{'10월':>20}{'11월':>20}{'12월':>20}{'평균인원':>18}\n"

            excel_original05_07 = excel_original05.split('다.증원소요인건비대상인원')[1]
            
            excel = excel_original05_07

            cnt_wrong = 0
            for i in range (0, 16):

                if i == 8:
                    excel = excel_original05_07.split('전년도')[1]
                    str_err += '\n\n전년도\n'
                    str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>20}{'2월':>20}{'3월':>20}{'4월':>20}{'5월':>20}{'6월':>20}{'7월':>20}{'8월':>21}{'9월':>20}{'10월':>20}{'11월':>20}{'12월':>20}{'평균인원':>18}\n"

                if i < 8:   # 전년도 표


                    try:
                        excel.split(list_title[i])[1]
                    except:
                        with open("log.txt", "a", encoding="utf-8") as f:                    
                            f.write("excel_original05 (3-3)다.증원인원 오류: " + list_title[i]  + '\n')
                        print("excel_original05 (3-3)다.증원인원 오류: " + list_title[i]  + '\n')
                        QMessageBox.information(self, "(3-3)다.증원인원 오류", "(3-3)다.증원인원 오류: " + list_title[i])
                        

                    excel = excel.split(list_title[i])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]

                    # str_err += self.text_table(i, 1) + '\t'
                    str_err += list_title[i] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 14):
                        if self.excel_str(excel_item.split('\t')[j], current_index, i, j) == self.table_str(current_index, i, j+1):
                            str_err += 'O '
                            list_temp.append(' ' * 21)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i, j+1)}").rjust(21))

                else:   # 당년도 표


                    try:
                        excel.split(list_title[i])[1]
                    except:
                        with open("log.txt", "a", encoding="utf-8") as f:                    
                            f.write("excel_original05 (3-3)다.증원인원 오류: " + list_title[i]  + '\n')
                        print("excel_original05 (3-3)다.증원인원 오류: " + list_title[i]  + '\n')
                        QMessageBox.information(self, "(3-3)다.증원인원 오류", "(3-3)다.증원인원 오류: " + list_title[i])
                        
                    

                    excel = excel.split(list_title[i])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]
                    
                    # str_err += self.text_table(i+2, 1) + '\t'
                    str_err += list_title[i] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 14):
                        if self.excel_str(excel_item.split('\t')[j], current_index, i, j) == self.table_str(current_index, i+2, j+1):
                            str_err += 'O '
                            list_temp.append(' ' * 21)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], current_index, i, j) + f"__{self.table_str(current_index, i+2, j+1)}").rjust(21))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-3) 다. 증원 인건비 인원', '(3-3) 다. 증원 인건비 인원\t불일치: [' + str(cnt_wrong) + '/208]')
            str_err_total += '(3-3) 다. 증원 인건비 인원\t불일치: [' + str(cnt_wrong) + '/208]\n'
            str_err += '\n\n\n'


        if 1 == 1 or current_index == 8:
            list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계', '1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계']
            str_err += '(3-4) 직급별 평균단가 계산\n전년도\n'
            str_err += '           1 2 3 4 5 6 7 8 9 101112인직' + f"{'1월':>36}{'2월':>36}{'3월':>36}{'4월':>36}{'5월':>36}{'6월':>36}{'7월':>37}{'8월':>36}{'9월':>36}{'10월':>36}{'11월':>36}{'12월':>36}{'인건비총계':>33}{'직급별평균단가':>31}\n"


            excel = excel_original06
            
            cnt_wrong = 0
            for i in range (0, 16):

                if i == 8:
                    excel = excel_original06.split('당년도')[1]
                    str_err += '\n\n당년도\n'
                    str_err += '           1 2 3 4 5 6 7 8 9 101112인직' + f"{'1월':>36}{'2월':>36}{'3월':>36}{'4월':>36}{'5월':>36}{'6월':>36}{'7월':>37}{'8월':>36}{'9월':>36}{'10월':>36}{'11월':>36}{'12월':>36}{'인건비총계':>33}{'직급별평균단가':>31}\n"


                if i < 8:   # 전년도 표

                    try:
                        excel.split(list_title[i])[1]
                    except:
                        with open("log.txt", "a", encoding="utf-8") as f:                    
                            f.write("excel_original06 (3-4)직급별평균단가 오류: " + list_title[i]  + '\n')
                        print("excel_original06 (3-4)직급별평균단가 오류: " + list_title[i]  + '\n')
                        QMessageBox.information(self, "(3-4)직급별평균단가 오류", "(3-4)직급별평균단가 오류: " + list_title[i])

                    

                    excel = excel.split(list_title[i])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]

                    
                    # str_err += self.text_table(i, 1) + '\t'
                    str_err += list_title[i] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 15):
                        if self.excel_str(excel_item.split('\t')[j], 8, i, j) == self.table_str(8, i, j+1):
                            str_err += 'O '
                            list_temp.append(' ' * 37)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], 8, i, j) + f"__{self.table_str(8, i, j+1)}").rjust(37))

                else:   # 당년도 표

                    try:
                        excel.split(list_title[i])[1]
                    except:
                        with open("log.txt", "a", encoding="utf-8") as f:                    
                            f.write("excel_original06 (3-4)직급별평균단가 오류: " + list_title[i]  + '\n')
                        print("excel_original06 (3-4)직급별평균단가 오류: " + list_title[i]  + '\n')
                        QMessageBox.information(self, "(3-4)직급별평균단가 오류", "(3-4)직급별평균단가 오류: " + list_title[i])

                    

                    excel = excel.split(list_title[i])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]
                    
                    # str_err += self.text_table(i+2, 1) + '\t'
                    str_err += list_title[i] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 15):
                        if self.excel_str(excel_item.split('\t')[j], 8, i, j) == self.table_str(8, i+2, j+1):
                            str_err += 'O '
                            list_temp.append(' ' * 37)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], 8, i, j) + f"__{self.table_str(8, i+2, j+1)}").rjust(37))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-4) 직급별 평균단가 계산', '(3-4) 직급별 평균단가 계산\t불일치: [' + str(cnt_wrong) + '/224]')
            str_err_total += '(3-4) 직급별 평균단가 계산\t불일치: [' + str(cnt_wrong) + '/224]\n'
            str_err += '\n\n\n'






        if 1 == 1 or current_index == 9:
            list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '기능직', '계', '1급', '2급', '3급', '4급', '5급', '6급', '연구직', '기능직', '계']
            str_err += '(3-6) 가. 초임직급 정원\n\n당년도\n'
            str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>19}{'2월':>19}{'3월':>19}{'4월':>19}{'5월':>19}{'6월':>19}{'7월':>19}{'8월':>20}{'9월':>19}{'10월':>19}{'11월':>19}{'12월':>19}{'평균인원':>18}\n"

            excel_original07_09 = excel_original07.split('나.초임직급정원변동에따른인건비효과')[0]            
            excel = excel_original07_09

            cnt_wrong = 0
            for i in range (0, 18):

                if i == 9:
                    excel = excel_original07.split('전년도')[1]
                    str_err += '\n\n전년도\n'
                    str_err += '           1 2 3 4 5 6 7 8 9 101112평' + f"{'1월':>19}{'2월':>19}{'3월':>19}{'4월':>19}{'5월':>19}{'6월':>19}{'7월':>19}{'8월':>20}{'9월':>19}{'10월':>19}{'11월':>19}{'12월':>19}{'평균인원':>18}\n"

                if i < 9:   # 전년도 표
                    try:
                        excel.split(list_title[i])[1]
                    except:
                        with open("log.txt", "a", encoding="utf-8") as f:                    
                            f.write("excel_original07 (3-6)가.초임정원 오류: " + list_title[i]  + '\n')
                        print("excel_original07 (3-6)가.초임정원 오류: " + list_title[i]  + '\n')
                        QMessageBox.information(self, "(3-6)가.초임정원 오류", "(3-6)가.초임정원 오류: " + list_title[i])
                    

                    excel = excel.split(list_title[i])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]

                    
                    # str_err += self.text_table(i, 1) + '\t'
                    str_err += list_title[i] + '\t'
                    
                    list_temp = []                
                    for j in range(1, 14):
                        if self.excel_str(excel_item.split('\t')[j], 9, i, j) == self.table_str(9, i, j+1):
                            str_err += 'O '
                            list_temp.append(' ' * 20)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], 9, i, j) + f"__{self.table_str(9, i, j+1)}").rjust(20))

                else:   # 당년도 표
                    
                    try:
                        excel.split(list_title[i])[1]
                    except:
                        with open("log.txt", "a", encoding="utf-8") as f:                    
                            f.write("excel_original07 (3-6)가.초임정원 오류: " + list_title[i]  + '\n')
                        print("excel_original07 (3-6)가.초임정원 오류: " + list_title[i]  + '\n')
                        QMessageBox.information(self, "(3-6)가.초임정원 오류", "(3-6)가.초임정원 오류: " + list_title[i])
                    
                    excel = excel.split(list_title[i])[1] # 기본급
                    excel_item = excel.split('\r\n')[0]
                    
                    # str_err += self.text_table(i+2, 1) + '\t'
                    str_err += list_title[i] + '\t'

                    list_temp = []                
                    for j in range(1, 14):
                        if self.excel_str(excel_item.split('\t')[j], 9, i, j) == self.table_str(9, i+2, j+1):
                            str_err += 'O '
                            list_temp.append(' ' * 20)
                        else:
                            str_err += 'X '
                            cnt_wrong += 1
                            list_temp.append((self.excel_str(excel_item.split('\t')[j], 9, i, j) + f"__{self.table_str(9, i+2, j+1)}").rjust(20))

                str_err = str_err[:-1] + ''.join(list_temp) + '\n'
            str_err = str_err.replace('(3-6) 가. 초임직급 정원', '(3-6) 가. 초임직급 정원\t\t불일치: [' + str(cnt_wrong) + '/234]')
            str_err_total += '(3-6) 가. 초임직급 정원\t\t불일치: [' + str(cnt_wrong) + '/234]\n'
            str_err += '\n\n\n'






        if 1 == 1 or current_index == 10:
            list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '기능직', '계' ]
            str_err += '(3-6) 나. 초임직급 인건비\n\n'
            str_err += '           전당인전 증' + f"{'전년도인원(A)':>18}{'당년도인원(B)':>18}{'인원증감(C)':>18}{'전년도단가(D)':>22}{'증원인건비':>28}\n"
            excel_original07_10 = excel_original07.split('나.초임직급정원변동에따른인건비효과')[1]
            excel = excel_original07_10

            cnt_wrong = 0
            for i in range (0, 9):


                try:
                    excel.split(list_title[i])[1]
                except:
                    with open("log.txt", "a", encoding="utf-8") as f:                    
                        f.write("excel_original07 (3-6)초임인건비 오류: " + list_title[i]  + '\n')
                    print("excel_original07 (3-6)초임인건비 오류: " + list_title[i]  + '\n')


                
                excel = excel.split(list_title[i])[1] # 기본급
                excel_item = excel.split('\r\n')[0]   
                # str_err += self.text_table(i, 0) + '\t'
                str_err += list_title[i] + '\t'
                
                list_temp = []
                for j in range(1, 6):
                    if self.excel_str(excel_item.split('\t')[j], 10, i, j) == self.table_str(10, i, j):
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
            str_err = str_err.replace('(3-6) 나. 초임직급 인건비', '(3-6) 나. 초임직급 인건비\t불일치: [' + str(cnt_wrong) + '/45]')
            str_err += '\n'
            str_err_total += '(3-6) 나. 초임직급 인건비\t불일치: [' + str(cnt_wrong) + '/45]\n\n'











        str_err = str_err_total + '\n\n' + str_err

        return str_err














    if 1!=1:
        global excel_original01, excel_original02, excel_original03, excel_original04, excel_original05, excel_original06, excel_original07
        
        excel_original01 = '(2) 인건비 집계를 위한 Template\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t(단위: 원)\r\n인건비 항목\t\t\t판관비\t영업외비용\t 제조원가\t타계정대체\t이익잉여금\t합계\r\n"급료\n임금\n제수당"\t기본급\t\t 744,433,839,400 \t1\t\t\t7\t 744,433,839,400 \r\n\t상여금\t인센티브 상여금\t 50,727,850,151 \t\t\t\t\t 50,727,850,151 \r\n\t\t그 외 상여금\t 48,367,494,910 \t\t\t\t\t 48,367,494,910 \r\n\t제수당\t법정수당\t 66,931,057,610 \t\t\t\t\t 66,931,057,610 \r\n\t\t해외근무수당\t 50,000,000 \t\t\t\t\t 50,000,000 \r\n\t\t그 외 제수당\t 202,750,281,360 \t\t\t\t\t 202,750,281,360 \r\n\t퇴직급여(명예퇴직금 포함)\t\t 168,793,866,818 \t\t\t\t\t 168,793,866,818 \r\n\t임원 인건비\t\t 983,482,250 \t\t\t\t\t 983,482,250 \r\n\t비상임이사 인건비\t\t 600,000,000 \t\t\t\t\t 600,000,000 \r\n\t"인상률 제외\n인건비"\t통상임금소송결과에 따른 실적급여 증가액\t 70,000,000 \t\t\t\t\t 70,000,000 \r\n\t\t기타 제외 인건비\t 8,000,000 \t\t\t\t\t 8,000,000 \r\n\t기타항목\t\t 74,870,000 \t\t\t\t\t 74,870,000 \r\n\t급료, 임금, 제수당 소계 ⓐ\t\t 1,283,790,742,499 \t - \t - \t - \t - \t 1,283,790,742,499 \r\n"복 리\n후생비"\t사내근로복지기금출연금\t\t 700,000,000 \t\t\t\t\t 700,000,000 \r\n\t국민연금사용자부담분\t\t 38,566,372,740 \t\t\t\t\t 38,566,372,740 \r\n\t건강보험사용자부담분\t\t 41,634,941,020 \t\t\t\t\t 41,634,941,020 \r\n\t고용보험사용자부담분\t\t 18,164,674,530 \t\t\t\t\t 18,164,674,530 \r\n\t산재보험료사용자부담분\t\t 5,325,440,550 \t\t\t\t\t 5,325,440,550 \r\n\t급식비\t\t 700,000,000 \t\t\t\t\t 700,000,000 \r\n\t교통보조비\t\t 800,000,000,000 \t\t\t\t\t 800,000,000,000 \r\n\t자가운전보조금\t\t 60,000,000 \t\t\t\t\t 60,000,000 \r\n\t학자보조금\t\t 49,525,720 \t\t\t\t\t 49,525,720 \r\n\t건강진단비 등(독감예방주사비용)\t\t 173,882,997 \t\t\t\t\t 173,882,997 \r\n\t선택적복지\t\t 9,194,447,060 \t\t\t\t\t 9,194,447,060 \r\n\t행사비\t\t 700,000,000 \t\t\t\t\t 700,000,000 \r\n\t포상품(비)\t\t 52,602,620 \t\t\t\t\t 52,602,620 \r\n\t기념품(비)\t\t 80,000,000 \t\t\t\t\t 80,000,000 \r\n\t격려품(비)\t\t 7,000,000 \t\t\t\t\t 7,000,000 \r\n\t장기근속관련 비용\t\t 8,000,000 \t\t\t\t\t 8,000,000 \r\n\t육아보조비 및 출산장려금\t\t 743,000,000 \t\t\t\t\t 743,000,000 \r\n\t자기계발비\t\t 80,000,000 \t\t\t\t\t 80,000,000 \r\n\t특별근로의 대가\t\t 8,000,000 \t\t\t\t\t 8,000,000 \r\n\t피복비\t\t 700,000,000 \t\t\t\t\t 700,000,000 \r\n\t경로효친비\t\t 800,000,000 \t\t\t\t\t 800,000,000 \r\n\t통신비\t\t 5,000,000 \t\t\t\t\t 5,000,000 \r\n\t축하금/조의금\t\t 70,000,000 \t\t\t\t\t 70,000,000 \r\n\t기타금품 등\t\t 100,927,240 \t\t\t\t\t 100,927,240 \r\n\t복리후생비 소계 ⓑ\t\t 917,923,814,477 \t - \t - \t - \t - \t 917,923,814,477 \r\n"\'잡급 및 무기계약직에\n대한 인건비\'\n(복리후생비, 인센티브포함) ⓒ"\t\t일반 급여(1)\t 15,823,215,150 \t - \t - \t - \t - \t 15,823,215,150 \r\n\t\t 인센티브 상여금\t 7,000,000 \t\t\t\t\t 7,000,000 \r\n\t\t 순액\t 15,816,215,150 \t\t\t\t\t 15,816,215,150 \r\n\t\t청년인턴 급여(2)\t 9,414,136,240 \t - \t - \t - \t - \t 9,414,136,240 \r\n\t\t 인센티브 상여금\t 8,000,000 \t\t\t\t\t 8,000,000 \r\n\t\t 순액\t 9,406,136,240 \t\t\t\t\t 9,406,136,240 \r\n\t\t무기계약직 급여(3)\t 26,694,838,746 \t - \t - \t - \t - \t 26,694,838,746 \r\n\t\t 인센티브 상여금\t 1,256,862,230 \t\t\t\t\t 1,256,862,230 \r\n\t\t 순액\t 25,437,976,516 \t\t\t\t\t 25,437,976,516 \r\n\t\t소계 ⓒ=(1)+(2)+(3)\t 51,932,190,136 \t - \t - \t - \t - \t 51,932,190,136 \r\n\t\t\t\t\t\t\t\t\r\n인건비 총계 : ⓓ=ⓐ+ⓑ+ⓒ\t\t\t 2,253,646,747,112 \t - \t - \t - \t - \t 2,253,646,747,112 \r\n인센티브 상여금 ⓔ=ⓔ-1+ⓔ-2\t\t\t 51,984,712,381 \t - \t - \t - \t - \t 51,984,712,381 \r\n- 인센티브 전환금 (ⓔ-1)\t\t\t 43,589,629,529 \t\t\t\t\t 43,589,629,529 \r\n- 인센티브 추가금 (ⓔ-2)\t\t\t 8,395,082,852 \t\t\t\t\t 8,395,082,852 \r\n인건비 해당금액 : ⓓ-ⓔ\t\t\t 2,201,662,034,731 \t - \t - \t - \t - \t 2,201,662,034,731 \r\n\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\r\n'
        excel_original01 = excel_original01.replace(' ', '').replace('\t-\t', '\t\t')

        excel_original02 = '(3)총인건비인상률지표의점수계산을위한Template\t\t\t\t\r\n\t\t\t\t(단위:원)\r\n구분\t\t\t2024\t2023\r\n\t1.인센티브상여금을제외한인건비총액\t\t\t\r\n\ta.판관비로처리한인건비\t\t1,397,001,034,731\t1,298,932,744,191\r\n\tb.영업외비용으로처리한인건비\t\t-\t-\r\n\tc.제조원가로처리한인건비\t\t-\t-\r\n\td.타계정대체로처리한인건비\t\t-\t-\r\n\te.이익잉여금의증감으로처리한인건비\t\t-\t-\r\n\t소계:(A)=a+b+c+d+e\t\t1,397,001,034,731\t1,298,932,744,191\r\n\t\t\t\t\r\n\t2.총인건비 인상률계산에서제외(조정)되는인건비\t\t\t\r\n\tf.퇴직급여(명예퇴직금포함)\t\t168,793,866,818\t141,500,433,647\r\n\tg.임원인건비\t\t983,482,250\t771,999,300\r\n\th.비상임이사인건비\t\t-\t-\r\n\ti.인상률제외인건비\t통상임금소송결과에따른실 적급여증가액\t-\t-\r\n\t\t기타제외인건비\t-\t-\r\n\tj.사내근로복지기금출연금\t\t-\t-\r\n\tk.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)\t\t50,660,327,906\t50,195,933,210\r\n\tl.공적보험사용자부담분\t\t103,691,428,840\t104,545,198,290\r\n\tm.연월차수당등조정(㉠-㉡+㉢)\t\t71,795,906,667\t-2,930,735,981\r\n\t-연월차수당등발생액(㉠)\t\t123,325,995,917\t63,001,832,519\r\n\t-연월차수당등지급액(㉡)\t\t51,530,089,250\t65,932,568,500\r\n\t-종업원저리대여금이 자관련인건비(㉢)\t\t-\t-\r\n\tn.저리·무상대여이익\t\t4,725,943,920\t5,598,293,980\r\n\to.지방이전관련직접인건비\t\t-\t-\r\n\tp.법령에따른특수건강진단비\t\t-\t-\r\n\tq.코로나19대응을위한시간외근로수당등\t\t-\t-\r\n\tr.해외근무수당\t\t-\t-\r\n\ts.직무발명보상금\t\t-\t-\r\n\tt.공무원수준내의자녀수당및출산격려금\t\t3,051,903,476\t1,832,315,628\r\n\tu.야간간호특별수당\t\t-\t-\r\n\tv.비상진료체계운영에따른특별수당등\t\t-\t-\r\n\tu.국민건강보험공단2023년도총인건비초과액에따른상환금액\t\t-\t22,500,000,000\r\n\t소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s+t+u+v+w\t\t394,250,972,037\t312,816,850,114\r\n\t\t\t\t\r\n\t3.실집행액기준총인건비발생액(C)=(A)-(B)\t\t1,002,750,062,694\t986,115,894,077\r\n\t\t\t\t\r\n"전년대비\n조정된\n총인건비\n발생액\n산출"\t4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)\t\t\t-8,039,360,305\r\n\t5.별도직군승진시기차이에따른인건비효과조정(E)\t\t\t\r\n\t6.초임직급정원변동에따른인건비효과조정(F)\t\t\t-511,459,730\r\n\t7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)\t\t\t\r\n\t8.생산량증가로인하여\'23년도\'에추가로지급된인건비의영향제거(H)\t\t\tn/a\r\n\t9.최저임금지급직원에대한인건비효과조정(I)\t\t\t\r\n\t10.파업등에따른인건비효과조정(J)\t\t\t\r\n\t11.코로나19로인한휴업의인건비효과조정(K)\t\t\t\r\n\t"12.총인건비인상률계산대상총인건비발생액\n=(C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)+(K)+(L)"\t\t1,002,750,062,694\t978,587,993,501\r\n\t\t\t\t\r\n"당해연도\n총인건비\n인상률\n계산"\t13.총인건비인상률가이드라인에따른총인건비상한액\t\tn/a\tn/a\r\n\t(1)\'23년도총인건비인상률가이드라인을준수한경우\t\t\t978,587,993,501\r\n\t(2)\'23년도총인건비인상률가이드라인을준수경우하지않은경우\t\t\t-\r\n\t\t\t\t\r\n\t14.총인건비인상률 산출(\'24년도총인건비인상률가이드라인=2.5%)\t\tn/a\t\r\n\t(1)\'23년도총인건비인상률가이드라인을준수한경우\t\t2.469%\t\r\n\t(2)\'23년도총인건비인상률가이드라인을준수경우하지않은경우\t\t-\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\r\n'
        excel_original02 = excel_original02.replace(' ', '').replace('\t-\t', '\t\t')
        
        excel_original03 = '(3-1) 증원소요 인건비 계산을 위한 Template\t\t\t\t\t\t\r\n\t\t\t\t\t(단위: 명, 원)\t\r\n직급\t인원\t\t\t"전년도의\n평균단가\n(D)"\t"증원소요 인건비\n(C) x (D)"\t\r\n\t"전년도\n(A)"\t"당년도\n(B)"\t"증감\n(C)=(B)-(A)"\t\t\t\r\n1급\t133.0 \t133.0 \t -  \t99,310,634 \t -  \t\r\n2급\t589.0 \t589.0 \t -  \t92,457,982 \t -  \t\r\n3급\t2,437.1 \t2,444.9 \t7.8 \t86,403,138 \t673,944,476 \t\r\n4급\t4,314.5 \t4,060.4 \t△254.1 \t77,428,700 \t△19,674,632,670 \t\r\n5급\t3,887.0 \t4,251.8 \t364.8 \t53,434,940 \t19,493,066,112 \t\r\n6급\t3,466.0 \t3,269.3 \t△196.7 \t44,091,356 \t△8,672,769,725 \t\r\n연 구직\t136.9 \t138.8 \t1.9 \t74,227,106 \t141,031,501 \t\r\n계\t14,963.5 \t14,887.2 \t△76.3 \t\t△8,039,360,305 \t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n'
        excel_original03 = excel_original03.replace(' ', '').replace('\t-\t', '\t\t')

        excel_original04 = '(3-2) 직급별 평균인원 계산을 위한 Template\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\r\n전년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균인원\t\r\n\t1급\t 166.0 \t 166.0 \t 167.0 \t 167.0 \t 167.0 \t 167.0 \t 159.0 \t 158.0 \t 158.0 \t 158.0 \t 158.0 \t 158.0 \t 162.4 \t\r\n\t2급\t 678.0 \t 678.0 \t 680.0 \t 680.0 \t 680.0 \t 678.0 \t 669.0 \t 669.0 \t 671.0 \t 670.0 \t 668.0 \t 670.0 \t 674.3 \t\r\n\t3급\t 2,598.0 \t 2,594.0 \t 2,591.0 \t 2,587.0 \t 2,584.0 \t 2,586.0 \t 2,555.0 \t 2,547.0 \t 2,548.0 \t 2,550.0 \t 2,549.0 \t 2,551.8 \t 2,570.1 \t\r\n\t4급\t 4,039.0 \t 4,189.8 \t 4,180.0 \t 4,174.5 \t 4,173.3 \t 4,168.3 \t 3,985.0 \t 3,967.5 \t 3,992.8 \t 3,981.3 \t 3,974.3 \t 3,977.5 \t 4,066.9 \t\r\n\t5급\t 4,011.3 \t 3,815.5 \t 3,797.0 \t 3,785.3 \t 3,773.5 \t 3,761.8 \t 3,966.8 \t 3,959.8 \t 3,988.0 \t 3,942.0 \t 3,916.0 \t 3,927.5 \t 3,887.0 \t\r\n\t6급\t 3,440.0 \t 3,432.0 \t 3,437.3 \t 3,440.5 \t 3,436.5 \t 3,439.8 \t 3,451.0 \t 3,439.0 \t 3,445.0 \t 3,423.5 \t 3,425.5 \t 3,782.0 \t 3,466.0 \t\r\n\t연구직\t 145.0 \t 140.0 \t 136.0 \t 133.0 \t 133.0 \t 133.0 \t 139.0 \t 138.0 \t 135.0 \t 135.0 \t 136.0 \t 139.8 \t 136.9 \t\r\n\t계\t 15,077.3 \t 15,015.3 \t 14,988.3 \t 14,967.3 \t 14,947.3 \t 14,933.8 \t 14,924.8 \t 14,878.3 \t 14,937.8 \t 14,859.8 \t 14,826.8 \t 15,206.5 \t 14,963.6 \t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\r\n당년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균인원\t\r\n\t1급\t 162.00 \t 162.00 \t 161.00 \t 160.00 \t 159.00 \t 158.00 \t 165.00 \t 165.00 \t 165.00 \t 165.00 \t 165.00 \t 165.00 \t 162.70 \t\r\n\t2급\t 678.00 \t 678.00 \t 678.00 \t 678.00 \t 678.00 \t 678.00 \t 670.00 \t 669.00 \t 669.00 \t 669.00 \t 669.00 \t 667.00 \t 673.40 \t\r\n\t3급\t 2,583.00 \t 2,579.00 \t 2,573.75 \t 2,566.50 \t 2,556.75 \t 2,561.00 \t 2,575.00 \t 2,571.75 \t 2,572.75 \t 2,569.75 \t 2,568.50 \t 2,569.50 \t 2,570.60 \t\r\n\t4급\t 3,877.75 \t 3,854.75 \t 3,847.75 \t 3,840.75 \t 3,835.00 \t 3,842.50 \t 3,526.50 \t 3,855.75 \t 3,853.00 \t 3,842.25 \t 3,834.50 \t 3,837.50 \t 3,820.70 \t\r\n\t5급\t 4,149.25 \t 4,126.25 \t 4,119.00 \t 4,117.75 \t 4,105.75 \t 4,119.50 \t 4,673.25 \t 4,325.50 \t 4,348.25 \t 4,318.50 \t 4,312.25 \t 4,306.75 \t 4,251.80 \t\r\n\t6급\t 3,319.75 \t 3,318.00 \t 3,307.50 \t 3,302.75 \t 3,292.50 \t 3,292.00 \t 3,155.25 \t 3,156.00 \t 3,160.00 \t 3,160.00 \t 3,160.75 \t 3,607.50 \t 3,269.30 \t\r\n\t연구직\t 138.00 \t 139.00 \t 136.00 \t 135.00 \t 134.00 \t 136.00 \t 137.00 \t 141.00 \t 139.00 \t 139.00 \t 146.00 \t 145.00 \t 138.80 \t\r\n\t계\t 14,907.75 \t 14,857.00 \t 14,823.00 \t 14,800.75 \t 14,761.00 \t 14,787.00 \t 14,902.00 \t 14,884.00 \t 14,907.00 \t 14,863.50 \t 14,856.00 \t 15,298.25 \t 14,887.30 \t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n'
        excel_original04 = excel_original04.replace(' ', '').replace('\t-\t', '\t\t')

        excel_original05 = '(3-3) 근속승진 및 증원소요인건비 대상 인원의 파악\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n가. 정원 및 현원 차이\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\t\t\t\t\t\t\t\r\n당년도\t직급\t1 월\t\t\t\t2월\t\t\t\t3월\t\t\t\t4월\t\t\t\t5월\t\t\t\t6월\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t\t\t\t\t\t\t\t\r\n\t1급\t133 \t162.0 \t0.0 \t-29.0 \t133 \t162.0 \t0.0 \t-29.0 \t133 \t161.0 \t0.0 \t-28.0 \t133 \t160.0 \t0.0 \t-27.0 \t133 \t159.0 \t0.0 \t-26.0 \t133 \t158.0 \t0.0 \t-25.0 \t\t\t\t\t\t\t\t\r\n\t2급\t589 \t678.0 \t0.0 \t-118.0 \t589 \t678.0 \t0.0 \t-118.0 \t589 \t678.0 \t0.0 \t-117.0 \t589 \t678.0 \t0.0 \t-116.0 \t589 \t678.0 \t0.0 \t-115.0 \t589 \t678.0 \t0.0 \t-114.0 \t\t\t\t\t\t\t\t\r\n\t3급\t2,382 \t2,583.0 \t51.0 \t-268.0 \t2,382 \t2,579.0 \t47.0 \t-268.0 \t2,382 \t2,573.8 \t46.0 \t-262.8 \t2,382 \t2,566.5 \t47.0 \t-253.5 \t2,382 \t2,556.8 \t46.0 \t-243.8 \t2,382 \t2,561.0 \t46.0 \t-247.0 \t\t\t\t\t\t\t\t\r\n\t4급\t8,518 \t3,877.8 \t0.0 \t4,372.3 \t8,518 \t3,854.8 \t0.0 \t4,395.3 \t8,518 \t3,847.8 \t0.0 \t4,407.5 \t8,518 \t3,840.8 \t0.0 \t4,423.8 \t8,518 \t3,835.0 \t0.0 \t4,439.3 \t8,518 \t3,842.5 \t0.0 \t4,428.5 \t\t\t\t\t\t\t\t\r\n\t5급\t1,280 \t4,149.3 \t0.0 \t1,503.0 \t1,280 \t4,126.3 \t0.0 \t1,549.0 \t1,280 \t4,119.0 \t0.0 \t1,568.5 \t1,280 \t4,117.8 \t0.0 \t1,586.0 \t1,280 \t4,105.8 \t0.0 \t1,613.5 \t1,280 \t4,119.5 \t0.0 \t1,589.0 \t\t\t\t\t\t\t\t\r\n\t6급\t2,479 \t3,319.8 \t0.0 \t662.3 \t2,479 \t3,318.0 \t0.0 \t710.0 \t2,479 \t3,307.5 \t0.0 \t740.0 \t2,479 \t3,302.8 \t0.0 \t762.3 \t2,479 \t3,292.5 \t0.0 \t800.0 \t2,479 \t3,292.0 \t0.0 \t776.0 \t\t\t\t\t\t\t\t\r\n\t연구직\t157 \t138.0 \t0.0 \t0.0 \t157 \t139.0 \t0.0 \t0.0 \t157 \t136.0 \t0.0 \t0.0 \t157 \t135.0 \t0.0 \t0.0 \t157 \t134.0 \t0.0 \t0.0 \t157 \t136.0 \t0.0 \t0.0 \t\t\t\t\t\t\t\t\r\n\t계\t15,538 \t14,907.8 \t51.0 \t\t15,538 \t14,857.0 \t47.0 \t\t15,538 \t14,823.0 \t46.0 \t\t15,538 \t14,800.8 \t47.0 \t\t15,538 \t14,761.0 \t46.0 \t\t15,538 \t14,787.0 \t46.0 \t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n당년도\t직급\t7월\t\t\t\t8월\t\t\t\t9월\t\t\t\t10월\t\t\t\t11월\t\t\t\t12월\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t정원\t 현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t정원\t현원\t복직자\t누적차\t\t\t\t\t\t\t\t\r\n\t1급\t133 \t165.0 \t0.0 \t-32.0 \t133 \t165.0 \t0.0 \t-32.0 \t133 \t165.0 \t0.0 \t-32.0 \t133 \t165.0 \t0.0 \t-32.0 \t133 \t165.0 \t0.0 \t-32.0 \t133 \t165.0 \t0.0 \t-32.0 \t\t\t\t\t\t\t\t\r\n\t2급\t589 \t670.0 \t0.0 \t-113.0 \t589 \t669.0 \t0.0 \t-112.0 \t589 \t669.0 \t0.0 \t-112.0 \t589 \t669.0 \t0.0 \t-112.0 \t589 \t669.0 \t0.0 \t-112.0 \t589 \t667.0 \t0.0 \t-110.0 \t\t\t\t\t\t\t\t\r\n\t3급\t2,399 \t2,575.0 \t66.0 \t-223.0 \t2,399 \t2,571.8 \t63.0 \t-221.8 \t2,399 \t2,572.8 \t60.0 \t-225.8 \t2,399 \t2,569.8 \t60.0 \t-222.8 \t2,399 \t2,568.5 \t60.0 \t-221.5 \t2,399 \t2,569.5 \t61.0 \t-219.5 \t\t\t\t\t\t\t\t\r\n\t4급\t8,547 \t3,526.5 \t0.0 \t4,797.5 \t8,547 \t3,855.8 \t0.0 \t4,469.5 \t8,547 \t3,853.0 \t0.0 \t4,468.3 \t8,547 \t3,842.3 \t0.0 \t4,482.0 \t8,547 \t3,834.5 \t0.0 \t4,491.0 \t8,547 \t3,837.5 \t0.0 \t4,490.0 \t\t\t\t\t\t\t\t\r\n\t5급\t1,284 \t4,673.3 \t0.0 \t1,408.3 \t1,284 \t4,325.5 \t0.0 \t1,428.0 \t1,284 \t4,348.3 \t0.0 \t1,404.0 \t1,284 \t4,318.5 \t0.0 \t1,447.5 \t1,284 \t4,312.3 \t0.0 \t1,462.8 \t1,284 \t4,306.8 \t0.0 \t1,467.3 \t\t\t\t\t\t\t\t\r\n\t6급\t2,551 \t3,155.3 \t0.0 \t804.0 \t2,551 \t3,156.0 \t0.0 \t823.0 \t2,551 \t3,160.0 \t0.0 \t795.0 \t2,551 \t3,160.0 \t0.0 \t838.5 \t2,551 \t3,160.8 \t0.0 \t853.0 \t2,551 \t3,607.5 \t0.0 \t410.8 \t\t\t\t\t\t\t\t\r\n\t연구직\t157 \t137.0 \t0.0 \t0.0 \t157 \t141.0 \t0.0 \t0.0 \t157 \t139.0 \t0.0 \t0.0 \t157 \t139.0 \t0.0 \t0.0 \t157 \t146.0 \t0.0 \t0.0 \t157 \t145.0 \t0.0 \t0.0 \t\t\t\t\t\t\t\t\r\n\t계\t15,660 \t14,902.0 \t66.0 \t\t15,660 \t14,884.0 \t63.0 \t\t15,660 \t14,907.0 \t60.0 \t\t15,660 \t14,863.5 \t60.0 \t\t15,660 \t14,856.0 \t60.0 \t\t15,660 \t15,298.3 \t61.0 \t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n'
        excel_original05 += '나. 근속승진\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n당년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t1급\t29.0\t29.0\t28.0\t27.0\t26.0\t25.0\t32.0\t32.0\t32.0\t32.0\t32.0\t32.0\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t2급\t89.0\t89.0\t89.0\t89.0\t89.0\t89.0\t81.0\t80.0\t80.0\t80.0\t80.0\t78.0\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t3급\t150.0\t150.0\t145.8\t137.5\t128.8\t133.0\t110.0\t109.8\t113.8\t110.8\t109.5\t109.5\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t4급\t-268.0\t-268.0\t-262.8\t-253.5\t-243.8\t-247.0\t-223.0\t-221.8\t-225.8\t-222.8\t-221.5\t-219.5\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t5급\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t6급\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t연구직\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t계\t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t0.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n다. 증원소요인건비 대상 인원\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n당년도\t직급\t1월\t2월\t3월\t4 월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균인원\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t1급\t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t2급\t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t3급\t2,433.0 \t2,429.0 \t2,428.0 \t2,429.0 \t2,428.0 \t2,428.0 \t2,465.0 \t2,462.0 \t2,459.0 \t2,459.0 \t2,459.0 \t2,460.0 \t2,444.9 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t4급\t4,145.8 \t4,122.8 \t4,110.5 \t4,094.3 \t4,078.8 \t4,089.5 \t3,749.5 \t4,077.5 \t4,078.8 \t4,065.0 \t4,056.0 \t4,057.0 \t4,060.4 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t5급\t4,149.3 \t4,126.3 \t4,119.0 \t4,117.8 \t4,105.8 \t4,119.5 \t4,673.3 \t4,325.5 \t4,348.3 \t4,318.5 \t4,312.3 \t4,306.8 \t4,251.8 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t6급\t3,319.8 \t3,318.0 \t3,307.5 \t3,302.8 \t3,292.5 \t3,292.0 \t3,155.3 \t3,156.0 \t3,160.0 \t3,160.0 \t3,160.8 \t3,607.5 \t3,269.3 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t연구직\t138.0 \t139.0 \t136.0 \t135.0 \t134.0 \t136.0 \t137.0 \t141.0 \t139.0 \t139.0 \t146.0 \t145.0 \t138.8 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t계\t14,907.8 \t14,857.0 \t14,823.0 \t14,800.8 \t14,761.0 \t14,787.0 \t14,902.0 \t14,884.0 \t14,907.0 \t14,863.5 \t14,856.0 \t15,298.3 \t14,887.2 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n전년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균인원\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t1급\t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t133.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t2급\t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t589.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t3급\t2,435.8 \t2,434.8 \t2,435.0 \t2,435.8 \t2,434.8 \t2,436.5 \t2,443.3 \t2,441.3 \t2,438.0 \t2,437.0 \t2,437.0 \t2,436.0 \t2,437.1 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t4급\t4,323.2 \t4,471.0 \t4,461.0 \t4,450.7 \t4,447.5 \t4,440.8 \t4,202.7 \t4,178.2 \t4,209.8 \t4,200.3 \t4,190.3 \t4,199.3 \t4,314.5 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t5급\t4,011.3 \t3,815.5 \t3,797.0 \t3,785.3 \t3,773.5 \t3,761.8 \t3,966.8 \t3,959.8 \t3,988.0 \t3,942.0 \t3,916.0 \t3,927.5 \t3,887.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t6급\t3,440.0 \t3,432.0 \t3,437.3 \t3,440.5 \t3,436.5 \t3,439.8 \t3,451.0 \t3,439.0 \t3,445.0 \t3,423.5 \t3,425.5 \t3,782.0 \t3,466.0 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t연구직\t145.0 \t140.0 \t136.0 \t133.0 \t133.0 \t133.0 \t139.0 \t138.0 \t135.0 \t135.0 \t136.0 \t139.8 \t136.9 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t계\t15,077.3 \t15,015.3 \t14,988.3 \t14,967.3 \t14,947.3 \t14,933.8 \t14,924.8 \t14,878.3 \t14,937.8 \t14,859.8 \t14,826.8 \t15,206.5 \t14,963.5 \t\tt\r\n'
        excel_original05 = excel_original05.replace(' ', '').replace('\t-\t', '\t\t')
        
        excel_original06 = '(3-4) 직급별 평균단가 계산을 위한 Template\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 원)\r\n전년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t 12월 \t"인건비\n총계"\t평균인원\t"직급별\n평균단가\n(수정 전)"\t"공무원 수준 내\n가족(자녀)수당"\t"공무원 수준 내\n출산축하금"\t"총인건비 차감 액\n(225억원)"\t"인건비 총계\n(수정 후)"\t"직급별\n평균단가"\r\n\t1급\t 1,321,802,810 \t 1,291,429,920 \t 1,326,000,290 \t 1,326,201,640 \t 1,268,376,330 \t 1,330,114,040 \t 1,733,986,960 \t 1,320,458,570 \t 1,312,172,040 \t 1,312,139,870 \t 1,315,490,040 \t 1,637,182,180 \t 16,495,354,690 \t 162.4 \t 101,572,381 \t - \t - \t 367,307,772 \t 16,128,046,918 \t 99,310,634 \r\n\t2급\t 4,948,980,180 \t 4,863,629,030 \t 4,953,343,590 \t 4,954,987,280 \t 4,769,837,630 \t 4,975,979,063 \t 6,451,898,160 \t 5,095,134,530 \t 5,091,679,310 \t 5,094,012,550 \t 5,088,037,870 \t 7,476,759,374 \t 63,764,278,567 \t 674.3 \t 94,563,664 \t\t - \t 1,419,861,260 \t 62,344,417,307 \t 92,457,982 \r\n\t3급\t 19,111,270,460 \t 17,320,263,020 \t 19,035,988,790 \t 17,316,149,340 \t 17,301,048,560 \t 20,258,047,323 \t 17,060,089,490 \t 17,042,175,518 \t 20,405,748,920 \t 17,024,524,280 \t 17,062,985,470 \t 28,690,840,311 \t 227,629,131,482 \t 2,570.1 \t 88,568,200 \t 493,728,590 \t 2,000,000 \t 5,068,696,653 \t 222,064,706,239 \t 86,403,138 \r\n\t4급\t 27,973,217,490 \t 25,314,121,630 \t 27,873,909,550 \t 25,211,744,390 \t 25,201,347,530 \t 26,581,898,988 \t 23,809,210,590 \t 23,736,133,130 \t 28,723,590,960 \t 23,824,586,280 \t 23,750,159,250 \t 40,926,953,862 \t 322,926,873,650 \t 4,066.9 \t 79,403,692 \t 796,369,178 \t 45,000,000 \t 7,190,724,460 \t 314,894,780,012 \t 77,428,700 \r\n\t5급\t 17,284,675,850 \t 15,464,665,320 \t 17,260,224,060 \t 15,372,935,600 \t 15,371,757,040 \t 17,199,384,134 \t 16,081,394,090 \t 16,153,774,921 \t 20,025,879,960 \t 16,191,904,800 \t 16,111,683,600 \t 30,354,439,609 \t 212,872,718,984 \t 3,887.0 \t 54,765,299 \t 329,995,920 \t 101,000,000 \t 4,740,110,509 \t 207,701,612,555 \t 53,434,940 \r\n\t6급\t 12,923,915,810 \t 11,492,535,180 \t 12,878,647,990 \t 11,552,605,610 \t 11,568,258,340 \t 13,256,094,043 \t 11,055,966,180 \t 11,589,625,850 \t 14,279,261,000 \t 11,550,381,140 \t 11,561,789,550 \t 22,657,653,654 \t 156,366,734,347 \t 3,466.0 \t 45,114,465 \t 47,221,940 \t 17,000,000 \t 3,481,872,192 \t 152,820,640,215 \t 44,091,356 \r\n\t연구직\t 858,793,160 \t 842,878,770 \t 819,288,680 \t 794,829,380 \t 788,109,900 \t 787,871,080 \t 804,115,530 \t 825,729,100 \t 807,479,280 \t 790,436,900 \t 810,932,730 \t 1,462,653,475 \t 10,393,117,985 \t 136.9 \t 75,917,589 \t - \t - \t 231,427,155 \t 10,161,690,830 \t 74,227,106 \r\n\t계\t 84,422,655,760 \t 76,589,522,870 \t 84,147,402,950 \t 76,529,453,240 \t 76,268,735,330 \t 84,389,388,671 \t 76,996,661,000 \t 75,763,031,619 \t 90,645,811,470 \t 75,787,985,820 \t 75,701,078,510 \t 133,206,482,465 \t 1,010,448,209,705 \t 14,963.6 \t 67,527,080 \t 1,667,315,628 \t 165,000,000 \t 22,500,000,000 \t 986,115,894,077 \t 65,900,979 \r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 원)\t\t\t\t\t\r\n당년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t 12월 \t"인건비\n총계"\t평균인원\t"직급별\n평균단가"\t\t\t\t\t\r\n\t1급\t 1,289,093,280 \t 1,301,470,470 \t 1,282,011,870 \t 1,294,314,070 \t 1,273,310,800 \t 1,266,833,110 \t 1,823,613,250 \t 1,377,821,680 \t 1,376,883,040 \t 1,377,071,790 \t 1,377,552,390 \t 1,543,436,610 \t 16,583,412,360 \t 162.7 \t 101,926,321 \t\t\t\t\t\r\n\t2급\t 5,041,228,250 \t 5,037,789,130 \t 5,038,918,830 \t 5,036,626,310 \t 5,028,001,270 \t 5,039,934,860 \t 6,644,537,710 \t 5,224,911,050 \t 5,219,179,220 \t 5,219,764,100 \t 5,220,681,520 \t 5,981,594,485 \t 63,733,166,735 \t 673.4 \t 94,643,847 \t\t\t\t\t\r\n\t3급\t 17,625,397,980 \t 19,344,193,980 \t 19,650,934,360 \t 17,536,858,650 \t 17,347,801,340 \t 19,553,311,730 \t 17,587,988,237 \t 17,519,558,340 \t 21,352,936,869 \t 17,542,838,840 \t 17,530,272,050 \t 24,306,822,638 \t 226,898,915,014 \t 2,570.6 \t 88,266,909 \t\t\t\t\t\r\n\t4급\t 23,541,146,470 \t 25,996,996,330 \t 26,409,785,160 \t 23,431,021,930 \t 23,228,242,220 \t 26,394,368,690 \t 21,477,194,120 \t 22,996,134,860 \t 28,449,719,510 \t 23,030,309,980 \t 23,019,346,970 \t 31,547,253,484 \t 299,521,519,724 \t 3,820.7 \t 78,394,409 \t\t\t\t\t\r\n\t5급\t 17,441,936,300 \t 19,518,492,260 \t 19,897,277,120 \t 17,437,728,740 \t 17,343,345,220 \t 19,981,102,910 \t 19,756,931,320 \t 18,280,688,130 \t 23,216,590,420 \t 18,386,888,560 \t 18,335,357,990 \t 27,101,369,172 \t 236,697,708,142 \t 4,251.8 \t 55,670,001 \t\t\t\t\t\r\n\t6급\t 11,643,907,510 \t 12,952,398,370 \t 13,176,416,364 \t 11,512,510,520 \t 11,503,845,320 \t 13,171,697,790 \t 10,234,872,400 \t 11,611,045,360 \t 13,778,287,160 \t 10,972,489,010 \t 10,996,629,300 \t 17,273,398,355 \t 148,827,497,459 \t 3,269.3 \t 45,522,741 \t\t\t\t\t\r\n\t연구직\t 879,506,520 \t 869,343,780 \t 865,985,430 \t 843,876,470 \t 826,613,590 \t 835,660,310 \t 841,369,650 \t 846,139,520 \t 869,109,910 \t 856,415,910 \t 853,742,870 \t 1,100,079,300 \t 10,487,843,260 \t 138.8 \t 75,560,830 \t\t\t\t\t\r\n\t계\t 77,462,216,310 \t 85,020,684,320 \t 86,321,329,134 \t 77,092,936,690 \t 76,551,159,760 \t 86,242,909,400 \t 78,366,506,687 \t 77,856,298,940 \t 94,262,706,129 \t 77,385,778,190 \t 77,333,583,090 \t 108,853,954,044 \t 1,002,750,062,694 \t 14,887.3 \t 67,356,073 \t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n'
        excel_original06 = excel_original06.replace(' ', '').replace('\t-\t', '\t\t')

        excel_original07 = '(3-6) 초임직급 정원변동에 따른 인건비 효과 조정을 위한 Template\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n가. 초임직급 정원\t\t\t\t\t\t\t\t\t\t\t\t\t\t(단위: 명)\t\t\t\t\t\t\t\r\n당년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균정원\t\t\t\t\t\t\t\r\n\t1급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t2급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t3급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t4급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t5급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t6급\t575 \t575 \t575 \t575 \t575 \t642 \t642 \t642 \t642 \t642 \t642 \t642 \t614.1 \t\t\t\t\t\t\t\r\n\t연구직\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t기능직\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t계\t575 \t575 \t575 \t575 \t575 \t642 \t642 \t642 \t642 \t642 \t642 \t642 \t614.1 \t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n전년도\t직급\t1월\t2월\t3월\t4월\t5월\t6월\t7월\t8월\t9월\t10월\t11월\t12월\t평균정원\t\t\t\t\t\t\t\r\n\t1급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t2급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t3급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t4급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t5급\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t6급\t657 \t657 \t657 \t657 \t657 \t608 \t608 \t608 \t608 \t608 \t608 \t575 \t625.7 \t\t\t\t\t\t\t\r\n\t연구직\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t기능직\t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0 \t0.0 \t\t\t\t\t\t\t\r\n\t계\t657 \t657 \t657 \t657 \t657 \t608 \t608 \t608 \t608 \t608 \t608 \t575 \t625.7 \t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n나. 초임직급 정원 변동에 따른 인건비 효과\t\t\t\t\t\t(단위: 명, 원)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n구분\t정원\t\t\t"전년도의\n평균단가\n(D)"\t"인건비 효과\n(E) = (C) x (D)"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t"전년도\n(A)"\t"당년도\n(B)"\t"증감\n(C)=(B)-(A)"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n1급\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n2급\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n3급\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n4급\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n5급\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n6급\t 625.7 \t 614.1 \t-11.6 \t44,091,356 \t-511,459,730 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n연구직\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n기능직\t - \t - \t - \t - \t - \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n계\t 625.7 \t 614.1 \t-11.6 \t\t-511,459,730 \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n'
        excel_original07 = excel_original07.replace(' ', '').replace('\t-\t', '\t\t')



















    def excel_input(self):


        global excel_original01, excel_original02, excel_original03, excel_original04, excel_original05, excel_original06, excel_original07




        
        rank_count = 8  # 직급 수 설정
        
        
        # s1 ############################################################################

        list_title = ['기본급\t', '인센티브상여금', '그외상여금', '법정수당', '해외근무수당', '그외제수당', '퇴직급여(명예퇴직금포함)\t', '임원인건비\t', '비상임이사인건비\t',
                      '통상임금소송결과에따른실적급여증가액', '기타제외인건비', '기타항목\t', '급료,임금,제수당소계ⓐ\t',  '사내근로복지기금출연금\t', '국민연금사용자부담분\t',
                      '건강보험사용자부담분\t', '고용보험사용자부담분\t', '산재보험료사용자부담분\t', '급식비\t', '교통보조비\t', '자가운전보조금\t', '학자보조금\t','건강진단비등(독감예방주사비용)\t',
                      '선택적복지\t', '행사비\t', '포상품(비)\t', '기념품(비)\t', '격려품(비)\t', '장기근속관련비용\t', '육아보조비및출산장려금\t', '자기계발비\t', '특별근로의대가\t',
                      '피복비\t', '경로효친비\t', '통신비\t', '축하금/조의금\t', '기타금품등\t', '복리후생비소계ⓑ\t', '일반급여(1)', '인센티브상여금', '순액', '청년인턴급여(2)', '인센티브상여금', '순액', '무기계약직급여(3)',
                      '인센티브상여금', '순액', '소계ⓒ=(1)+(2)+(3)', '인건비총계:ⓓ=ⓐ+ⓑ+ⓒ\t\t', '인센티브상여금ⓔ=ⓔ-1+ⓔ-2\t\t', '인센티브전환금(ⓔ-1)\t\t', '인센티브추가금(ⓔ-2)\t\t', '인건비해당금액:ⓓ-ⓔ\t\t']

        excel = excel_original01
        
        # S1.py에서 정의된 보호 행(파란색) 목록
        readonly_rows = [12, 37, 38, 41, 44, 47, 48, 49, 52]
        
        self.s1.table.blockSignals(True)

        for i in range(0, 53):

            if i == 39: excel = excel_original01.split('일반급여(1)')[1]    
            if i == 42: excel = excel_original01.split('청년인턴급여(2)')[1]
            if i == 45: excel = excel_original01.split('무기계약직급여(3)')[1]
            if i == 49: excel = excel_original01.split('인건비총계:ⓓ=ⓐ+ⓑ+ⓒ')[1]




            try:
                # 1. 항목 존재 여부 체크
                try:
                    excel.split(list_title[i])[1]
                except:
                    return
                    # 항목을 못 찾으면 로그 기록 후 다음 항목으로
                    continue

                # 2. 데이터 추출


                excel = excel.split(list_title[i])[1]
                excel_item = excel.split('\r\n')[0]
                
                # 3. UI 테이블 입력 (파란색 영역 제외)
                # S1.py 로직: r in readonly_rows(파란색) 또는 c == 6(합계열, 파란색)은 입력 금지
                if i in readonly_rows:
                    continue # 소계/총계 행 전체 스킵

                for j in range(1, 6): # 1(판관비) ~ 5(이익잉여금)까지만 입력 (6번 합계열은 파란색이라 제외)

                    val = excel_item.split('\t')[j].strip().replace(',', '')
                    
                    # 엑셀의 빈 값 처리 및 입력
                    if val == "": val = "0"
                    self.s1.table.item(i, j).setText(val)

            except Exception as e:
                print(f"S1 입력 오류 [항목: {list_title[i].strip()}]: {e}")
                continue

        # 모든 입력 후 자동 계산 한 번 수행 (변경된 열 기준)
        for col_idx in range(1, 6):
            self.s1.calculate_s1(self.s1.table.item(0, col_idx))

        self.s1.table.blockSignals(False)
        self.s1.table.viewport().update()




        # s2 ############################################################################

        list_title = [
            '1.인센티브상여금을제외한인건비총액', 'a.판관비로처리한인건비', 'b.영업외비용으로처리한인건비', 'c.제조원가로처리한인건비', 
            'd.타계정대체로처리한인건비', 'e.이익잉여금의증감으로처리한인건비', '소계:(A)=a+b+c+d+e', 
            '2.총인건비인상률계산에서제외(조정)되는인건비', 'f.퇴직급여(명예퇴직금포함)', 'g.임원인건비', 'h.비상임이사인건비',
            '기타제외인건비', 'j.사내근로복지기금출연금', 'k.잡급및무기계약직에대한인건비(복리후생비포함,인센티브상여금제외)', 
            'l.공적보험사용자부담분', 'm.연월차수당등조정(㉠-㉡+㉢)', '연월차수당등발생액(㉠)',
            '연월차수당등지급액(㉡)', '종업원저리대여금이자관련인건비(㉢)', '무상대여이익', 'o.지방이전관련직접인건비', 
            'p.법령에따른특수건강진단비', 'q.코로나19대응을위한시간외근로수당등', 'r.해외근무수당', 's.직무발명보상금', 
            't.공무원수준내의자녀수당및출산격려금', 'v.비상진료체계운영에따른특별수당등',
            'u.국민건강보험공단2023년도총인건비초과액에따른상환금액', '소계:(B)=f+g+h+i+j+k+l+m-n+o+p+q+r+s+t+u+v+w', 
            '3.실집행액기준총인건비발생액(C)=(A)-(B)', '4.연도별증원소요인건비의영향을제거하기위한인건비의조정(D)',
            '5.별도직군승진시기차이에따른인건비효과조정(E)', '6.초임직급정원변동에따른인건비효과조정(F)', 
            '7.정년이후재고용을전제로전환된정원외인력의인건비효과조정(G)', '추가로지급된인건비의영향제거(H)', 
            '최저임금지급직원에대한인건비효과조정(I)', '10.파업등에따른인건비효과조정(J)', '11.코로나19로인한휴업의인건비효과조정(K)', 
            '(C)+(D)+(E)-(F)-(G)-(H)+(I)+(J)+(K)+(L)'
        ]

        excel = excel_original02
        self.s2.table.blockSignals(True) # self.table을 self.s2.table로 수정

        # 보호 구역 (39행 미만 중 데이터 입력을 건너뛸 행들)
        readonly_rows = [0, 6, 7, 15, 28, 29, 38] 
        yellow_rows = [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 30, 32]

        for i in range(0, 39):
            try:
                excel = excel.split(list_title[i])[1]
                excel_item = excel.split('\r\n')[0]
                
                if i == 11: excel_item = '\t' + excel_item   

                for j in range(2, 5): 
                    target_item = self.s2.table.item(i, j) # self.s2.table로 수정
                    
                    if not target_item or target_item.text() == "n/a": 
                        continue

                    if i in readonly_rows: 
                        continue

                    if i in yellow_rows and j == 2: 
                        continue

                    val = self.excel_str(excel_item.split('\t')[j], 2, i, j)
                    
                    try:
                        f_val = float(val.replace(',', ''))
                        target_item.setData(Qt.EditRole, f_val)
                    except:
                        target_item.setText(val)
            except:
                continue

        self.s2.table.blockSignals(False) # self.s2.table로 수정






        # s4 ############################################################################

        list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계', '1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계']
        
        excel = excel_original04
        self.s4.table.blockSignals(True)

        for i in range(0, 16):
            if i == 8:
                # 당년도 섹션으로 전환
                excel = excel_original04.split('당년도')[1]

            try:
                # 1. 직급명 체크 (3종 오류 알림 세트)
                try:
                    excel.split(list_title[i])[1]
                except:
                    err_loc = f"S4 엑셀 입력 오류: (3-2) [직급:{list_title[i]}] 데이터를 찾을 수 없음"
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write(err_loc + '\n')
                    print(err_loc)
                    QMessageBox.information(self, "S4 엑셀 입력 오류", err_loc)
                    continue

                # 2. 데이터 추출 (순차적 잘라내기)
                excel = excel.split(list_title[i])[1]
                excel_item = excel.split('\r\n')[0]

                # 3. UI 테이블 입력 (불필요 변수 없이 i와 j 인덱스로 직접 처리)
                if i < 8:   # 전년도 표
                    if i == 7: continue # '계' 제외
                    for j in range(1, 14): # 1월~12월 + 평균인원 (총 13개)
                        val = excel_item.split('\t')[j].strip().replace(',', '')
                        # i행, j+1열에 직접 입력
                        self.s4.table.item(i, j + 1).setText(val)

                else:       # 당년도 표
                    if i == 15: continue # '계' 제외
                    # rank_count=9 및 구분선 반영하여 i+2행에 직접 입력 [cite: 2025-12-24, 2025-12-20]
                    for j in range(1, 14):
                        val = excel_item.split('\t')[j].strip().replace(',', '')
                        self.s4.table.item(i + 2, j + 1).setText(val)

            except Exception as e:
                # 4. 예외 발생 시 상세 알림
                err_detail = f"S4 엑셀 입력 오류 [(3-2)직급별평균인원, 직급: {list_title[i]}]: {e}"
                with open("log.txt", "a", encoding="utf-8") as f:                    
                    f.write(err_detail + "\n")
                print(err_detail)
                QMessageBox.information(self, "S4 엑셀 입력 오류", err_detail)
                continue

        self.s4.table.blockSignals(False)
        self.s4.table.viewport().update()




        # s5 ############################################################################


        # S5 - (3-3) 가. 정원현원차이
        list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계', '1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계', ]
        
        # '나.근속승진' 이전 섹션인 '가.정원현원차이' 영역 추출
        excel_original05_05 = excel_original05.split('나.근속승진')[0]  
        excel = excel_original05_05

        self.s5.table.blockSignals(True)

        for i in range(0, 18):
            # 상단 표(1~6월)와 하단 표(7~12월) 섹션 전환
            if i == 8:
                continue # 빈 줄 혹은 구분선 스킵
            
            if i == 9:
                # 7~12월 데이터 섹션으로 전환
                excel = excel_original05_05.split('당년도')[2]
                continue

            try:
                # 1. 직급명 체크 (3종 오류 알림)
                try:
                    if i < 9: excel.split(list_title[i])[1]
                    else: excel.split(list_title[i-2])[1]
                except:
                    err_loc = f"S5 엑셀 입력 오류: (3-3) 가.정원현원차이 [직급:{list_title[i]}] 찾을 수 없음"
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write(err_loc + '\n')
                    print(err_loc)
                    QMessageBox.information(self, "S5 엑셀 입력 오류", err_loc)
                    continue


                
                # 3. UI 테이블 입력 (i < 9는 1~6월, i > 9는 7~12월)
                if i < 9:
                    excel = excel.split(list_title[i])[1]
                    excel_item = excel.split('\r\n')[0]
                    if i == 7: continue # '계' 행 제외
                    for j in range(1, 25): # 1월~6월 (정/현/복/누 4개씩 6개월 = 24개)
                        val = excel_item.split('\t')[j].strip().replace(',', '')
                        # i행, j+1열에 직접 입력
                        self.s5.table.item(i, j + 1).setText(val)
                else:
                    excel = excel.split(list_title[i-2])[1]
                    excel_item = excel.split('\r\n')[0]                    
                    if i == 17: continue # '계' 행 제외
                    for j in range(1, 25): # 7월~12월
                        val = excel_item.split('\t')[j].strip().replace(',', '')
                        # 7~12월 표 위치 보정 (i는 이미 9 이상이므로 시트 구조에 맞게 입력)
                        self.s5.table.item(i, j + 1).setText(val)

            except Exception as e:
                err_detail = f"S5 엑셀 입력 오류 [(3-3)가.정원현원차이, 직급: {list_title[i]}]: {e}"
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(err_detail + "\n")
                print(err_detail)
                QMessageBox.information(self, "S5 엑셀 입력 오류", err_detail)
                continue

        self.s5.table.blockSignals(False)
        self.s5.table.viewport().update()


        # s7 ############################################################################


        list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계', '1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계']

        # 상단 표 제외, 하단 '전년도' 섹션만 고정
        excel_original05_07 = excel_original05.split('다.증원소요인건비대상인원')[1]
        excel = excel_original05_07.split('전년도')[1]

        self.s7.table.blockSignals(True)

        # 8(전년도 1급)부터 14(전년도 연구직)까지 반복 (15번 '계' 자동 제외)
        for i in range(8, 15):
            try:
                try:
                    excel.split(list_title[i])[1]
                except:
                    err_loc = f"S7 엑셀 입력 오류: (3-3) 하단표 [직급:{list_title[i]}] 데이터를 찾을 수 없음"
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write(err_loc + '\n')
                    print(err_loc)
                    QMessageBox.information(self, "S7 엑셀 입력 오류", err_loc)
                    continue

                excel = excel.split(list_title[i])[1]
                excel_item = excel.split('\r\n')[0]
                
                # 하단 표 - 전년도 영역 데이터 입력
                for j in range(1, 14): 
                    val = excel_item.split('\t')[j].strip().replace(',', '')
                    # i+2, j+1 인덱스로 직접 입력 (rank_count=9 반영)
                    self.s7.table.item(i + 2, j + 1).setText(val)

            except Exception as e:
                err_detail = f"S7 엑셀 입력 오류 [(3-3)다.증원인원, 직급: {list_title[i]}]: {e}"
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(err_detail + "\n")
                print(err_detail)
                QMessageBox.information(self, "S7 엑셀 입력 오류", err_detail)
                continue

        self.s7.table.blockSignals(False)
        self.s7.table.viewport().update()












        # s8 ############################################################################


        list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계', '1급', '2급', '3급', '4급', '5급', '6급', '연구직', '계']

        # S8 데이터 영역 (excel_original06 사용)
        excel = excel_original06
        self.s8.table.blockSignals(True)

        for i in range(0, 16):
            if i == 8:
                # 당년도 섹션으로 전환
                excel = excel_original06.split('당년도')[1]

            try:
                # 1. 직급명 체크 (3종 오류 알림)
                try:
                    excel.split(list_title[i])[1]
                except:
                    err_loc = f"S8 엑셀 입력 오류: (3-4) [직급:{list_title[i]}] 데이터를 찾을 수 없음"
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write(err_loc + '\n')
                    print(err_loc)
                    QMessageBox.information(self, "S8 엑셀 입력 오류", err_loc)
                    continue

                # 2. 데이터 추출
                excel = excel.split(list_title[i])[1]
                excel_item = excel.split('\r\n')[0]

                # 3. UI 테이블 입력 (불필요 변수 및 수식 제외 로직 삭제)
                if i < 8:   # 전년도 표
                    if i == 7: continue 
                    for j in range(1, 13): # 1월~12월 (데이터 위치에 따라 j 범위 조정)
                        val = excel_item.split('\t')[j].strip().replace(',', '')
                        # i와 j+1(또는 컬럼 규격) 인덱스로 직접 입력
                        self.s8.table.item(i, j + 1).setText(val)

                else:       # 당년도 표
                    if i == 15: continue 
                    for j in range(1, 13):
                        val = excel_item.split('\t')[j].strip().replace(',', '')
                        # rank_count=9 반영하여 i+2 행에 직접 입력
                        self.s8.table.item(i + 2, j + 1).setText(val)

            except Exception as e:
                # 4. 예외 발생 시 3종 세트 알림 (S8 엑셀 입력 오류로 통일)
                err_detail = f"S8 엑셀 입력 오류 [(3-4)직급별평균단가, 직급: {list_title[i]}]: {e}"
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(err_detail + "\n")
                print(err_detail)
                QMessageBox.information(self, "S8 엑셀 입력 오류", err_detail)
                continue

        self.s8.table.blockSignals(False)
        self.s8.table.viewport().update()






        # s9 ############################################################################



        list_title = ['1급', '2급', '3급', '4급', '5급', '6급', '연구직', '기능직', '계', '1급', '2급', '3급', '4급', '5급', '6급', '연구직', '기능직', '계']

        # S9 핵심 데이터 영역 (excel_original07 사용 및 기존 필터 유지)
        excel_original07_09 = excel_original07.split('나.초임직급정원변동에따른인건비효과')[0]            
        excel = excel_original07_09

        self.s9.table.blockSignals(True)

        for i in range(0, 18):
            if i == 9:
                # 당년도 섹션으로 전환
                excel = excel_original07_09.split('전년도')[1]

            try:
                # 1. 직급명 체크 (3종 오류 알림 세트)
                try:
                    excel.split(list_title[i])[1]
                except:
                    err_loc = f"S9 엑셀 입력 오류: (3-6) [직급:{list_title[i]}] 데이터를 찾을 수 없음"
                    with open("log.txt", "a", encoding="utf-8") as f:
                        f.write(err_loc + '\n')
                    print(err_loc)
                    QMessageBox.information(self, "S9 엑셀 입력 오류", err_loc)
                    continue

                # 2. 데이터 추출 (순차적 자르기 유지)
                excel = excel.split(list_title[i])[1]
                excel_item = excel.split('\r\n')[0]

                # 3. UI 테이블 입력 (불필요 변수/로직 제거, 고정 인덱스 사용)
                if i < 9:   # 전년도 표
                    if i == 8: continue # '계' 제외
                    for j in range(1, 13): # 1월~12월 (j 인덱스 고정)
                        val = excel_item.split('\t')[j].strip().replace(',', '')
                        # i와 j+1 인덱스로 직접 입력
                        self.s9.table.item(i, j + 1).setText(val)

                else:       # 당년도 표
                    if i == 17: continue # '계' 제외
                    for j in range(1, 13):
                        val = excel_item.split('\t')[j].strip().replace(',', '')
                        # rank_count=9(기능직포함) 및 구분선 규격 반영 [cite: 2025-12-24, 2025-12-20]
                        self.s9.table.item(i + 2, j + 1).setText(val)

            except Exception as e:
                # 4. 예외 발생 시 상세 알림
                err_detail = f"S9 엑셀 입력 오류 [(3-6)초임직급정원, 직급: {list_title[i]}]: {e}"
                with open("log.txt", "a", encoding="utf-8") as f:                    
                    f.write(err_detail + "\n")
                print(err_detail)
                QMessageBox.information(self, "S9 엑셀 입력 오류", err_detail)
                continue

        self.s9.table.blockSignals(False)
        self.s9.table.viewport().update()


        # 각 페이지 계산   ############################################################################

        self.load_json('excel_input')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("맑은 고딕", 9))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
