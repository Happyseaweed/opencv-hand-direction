import cv2 as cv
import mediapipe as mp
import pygame
import numpy as np
import math
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_faceMesh = mp.solutions.face_mesh

capture = cv.VideoCapture(0)

def avg_point(landmarks):
    avg_x = 0
    avg_y = 0

    for i in range(0, 21):
        avg_x += landmarks.landmark[i].x
        avg_y += landmarks.landmark[i].y

    avg_x = avg_x / len(landmarks.landmark)
    avg_y = avg_y / len(landmarks.landmark)
    return avg_x, avg_y

def checkGrab(finger_tips, frame):
    avg_x = 0
    avg_y = 0
    length = frame.shape[1]
    width = frame.shape[0]

    for points in finger_tips:
        avg_x += points.x
        avg_y += points.y
    
    avg_x = avg_x/5
    avg_y = avg_y/5

    for i in range(0, 5):
        dist = math.sqrt(math.pow(finger_tips[i].x-avg_x, 2) + math.pow(finger_tips[i].y-avg_y, 2));
        if dist >= 0.06:
            return False
    return True

def detectMotion(hand_landmarks, init_x, init_y):
    # We can do multiple detections along the way
    # the motion of the hand should indicate: swipe up, swipe down, swipe left and swipe right
    # Merely doing the release point relative to initial point might not be enough <- or maybe it is?
    # I am not sure because opencv can sometimes jitter around and if the program detects grabbing = False, then
    # user basically swipes in an unwanted direction.
    print("Work in Progress. . .")

def detectDirection(init_x, init_y, cur_x, cur_y, frame):
    # Think of the regions being seperated like a big X
    # The lines can be modelled as: y = (height/width)x and y = -(height/width)x
    cur_x -= init_x
    cur_y -= init_y
    a = -1
    b = -1
    width = frame.shape[1]
    height = frame.shape[0]
    if cur_y <= (height/width)*cur_x:
        a = 1
    else:
        a = 0
    if cur_y <= -(height/width)*cur_x:
        b = 1
    else:
        b = 0

    if a == 1:
        if b == 1:
            print("Swipe Up")
        else:
            print("Swipe Right")
    else:
        if b == 1:
            print("Swipe Left")
        else:
            print("Swipe Down")


# Hand gesture detection
with mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6) as hands:

    counter = 0
    grabbing = False
    hand_x = -1
    hand_y = -1

    while capture.isOpened():

        ret, frame = capture.read()
        frame = cv.resize(frame, (int(frame.shape[1]*1.5), int(frame.shape[0]*1.5)))
        
        img = cv.cvtColor(cv.flip(frame, 1), cv.COLOR_BGR2RGB)
        img.flags.writeable = False;

        results = hands.process(img)
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        frame = cv.flip(frame, 1)

        # If there are hands deteced.
        if results.multi_hand_landmarks:
            # Iterate through the two hands
            for hand_landmarks in results.multi_hand_landmarks:
                # Five finger tips
                # 4, 8, 12, 16, 20
                finger_tips = []
                finger_tips.append(hand_landmarks.landmark[4])
                finger_tips.append(hand_landmarks.landmark[8])
                finger_tips.append(hand_landmarks.landmark[12])
                finger_tips.append(hand_landmarks.landmark[16])
                finger_tips.append(hand_landmarks.landmark[20])
                


                if checkGrab(finger_tips, frame):
                    # print("Grabbing ", counter)
                    # counter+=1
                    if grabbing == False:
                        hand_x, hand_y = avg_point(hand_landmarks)
                    grabbing = True
                else:
                    if grabbing == True:
                        cur_x, cur_y = avg_point(hand_landmarks)
                        detectDirection(hand_x, hand_y, cur_x, cur_y, frame)
                    grabbing = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS, 
                    mp_drawing.DrawingSpec(color=(207,252,3), thickness=3, circle_radius=3),
                    mp_drawing.DrawingSpec(color=(255,255,255), thickness=3, circle_radius=1)
                )

        cv.imshow('Video', frame)
        if cv.waitKey(10) & 0xFF == ord('q'):
            break


capture.release()
cv.destroyAllWindows()
