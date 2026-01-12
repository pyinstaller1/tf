import sqlite3
import pandas as pd
import os
import mariadb
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os
import requests
import xml.etree.ElementTree as ET


import requests
import time




load_dotenv()

# MariaDB 연결
engine = create_engine( f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@127.0.0.1:3306/db_ls?charset=utf8mb4" )


base_dir = os.path.dirname(os.path.abspath(__file__))  # util/
db_path = os.path.abspath(os.path.join(base_dir, '..', 'stock.db'))

def get_ilbong_data(key: str):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()

        # 코드 판별
        if key.isdigit() and len(key) == 6:
            code = key
        else:
            cur.execute("SELECT 코드 FROM KOSPI_ALL WHERE 종목명 = ?", (key,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"종목명을 찾을 수 없습니다: {key}")
            code = row[0]

        # 일봉 데이터 조회
        query = f"""
        SELECT
            date,
            (SELECT 종목명 FROM KOSPI_ALL WHERE 코드 = ?) AS 종목명,
            open, high, low, close, volume,
            a5, a20, a60, a120,
            rsi, rsi9, ema26, macd, macd9,
            bol_u, bol_l, bol_size, bol_dolpa,
            ilmok_a, ilmok_b, ilmok_dolpa, ilmok_yang,
            개인, 외국인, 기관, 연기금
        FROM "{code}"
        """
        df = pd.read_sql_query(query, conn, params=(code,))
        return df




def insert_df_to_db(table, df):
    with sqlite3.connect(db_path) as conn:
        temp_table = f"{table}_temp"
        df.to_sql(temp_table, conn, if_exists="replace", index=True, index_label="date")

        cur = conn.cursor()

        # 기존 테이블 없으면 생성
        cur.execute(f'SELECT name FROM sqlite_master WHERE type="table" AND name="{table}"')
        if not cur.fetchone():
            df.head(0).to_sql(table, conn, if_exists="replace", index=True, index_label="date")
            cur.execute(f'CREATE UNIQUE INDEX IF NOT EXISTS idx_{table}_date ON "{table}" (date)')

        # 기존 테이블에서 TEMP에 없는 날짜만 가져와 TEMP에 추가
        col_names = list(df.columns)
        col_str = ", ".join(col_names)
        cur.execute(f'''
            INSERT INTO "{temp_table}" (date, {col_str})
            SELECT date, {col_str} FROM "{table}"
            WHERE date NOT IN (SELECT date FROM "{temp_table}")
        ''')


        # 기존 테이블 전체 삭제
        cur.execute(f'DELETE FROM "{table}"')

        # TEMP 데이터를 다시 원본 테이블에 삽입
        cur.execute(f'''
            INSERT INTO "{table}" (date, {col_str})
            SELECT date, {col_str} FROM "{temp_table}"
        ''')

        # TEMP 삭제
        cur.execute(f'DROP TABLE IF EXISTS "{temp_table}"')
        conn.commit()



def get_kospi_codes():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 코드 FROM KOSPI")
        codes = [row[0] for row in cursor.fetchall()]
        return codes

        

def get_kospi300_code():
    
    with sqlite3.connect(db_path) as conn:
        df_db = pd.read_sql("SELECT 코드, 종목명, 현재가, 등락률, 시가총액, 시장, 순위 FROM KOSPI", conn)  # 쿼리 결과를 DataFrame에 저장
    # dict_kospi = dict(zip(df_db['코드'], df_db['종목명']))
    return df_db





























def create_tb_ilbong():
    with engine.connect() as conn:

        # 기존 테이블 존재 여부 확인 (로직 동일)
        result = conn.execute(
            text("SELECT COUNT(*) FROM information_schema.tables "
                 "WHERE table_schema = DATABASE() AND table_name = 'tb_ilbong'")
        ).scalar()

        if result:
            conn.execute(text("DROP TABLE tb_ilbong"))
            print("⚠ 기존 tb_ilbong 테이블 삭제됨")

        # 테이블 생성 (새로운 컬럼 추가됨)
        sql_create = """
        CREATE TABLE tb_ilbong (
            code CHAR(6) NOT NULL,
            date CHAR(8) NOT NULL,

            -- 1. 일봉 (OHLCV)
            open INT,
            high INT,
            low INT,
            close INT,
            volume BIGINT,

            -- 2. 이동평균선 (get_ilbong 함수에서 계산)
            ma5 FLOAT,
            ma20 FLOAT,
            ma60 FLOAT,
            ma120 FLOAT,
            
            -- 3. calculate_all_indicators 함수의 지표 (기존 컬럼들)
            rsi14 FLOAT,
            macd FLOAT,
            macd9 FLOAT,
            bol_u FLOAT,
            bol_l FLOAT,
            bol_size VARCHAR(10),
            bol_dolpa VARCHAR(10),

            ilmok_a FLOAT,
            ilmok_b FLOAT,
            ilmok_dolpa VARCHAR(10),
            ilmok_yang VARCHAR(5),
            
            -- 4. 수급 및 공매도/프로그램 데이터 (추가된 컬럼들)
            개인 FLOAT,
            외국인 FLOAT,
            기관 FLOAT,
            연기금 FLOAT,
            사모펀드 FLOAT,
            
            프로그램 FLOAT,
            공매도수량 FLOAT,
            공매도대금 FLOAT,

            PRIMARY KEY (code, date),
            KEY idx_code (code),
            KEY idx_date (date)
        ) ENGINE=InnoDB
        DEFAULT CHARSET=utf8mb4
        COMMENT='주식 일봉 (수급, 공매도, 프로그램, 각종 지표 포함)';
        """

        conn.execute(text(sql_create))
        # print("✅ tb_ilbong 테이블 생성 완료 (수급/공매도 컬럼 추가)")


        


def insert_tb_ilbong(code, ilbong):
    with engine.connect() as conn:
        # SQL 쿼리 수정: 새로운 컬럼들을 REPLACE INTO 문에 추가
        sql = """
        REPLACE INTO tb_ilbong 
        (code, date, open, high, low, close, volume, ma5, ma20, ma60, ma120, rsi14,
         macd, macd9, bol_u, bol_l, bol_size, bol_dolpa,
         ilmok_a, ilmok_b, ilmok_dolpa, ilmok_yang,
         
         -- 새로 추가된 수급 및 프로그램/공매도 컬럼들
         개인, 외국인, 기관, 연기금, 사모펀드,
         프로그램, 공매도수량, 공매도대금) 
        
        VALUES (:code, :date, :open, :high, :low, :close, :volume, :ma5, :ma20,
                :ma60, :ma120, :rsi14, :macd, :macd9, :bol_u, :bol_l, :bol_size, :bol_dolpa,
                :ilmok_a, :ilmok_b, :ilmok_dolpa, :ilmok_yang,
                
                -- 새로 추가된 파라미터들
                :개인, :외국인, :기관, :연기금, :사모펀드,
                :프로그램, :공매도수량, :공매도대금)
        """

        insert_data = []
        for row in ilbong:
            insert_data.append({
                'code': code,
                'date': row['date'],
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row.get('volume', 0),
                
                # 이동평균선 (get_ilbong에서 계산)
                'ma5': row.get('ma5'),
                'ma20': row.get('ma20'),
                'ma60': row.get('ma60'),
                'ma120': row.get('ma120'),
                
                # 지표 (calculate_all_indicators에서 채워질 예정)
                'rsi14': row.get('rsi14'),
                'macd': row.get('macd'),
                'macd9': row.get('macd9'),
                'bol_u': row.get('bol_u'),
                'bol_l': row.get('bol_l'),
                'bol_size': row.get('bol_size'),
                'bol_dolpa': row.get('bol_dolpa'),

                'ilmok_a': row.get('ilmok_a'),
                'ilmok_b': row.get('ilmok_b'),
                'ilmok_dolpa': row.get('ilmok_dolpa'),
                'ilmok_yang': row.get('ilmok_yang'),
                
                # 수급 및 공매도/프로그램 데이터 (get_ilbong에서 가져옴)
                '개인': row.get('개인'),
                '외국인': row.get('외국인'),
                '기관': row.get('기관'),
                '연기금': row.get('연기금'),
                '사모펀드': row.get('사모펀드'),
                
                '프로그램': row.get('프로그램'),
                '공매도수량': row.get('공매도수량'),
                '공매도대금': row.get('공매도대금'),

            })

        # 데이터베이스 실행
        conn.execute(text(sql), insert_data)
        conn.commit()
        # print(f"✅ 총 {len(insert_data)}개 데이터 `{code}` 저장/업데이트 완료 (수급/공매도 포함)")



















    

def create_tb_kospi(df, option="replace"):

    # 컬럼명 정리
    if 'index' in df.columns:
        df = df.rename(columns={'index': 'date'})

    # SQLAlchemy 엔진
    engine = create_engine(
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        "@127.0.0.1:3306/db_ls?charset=utf8mb4"
    )

    # 테이블 생성 + 데이터 insert
    df.to_sql(
        name="tb_kospi",
        con=engine,
        if_exists=option,
        index=False,
        chunksize=1000,
        method="multi"
    )

    engine.dispose()

    return





def select_tb_kospi(code=None):
    with engine.connect() as conn:
        if code:
            query = text("""SELECT 코드, 종목명, 현재가, 등락률, 시가총액, 매출, 영업이익, 배당금, 외국인, PER, concat(replace(replace(시장, '코스피', ''), '코스닥', 'Q'), 순위) as 순위, '' as 섹터,
(SELECT ROUND(rsi14, 0) FROM tb_ilbong WHERE code = tb_kospi.코드 ORDER BY date DESC LIMIT 1) as rsi FROM tb_kospi WHERE 코드 = :code""")
            result = conn.execute(query, {"code": code})
        else:
            query = text("""SELECT 코드, 종목명, 현재가, 등락률, 시가총액, 매출, 영업이익, 배당금, 외국인, PER, concat(replace(replace(시장, '코스피', ''), '코스닥', 'Q'), 순위) as 순위, '' as 섹터,
(SELECT ROUND(rsi14, 0) FROM tb_ilbong WHERE code = tb_kospi.코드 ORDER BY date DESC LIMIT 1) as rsi FROM tb_kospi""")
            result = conn.execute(query)            
    return [tuple(row) for row in result.fetchall()]




def select_tb_basic(code=None):
    with engine.connect() as conn:
        if code:
            query = text("SELECT * FROM tb_basic WHERE 코드 = :code")
            result = conn.execute(query, {"code": code})
        else:
            query = text("SELECT * FROM tb_basic")
            result = conn.execute(query)
        
    return [tuple(row) for row in result.fetchall()]
    

def create_tb_basic():
    with engine.connect() as conn:
        # 테이블 삭제
        conn.execute(text("DROP TABLE IF EXISTS tb_basic"))

        # 테이블 생성
        sql_create = '''
        CREATE TABLE IF NOT EXISTS tb_basic (
            코드 VARCHAR(20) PRIMARY KEY,
            종목명 VARCHAR(100),
            corp_code VARCHAR(20),
            섹터 VARCHAR(50),
            매출202201 BIGINT, 영업이익202201 BIGINT, 매출202202 BIGINT, 영업이익202202 BIGINT, 매출202203 BIGINT, 영업이익202203 BIGINT, 매출202204 BIGINT, 영업이익202204 BIGINT,
            매출202301 BIGINT, 영업이익202301 BIGINT, 매출202302 BIGINT, 영업이익202302 BIGINT, 매출202303 BIGINT, 영업이익202303 BIGINT, 매출202304 BIGINT, 영업이익202304 BIGINT,
            매출202401 BIGINT, 영업이익202401 BIGINT, 매출202402 BIGINT, 영업이익202402 BIGINT, 매출202403 BIGINT, 영업이익202403 BIGINT, 매출202404 BIGINT, 영업이익202404 BIGINT,
            매출202501 BIGINT, 영업이익202501 BIGINT, 매출202502 BIGINT, 영업이익202502 BIGINT, 매출202503 BIGINT, 영업이익202503 BIGINT, 매출202504 BIGINT, 영업이익202504 BIGINT,
            매출202601 BIGINT, 영업이익202601 BIGINT, 매출202602 BIGINT, 영업이익202602 BIGINT, 매출202603 BIGINT, 영업이익202603 BIGINT, 매출202604 BIGINT, 영업이익202604 BIGINT
        );
        '''
        conn.execute(text(sql_create))

        # KOSPI 데이터 삽입 (이미 tb_kospi 테이블이 있다고 가정)
        conn.execute(text('''
        INSERT INTO tb_basic (코드, 종목명)
        SELECT 코드, 종목명 FROM tb_kospi
        '''))

        # XML -> corp_code 매핑
        xml_path = os.path.join(base_dir, "CORPCODE.xml")
        tree = ET.parse(xml_path)
        root = tree.getroot()
        mapping = {item.find("stock_code").text.strip(): item.find("corp_code").text.strip()
                   for item in root.findall("list") if item.find("stock_code") is not None}

        for stock_code, corp_code in mapping.items():
            conn.execute(
                text("UPDATE tb_basic SET corp_code = :corp WHERE 코드 = :code"),
                {"corp": corp_code, "code": stock_code}
            )


        # DART API 분기 실적 업데이트 (기존 로직 그대로)
        API_KEY = "c2bc2e5748c3279f4b75fd9508b4e8e8145ada4b"
        REPRT_MAP = {1: "11013", 2: "11012", 3: "11014", 4: "11011"}

        def fetch_dart_quarter(corp_code, year, quarter):
            url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
            params = {"crtfc_key": API_KEY, "corp_code": corp_code, "bsns_year": str(year), "reprt_code": REPRT_MAP[quarter]}
            r = requests.get(url, params=params).json()
            if r.get("status") != "000":
                return None, None
            sales, op = None, None
            for item in r.get("list", []):
                val = item.get("thstrm_amount", "0").replace(",", "")
                v = int(val) if val and val != '-' else 0
                if item.get("account_nm") == "매출액":
                    sales = v
                elif item.get("account_nm") == "영업이익":
                    op = v
            return sales, op

        rows = conn.execute(text("SELECT 코드, corp_code FROM tb_basic")).fetchall()

        cnt = 0
        for stock_code, corp_code in rows:
            cnt += 1
            if cnt >= 1:
                print(str(cnt) + '\t' + stock_code + '\t' + time.strftime("%H:%M", time.localtime()))
                if not corp_code:
                    continue
                update_dict = {}
                for year in range(2022, 2027):
                    for q in range(1, 5):
                        sales, op = fetch_dart_quarter(corp_code, year, q)
                        update_dict[f"매출{year}{q:02d}"] = sales
                        update_dict[f"영업이익{year}{q:02d}"] = op
                set_clause = ", ".join([f"{k}=:{k}" for k in update_dict.keys()])
                params = update_dict.copy()
                params["code"] = stock_code
                conn.execute(text(f"UPDATE tb_basic SET {set_clause} WHERE 코드 = :code"), params)

                conn.commit()

    print("[ALL DONE] tb_basic 생성 및 분기 실적 업데이트 완료")












































































def delete_db_1day(code, date): # DB 최근일 삭제
    with sqlite3.connect(db_path) as conn:
        conn.execute(f"""DELETE FROM '{code}' WHERE DATE = '{date}'""")
        conn.commit()

def delete_db_days(code, date1, date2): # DB 최근일 삭제
    with sqlite3.connect(db_path) as con:
        con.execute(f"""DELETE FROM '{code}' WHERE DATE BETWEEN '{date1}' AND '{date2}'""")
        con.commit()

def drop_db(code):
    with sqlite3.connect(db_path) as con:
        con.execute(f"""DROP TABLE '{code}'""")
        con.commit()














