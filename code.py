import cv2
import numpy as np
from collections import deque


cam1 = cv2.VideoCapture("http://192.168.1.4:2243/video")  # edge cam (u can use apps like droid cam to get real time footage)
cam2 = cv2.VideoCapture("http://192.168.1.7:1347/video")  # lbw cam

buffer_size = 300
buffer1 = deque(maxlen=buffer_size)
buffer2 = deque(maxlen=buffer_size)

print("Press R for replay, Q to quit")

while True:

    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if not ret1 or not ret2:
        break

    buffer1.append(frame1.copy())
    buffer2.append(frame2.copy())

    frame1 = cv2.resize(frame1,(640,360))
    frame2 = cv2.resize(frame2,(640,360))

    top = np.hstack((frame1,frame2))

    cv2.putText(top,"EDGE CAMERA",(50,30),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    cv2.putText(top,"LBW CAMERA",(700,30),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    cv2.imshow("DRS LIVE",top)

    key = cv2.waitKey(1) & 0xFF

    
    if key == ord('r'):

        print("DRS Replay")

        for f1,f2 in zip(buffer1,buffer2):

            f1 = cv2.resize(f1,(640,360))
            f2 = cv2.resize(f2,(640,360))

            replay = np.hstack((f1,f2))

            cv2.putText(replay,"REPLAY",
                        (550,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(0,0,255),3)

            cv2.imshow("DRS REPLAY",replay)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

    if key == ord('q'):
        break

cam1.release()
cam2.release()
cv2.destroyAllWindows()
