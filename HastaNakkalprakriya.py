import mediapipe as mp
import cv2
import time
import math
import numpy as np



import pyfirmata

pin1=[9,10,11,12,13]
port="COM3"
board=pyfirmata.Arduino(port)

for i in pin1:
    board.digital[i].mode=pyfirmata.SERVO
    board.digital[i].write(0)



#pyfirmata end


#setting camera
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,460)
cap.set(10,100)

#setting time for fps 
cTime=0
pTime=0

x0,x4,x8,x12,x16,x20=0,0,0,0,0,0
y0,y4,y8,y12,y16,y20=0,0,0,0,0,0
x17,y17=0,0
#midx,midy=0,0
#length=0



#setting MediaPipe 
mpHands=mp.solutions.hands
hands=mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw=mp.solutions.drawing_utils


while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img,handLms)
            for id,lm in enumerate(handLms.landmark):
                #print(id,lm.x,lm.y)
                
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                if id==0:
                    cv2.circle(img,(cx,cy),8,(255,255,0))
                    x0,y0=cx,cy
                    
                if id==4:
                    cv2.circle(img,(cx,cy),8,(255,255,0))
                    x4,y4=cx,cy

                if id==8:
                    cv2.circle(img,(cx,cy),8,(255,255,0))
                    x8,y8=cx,cy

                if id==12:
                    cv2.circle(img,(cx,cy),8,(255,255,0))
                    x12,y12=cx,cy

                if id==16:
                    cv2.circle(img,(cx,cy),8,(255,255,0))
                    x16,y16=cx,cy

                if id==20:
                    cv2.circle(img,(cx,cy),8,(255,255,0))
                    x20,y20=cx,cy

                if id==17:
                    cv2.circle(img,(cx,cy),8,(255,255,0))
                    x17,y17=cx,cy
                

                #Lines shown
                cv2.line(img,(x4,y4),(x17,y17),(255,255,0),1)
                cv2.line(img,(x0,y0),(x8,y8),(255,255,0),1)
                cv2.line(img,(x0,y0),(x12,y12),(255,255,0),1)
                cv2.line(img,(x0,y0),(x16,y16),(255,255,0),1)
                cv2.line(img,(x0,y0),(x20,y20),(255,255,0),1)
                 
                #finger lengths 
                thumb=math.hypot(x4-x17,y4-y17)
                fore_finger=math.hypot(x0-x8,y0-y8)
                middle_finger=math.hypot(x0-x12,y0-y12)
                ring_finger=math.hypot(x0-x16,y0-y16)
                pinky_finger=math.hypot(x0-x20,y0-y20)

                #midddle points
                mid_thumb_x,mid_thumb_y=int((x4+x17)/2),int((y4+y17)/2)
                cv2.circle(img,(mid_thumb_x,mid_thumb_y),10,(255,0,0),cv2.FILLED)

                
                mid_fore_x,mid_fore_y=int((x0+x8)/2),int((y0+y8)/2)
                cv2.circle(img,(mid_fore_x,mid_fore_y),10,(255,0,0),cv2.FILLED)

                mid_middle_x,mid_middle_y=int((x0+x12)/2),int((y0+y12)/2)
                cv2.circle(img,(mid_middle_x,mid_middle_y),10,(255,0,0),cv2.FILLED)

                mid_ring_x,mid_ring_y=int((x0+x16)/2),int((y0+y16)/2)
                cv2.circle(img,(mid_ring_x,mid_ring_y),10,(255,0,0),cv2.FILLED)

                mid_pinky_x,mid_pinky_y=int((x0+x20)/2),int((y0+y20)/2)
                cv2.circle(img,(mid_pinky_x,mid_pinky_y),10,(255,0,0),cv2.FILLED)

                #for thumb control
                if thumb < 50:
                    cv2.circle(img,(mid_thumb_x,mid_thumb_y),10,(0,0,0),cv2.FILLED)
                    board.digital[9].write(0)
                if thumb >50:
                    cv2.circle(img,(mid_thumb_x,mid_thumb_y),10,(0,255,0),cv2.FILLED)
                    board.digital[9].write(90)


                #for forefinger control
                if fore_finger < 70:
                    cv2.circle(img,(mid_fore_x,mid_fore_y),10,(0,0,0),cv2.FILLED)
                    board.digital[10].write(0)
                if fore_finger > 70:
                    cv2.circle(img,(mid_fore_x,mid_fore_y),10,(0,255,0),cv2.FILLED)
                    board.digital[10].write(90)
                

                #for middlefinger control
                if middle_finger < 90:
                    cv2.circle(img,(mid_middle_x,mid_middle_y),10,(0,0,0),cv2.FILLED)
                    board.digital[11].write(0)
                
                if middle_finger > 90:
                    cv2.circle(img,(mid_middle_x,mid_middle_y),10,(0,255,0),cv2.FILLED)
                    board.digital[11].write(90)
                
                 

                #for ring finger control
                if ring_finger < 85:
                    cv2.circle(img,(mid_ring_x,mid_ring_y),10,(0,0,0),cv2.FILLED)
                    board.digital[12].write(0)
                
                if ring_finger > 85:
                    cv2.circle(img,(mid_ring_x,mid_ring_y),10,(0,255,0),cv2.FILLED)
                    board.digital[12].write(90)
                

                if pinky_finger < 80:
                    cv2.circle(img,(mid_pinky_x,mid_pinky_y),10,(0,0,0),cv2.FILLED)
                    board.digital[13].write(0)
                if pinky_finger > 80:
                    cv2.circle(img,(mid_pinky_x,mid_pinky_y),10,(0,0,0),cv2.FILLED)
                    board.digital[13].write(90)

                
                print('thumb',int(thumb))
                print('fore_finger',int(fore_finger))
                print('middle_finger',int(middle_finger))
                print('ring_finger',int(ring_finger))
                print('pinky_finger',int(pinky_finger))
                
                '''thumb=math.hypot(x4-x17,y4-y17)
                print(int(thumb))'''


                

   


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,'fps'+str(int(fps)),(20,30),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
     

    cv2.imshow('Image',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break