import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
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




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4개 공통지표 점수로 인건비 집계")        
        self.setGeometry(150, 150, 1100, 850)
        self.setStyleSheet("background-color: white;") 
        
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)

        # 1. 상단 버튼바 (간격 최소화: spacing=2)
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(2) # 버튼 사이 간격을 2픽셀로 고정
        


        # 엑셀 버튼
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
        # 각 번호에 맞는 시트 클래스를 연결
        for i in range(1, 19):
            if i == 2:
                page = Sheet2Page()
            elif i == 3:
                page = Sheet3Page()
            elif i == 4:
                page = Sheet4Page()
            elif i == 5:
                page = Sheet5Page()                
            elif i == 6:
                page = Sheet6Page()                
            elif i == 7:
                page = Sheet7Page()
            elif i == 8:
                page = Sheet8Page()
            elif i == 9:
                page = Sheet9Page()
            elif i == 10:
                page = Sheet10Page()                  
            elif i == 11:
                page = Sheet11Page()
            elif i == 12:
                page = Sheet12Page()                
            elif i == 13:
                page = Sheet13Page()           
            elif i == 14:
                page = Sheet14Page()                                            
            elif i == 15:
                page = Sheet15Page()
            elif i == 16:
                page = Sheet16Page()
            elif i == 17:
                page = Sheet17Page()
            elif i == 18:
                page = Sheet18Page()                  
            else:
                page = QWidget() # 나머지는 아직 빈 페이지
                
            self.tabs.addTab(page, f"Sheet{i}")

        self.tabs.setCurrentIndex(1)
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






    def save_json(self, is_save_as=False):
        import json, os
        
        if is_save_as or not hasattr(self, 'current_path') or not self.current_path:
            default_name = os.path.join(os.getcwd(), "budget_data.json")
            path, _ = QFileDialog.getSaveFileName(self, "데이터 저장", default_name, "JSON Files (*.json);;Text Files (*.txt)")
            if not path: return
            self.current_path = path
        else:
            path = self.current_path

        total_data = {}
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
            
            self.setWindowTitle(f"예산 관리 프로그램 - {os.path.basename(path)}")
            QMessageBox.information(self, "완료", "데이터가 안전하게 저장되었습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"저장 실패: {e}")




    def load_json(self):
        import json, os
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        from PyQt5.QtCore import Qt

        path, _ = QFileDialog.getOpenFileName(self, "데이터 불러오기", os.getcwd(), "JSON Files (*.json)")
        if not path: return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                total_data = json.load(f)

            for i in range(self.tabs.count()):
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
                            if item and (item.flags() & Qt.ItemIsEditable):
                                item.setText(str(val))
                    table.blockSignals(False)

                    # 2. 시트별 계산 함수 탐색
                    calc_func = None
                    for attr in dir(page):
                        if "calculate" in attr.lower():
                            calc_func = getattr(page, attr)
                            break
                    
                    if calc_func:
                        # 4번 시트(Sheet4Page) 전용 집중 케어
                        if "4" in sheet_name or i == 3: 
                            # 전년도(0~7행)와 당년도(11~17행)의 데이터를 모두 깨움
                            active_rows = list(range(0, 8)) + list(range(11, 18))
                            for r in active_rows:
                                # 2열(1월)부터 13열(12월)까지 값을 확인하며 신호를 보냄
                                for c in range(2, 14):
                                    trigger_item = table.item(r, c)
                                    if trigger_item and trigger_item.text() != "":
                                        # 직접 함수 호출로 가로 평균과 세로 합계를 동시에 유도
                                        try:
                                            calc_func(trigger_item)
                                        except: pass
                                        # 한 행에 한 번만 신호를 보내도 가로 평균은 계산되므로 
                                        # 성능을 위해 각 행의 첫 번째 유효 데이터에서 break 할 수 있음
                                        break
                        else:
                            # 2, 3, 15번 등 나머지 시트들은 기존 방식대로 행 단위 트리거
                            for r in range(table.rowCount()):
                                trigger_item = table.item(r, 2)
                                if trigger_item:
                                    try:
                                        calc_func(trigger_item)
                                        table.itemChanged.emit(trigger_item)
                                    except: continue

            self.current_path = path
            self.setWindowTitle(f"예산 관리 프로그램 - {os.path.basename(path)}")
            QMessageBox.information(self, "성공", "4번 시트 포함 18개 시트 연산 완료")

        except Exception as e:
            QMessageBox.critical(self, "오류", f"불러오기 실패: {e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("맑은 고딕", 9))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
