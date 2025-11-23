
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import joblib
import warnings
warnings.filterwarnings('ignore') # 경고 메시지 무시







def run():

    data = np.array([
        [5, 50, 30, 50, 80, 30, 20, 5, 8 , 7],    # 1월
        [3, 100, 30, 50, 80, 30, 20, 5, 8 , 7],   # 2월
        [8, 150, 30, 50, 80, 30, 20, 5, 8 , 7],   # 3월
        [6, 130, 30, 50, 80, 30, 20, 5, 8 , 7],   # 4월
        [10, 180, 30, 50, 80, 30, 20, 5, 8 , 7],  # 5월
        [7, 160, 30, 50, 80, 30, 20, 5, 8 , 7]    # 6월
    ])

    look_back = 3   # 시계열 기간 3개월로 3음달 예측
    epochs_count = 100 # 학습 횟수


    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data) # 데이터 스케일링 (0~1로 정규화)

    '''
    [[0.28571429 0.        ]
     [0.         0.38461538]
     [0.71428571 0.76923077]
     [0.42857143 0.61538462]
     [1.         1.        ]
     [0.57142857 0.84615385]]
    '''


    X, Y = [], []    
    for i in range(len(scaled_data) - look_back):
        a = scaled_data[i:(i + look_back), :]
        X.append(a)
        Y.append(scaled_data[i + look_back, :])

    X = np.array(X)
    Y = np.array(Y)


    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(look_back, X.shape[2])))   # 입력층 3개월 입력 (AB 2노드), 은닉층 1층 (50노드)
    model.add(Dense(10)) # 출력층은 예측값 (AB 2노드)
    model.compile(optimizer='adam', loss='mse')   # MSE(Mean Squared Error) → 오차를 제곱해서 평균



    print(f"모델 학습 시작 (Epochs: {epochs_count})...")
    model.fit(X, Y, epochs=epochs_count, batch_size=1, verbose=0)  # 모델학습, 에포크3
    print("모델 학습 완료!\n")










    # model.save("lstm_model.keras")   # 모델 저장
    # joblib.dump(scaler, "scaler.save")

    print("--- 다음 달 예측 ---")

    #####
    '''    
    model = load_model("lstm_model.keras")   # 모델 로드
    scaler = joblib.load("scaler.save")
    
    
    last_3_months = np.array([
        [6, 130, 30, 50, 80, 30, 20, 5, 8 , 7],   # 4월
        [10, 180, 30, 50, 80, 30, 20, 5, 8 , 7],  # 5월
        [7, 160, 30, 50, 80, 30, 20, 5, 8 , 7]    # 6월
    ])
    look_back = 3
    last_3_months = scaler.transform(last_3_months)
    '''
    #####
    
    last_3_months = scaled_data[-look_back:]   # 예측 입력값 (4,5,6월)













    

    input_scaled = last_3_months.reshape(1, look_back, last_3_months.shape[1]) # list (3, 2) => (1, 3, 2)

    predicted_scaled = model.predict(input_scaled, verbose=0)   # 예측 수행
    predicted_original = scaler.inverse_transform(predicted_scaled)   # scaled => 숫자

    predicted_A = round(predicted_original[0, 0])
    predicted_B = round(predicted_original[0, 1])
    print(round(predicted_original[0, 2]))
    print(round(predicted_original[0, 3]))
    print(round(predicted_original[0, 4]))
    print(round(predicted_original[0, 5]))
    print(round(predicted_original[0, 6]))
    print(round(predicted_original[0, 7]))
    print(round(predicted_original[0, 8]))
    print(round(predicted_original[0, 9]))


    print(f"입력 데이터 (4, 5, 6월):")
    print(f"A: {last_3_months[-3:, 0]}, B: {last_3_months[-3:, 1]}")
    print("\n" + "=" * 40)
    print(f"**➡️ 다음 달 (7개월차) 오류 건수 예측 결과:**")
    print(f"** A 예측값: {predicted_A} 건**")
    print(f"** B 예측값: {predicted_B} 건**")
    print("=" * 40)












run()




