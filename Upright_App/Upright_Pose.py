from random import random
import turtle
import cv2 as cv
import math
import time
import mediapipe as mp
import numpy as np
from tkinter import messagebox
import os
import User
import Upright_DB
import tensorflow.keras
#import User_alarm
from scipy.spatial import distance as dist
from imutils import face_utils
import pygame 
import time
import User_alarm
from random import *


start = time.time()  # 시작 시간 저장

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

sensitivity_F=1       # fine 민감도
sensitivity_T=1       # turtle 민감도

#os.environ["CUDA_VISIBLE_DEVICES"] = "0"
classes = ['fine', 'turtle']
model = tensorflow.keras.models.load_model('keras_model.h5')

# For static images:
IMAGE_FILES = []
size = (224, 224)
BG_COLOR = (192, 192, 192) # gray
ear = 0

def Save_Cam():
    now = time.localtime()
    name = str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+str("_") + \
        str(now.tm_hour)+str("_")+str(now.tm_min)+str("_")+str(now.tm_sec)
    return name

# # For webcam input--------------------------------------------------------------------------
def camStart():
    now = time.localtime()
    Upright_DB.Init_habit()
    cap = cv.VideoCapture(0)
    while_Counter1=0
    while_Counter2=0
    turtle_Count=0
    turtle_check=0
    turtle_Count2=0
    while_counter_turtle=0
# face, body------------------------------------------------------------------------------------------
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh,\
        mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5
            ) as pose:
        count=0
        chk=0
        while cap.isOpened():
            textcheck=0
            # turtle ----------------------------------------------------------------------------------
            success, image = cap.read()
            image = cv.flip(image,1)
            if not success:
                break
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            results_face = face_mesh.process(image)
            results_P = pose.process(image)   # body
            while_counter_turtle+=1
            # face, pose 좌표 그리기
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

            if results_face.multi_face_landmarks:
                for face_landmarks in results_face.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=None,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_contours_style())
                        
            if results_P.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results_P.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=None)
            # Flip the image horizontally for a selfie-view display.
            suby = abs(face_landmarks.landmark[374].y-face_landmarks.landmark[386].y)
            print(suby)
            if suby<0.013:
                if chk==0:
                    count+=1
                    chk=1
            if suby>0.015:
                chk=0
            image = cv.flip(image,1)
            if while_Counter2>200:
                if count<15:
                    if(User.user.alarm=="on"):
                        pygame.mixer.init() 
                        pygame.mixer.music.load('mp3\눈을 깜빡이세요.mp3')
                        pygame.mixer.music.play()
                        User_alarm.alarm("눈을 깜빡여 주세요.")
                        messagebox.showinfo("경고", "눈을 깜빡여주세요")
                        print(time.time()-start)
                        Upright_DB.Count_habit("eye", time.time()-start)
                    count=0
                    while_Counter2=0
                else:
                    count=0
                    while_Counter2=0
            while_Counter1+=1
            while_Counter2+=1

           

            image = cv.flip(image, 1)

            img_input = cv.resize(image, size)
            img_input = (img_input.astype(np.float32) / 127.0) - 1
            img_input = np.expand_dims(img_input, axis=0)

            predict = model.predict(img_input)[0]
            prediction_F = predict[0]*sensitivity_F
            prediction_T = predict[1]*sensitivity_T
            idx = np.argmax(np.array([prediction_F, prediction_T]))

            cv.putText(image, f"Blinks: {count}", (10, 30),
                    cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            try:
                pose_x=abs((results_P.pose_landmarks.landmark[12].x+results_P.pose_landmarks.landmark[11].x)/2)
                pose_y=abs((results_P.pose_landmarks.landmark[12].y+results_P.pose_landmarks.landmark[11].y)/2)
                length_turtle=math.sqrt((results_P.pose_landmarks.landmark[0].x-pose_x)**2+(results_P.pose_landmarks.landmark[0].y-pose_y)**2)
            except Exception as e:
                continue
            
            if while_counter_turtle==1:
                turtle_check+=length_turtle
            elif while_counter_turtle<20:
                turtle_check+=length_turtle
                turtle_check/=2
                print(length_turtle)
            else:
                if length_turtle<turtle_check*0.96*sensitivity_T and length_turtle>turtle_check*0.96*sensitivity_T*0.95:
                    turtle_Count2+=1
                    print(turtle_Count2)
                    print("chk")
                    if turtle_Count2>=31:
                        if(User.user.alarm=="on"):
                            pygame.mixer.init() 
                            if(randint(0, 1)==0):
                                pygame.mixer.music.load(os.getcwd()+r'/mp3/거북목입니다.mp3')
                            else:
                                pygame.mixer.music.load(os.getcwd()+r'/mp3/자세를 바르게하세요.mp3')
                            pygame.mixer.music.play()
                            User_alarm.alarm("거북목 입니다. 자세를 바르게 하세요!!")
                            messagebox.showinfo("경고", "거북목입니다!")
                            Upright_DB.Count_habit("turtle", time.time()-start)
                            path = "C:/imgfile/" + str("habit_") + Save_Cam() + ".png"
                            cv.imwrite(path, image)
                            Upright_DB.insertBLOB(path)
                            turtle_Count2=0
                            textcheck=1
                else:
                    turtle_Count2=0

            if idx==1:
                turtle_Count+=1
                if turtle_Count>=31:
                    if(User.user.alarm=="on"):
                        pygame.mixer.init() 
                        if(randint(0, 1)==0):
                            pygame.mixer.music.load('mp3\거북목입니다.mp3')
                        else:
                            pygame.mixer.music.load('mp3\자세를 바르게하세요.mp3')
                        pygame.mixer.music.play()
                        User_alarm.alarm("거북목 입니다. 자세를 바르게 하세요!!")
                        messagebox.showinfo("경고", "거북목입니다!")

                        Upright_DB.Count_habit("turtle", time.time()-start)
                        path = "C:/imgfile/" + str("habit_") + Save_Cam() + ".png"
                        cv.imwrite(path, image)
                        Upright_DB.insertBLOB(path)
                        textcheck=1

                        

                    turtle_Count=0
            else: turtle_Count=0

            cv.putText(image, f"Blinks: {count}", (10, 30),
                    cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if(User.user.alarm=="on"):
                cv.putText(image, "alarm: on", org=(400, 30),
                fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 0, 255), thickness=2)    
            if(User.user.alarm=="off"):
                cv.putText(image, "alarm: off", org=(400, 30),
                fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 255, 255), thickness=2)

            if(idx==0):
                cv.putText(image, text=classes[idx], org=(10, 60),
                fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 0, 255), thickness=2)    
            if(idx==1):
                cv.putText(image, text=classes[idx], org=(10, 60),
                fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 255, 255), thickness=2)
    # ------------------------------------------------------------------------------------------
            cv.imshow('Pose', image)
            if cv.waitKey(1) & 0xFF == 27:
                break
            if cv.getWindowProperty("Pose", cv.WND_PROP_VISIBLE) <1:  # X버튼을 누르면 창 닫기 -> 창이 닫혔는지 감지하면 종료, 다시 실행되는 것을 방지
                break
    cap.release()