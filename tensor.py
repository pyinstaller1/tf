import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore') # 경고 메시지 무시

# --- 1. 데이터 정의 및 설정 ---
print("--- 1. 데이터 정의 및 설정 ---")

# 6개월치 가상 데이터 (월별)
# A = 오류 건수 A, B = 오류 건수 B
data = np.array([
    [5, 50],    # 1월
    [3, 100],   # 2월
    [8, 150],   # 3월
    [6, 130],   # 4월
    [10, 180],  # 5월
    [7, 160]    # 6월
])

# 시계열 기간 설정 (이전 3개월 데이터로 다음 1개월 예측)
look_back = 3
epochs_count = 100 # 학습 횟수

# --- 2. 데이터 전처리 및 데이터셋 생성 ---
print("--- 2. 데이터 전처리 ---")

# 1) 데이터 스케일링 (정규화)
# 데이터를 0과 1 사이로 변환하여 모델 학습 효율을 높입니다.
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# 2) 시계열 데이터셋 생성 함수
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back):
        # i부터 look_back 기간까지의 데이터를 입력(X)으로 설정
        a = dataset[i:(i + look_back), :]
        X.append(a)
        # look_back 기간 다음의 데이터를 출력(Y)으로 설정
        Y.append(dataset[i + look_back, :])
    return np.array(X), np.array(Y)

# 데이터셋 생성 및 형태 변환 (LSTM 입력 형태: [샘플 수, 시간 단계, 특성 수])
X, Y = create_dataset(scaled_data, look_back)

# 현재 훈련 샘플 확인 (6개월 데이터에서 look_back=3 이면 3개의 샘플이 생성됨)
print(f"훈련 데이터 샘플 수: {X.shape[0]}개")
print(f"LSTM 입력 형태 (X): {X.shape}") 
print(f"LSTM 출력 형태 (Y): {Y.shape}")
print("\n" + "-"*30)

# --- 3. LSTM 모델 구성 및 학습 ---
print("--- 3. LSTM 모델 구성 및 학습 ---")

# 모델 구성
model = Sequential()
# LSTM 레이어: 50개의 뉴런, 입력 형태는 (look_back=3, 특성수=2)
model.add(LSTM(50, activation='relu', input_shape=(look_back, X.shape[2])))
# 출력 레이어: A와 B 2개의 예측값 (다음 달 A와 B 건수)
model.add(Dense(2))
model.compile(optimizer='adam', loss='mse')

# 모델 학습
print(f"모델 학습 시작 (Epochs: {epochs_count})...")
model.fit(X, Y, epochs=epochs_count, batch_size=1, verbose=0) 
print("모델 학습 완료!")
print("\n" + "-"*30)

# --- 4. 다음 달 (7개월차) 예측 ---
print("--- 4. 다음 달 (7개월차) 예측 ---")

# 마지막 3개월 데이터 (4월, 5월, 6월) 추출
last_3_months = scaled_data[-look_back:]

# 예측을 위한 입력 형태 변환: [1, look_back, 특성 수]
input_for_predict = last_3_months.reshape(1, look_back, X.shape[2])

# 예측 수행 (스케일링된 값)
predicted_scaled = model.predict(input_for_predict, verbose=0)

# 예측 결과 역변환 (원래의 오류 건수 값으로 복원)
# scaler.inverse_transform(predicted_scaled)를 사용하여 원래 스케일로 되돌립니다.
predicted_original = scaler.inverse_transform(predicted_scaled)

# 결과 출력
predicted_A = round(predicted_original[0, 0])
predicted_B = round(predicted_original[0, 1])

print(f"입력 데이터 (4, 5, 6월):")
print(f"A: {data[-3:, 0]}, B: {data[-3:, 1]}")
print("\n" + "=" * 40)
print(f"**➡️ 다음 달 (7개월차) 오류 건수 예측 결과:**")
print(f"** A 예측값: {predicted_A} 건**")
print(f"** B 예측값: {predicted_B} 건**")
print("=" * 40)
