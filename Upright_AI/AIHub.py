import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.utils import plot_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dropout, Dense, LSTM, BatchNormalization, Flatten, MaxPooling2D

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
folders = os.listdir(r'image(test)')
print(folders)

categories = []
images = []

#label 처리
for folder in folders:
    files = os.listdir(r'image(test)/'+folder)
    for file in files:
        categorie = file.split('.')[0]
        if categorie == 'turtle':
            categorie = 1
        else :
            categorie = 0

        categories.append(categorie)

        #이미지 처리
        image = keras.preprocessing.image.load_img(r'image(test)/'+folder+r'/'+file, target_size=(224,224))
        imageArr = np.array(image)
        images.append(imageArr)

categories = np.array(categories)
images = np.array(images)
print(images.shape)

trainX, testX, trainY, testY = train_test_split(images, categories, shuffle=True, test_size=0.2,stratify=categories)
print(trainX.shape, trainY.shape, testX.shape, testY.shape)

#학습 모델 생성
model = keras.Sequential()
#2개의 히든 레이블
model.add(keras.layers.Flatten())
model.add(keras.layers.InputLayer(input_shape=(224*224*3)))
model.add(keras.layers.Dense(32,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(keras.layers.Dense(64,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.25))
model.add(keras.layers.Dense(128,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(keras.layers.Dense(512,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Flatten())
model.add(keras.layers.Dense(256,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(keras.layers.Dense(2,activation='sigmoid'))

#오버피팅 방지
callbacks = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)
mc = keras.callbacks.ModelCheckpoint(r'abcd/best_model.h5', monitor='val_loss', mode='min', save_best_only=True)

#모델 학습 방법 정의 
model.compile(optimizer=Adam(learning_rate=0.0001),loss='sparse_categorical_crossentropy',metrics=['accuracy'])
#모델 학습
history=model.fit(trainX, trainY, epochs=30, batch_size=8, validation_split=0.2)
# , callbacks=[callbacks, mc]

plt.figure(figsize=(12, 4))                                                     #그래프의 가로세로 비율
plt.subplot(1, 1, 1)                                                            #1행 1열의 첫번째 위치
plt.plot(history.history['loss'], 'b--', label = 'loss')                        #loss는 파란색 점선
plt.plot(history.history['accuracy'], 'g-', label = 'Accuracy')                 #accuracy는 녹색실선
plt.xlabel('Epoch')
plt.legend()
plt.show()
print("최적화 완료!")

print("\n================test results=================")
labels=model.predict(testX)
print("\n Accuracy: %.4f" % (model.evaluate(trainX, trainY)[1]))
print("=============================")

# h5 모델 저장
model.save('keras_model.h5')