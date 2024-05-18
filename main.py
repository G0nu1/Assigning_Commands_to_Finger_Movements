import cv2
import time
import mediapipe as mp
import math 


cap = cv2.VideoCapture(0)

# first step initialize the mp classes
mpHand = mp.solutions.hands
hands = mpHand.Hands()
mpDraw = mp.solutions.drawing_utils

# Initialize variable to store the time when fingers are detected to be close
close_start_time = None

# Initialize variables for landmark positions
x4, y4, x8, y8 = 0, 0, 0, 0

pTime = 0
cTime = 0

# continue the loop as long as the hand is detected
while True:
    # success: + || - for indicate to read
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    #for deteting hand
    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks)
    
    # for palmer landmark
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, connections = mpHand.HAND_CONNECTIONS)
            
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                
                cx, cy = int(lm.x*w), int(lm.y*h) 
                
                # wrist
                if id == 4:
                    x4, y4 = cx, cy

                if id == 8:
                    x8, y8 = cx, cy

                # Calculate distance
                if x4 != 0 and y4 != 0 and x8 != 0 and y8 != 0:
                    r = math.sqrt((x4 - x8) ** 2 + (y4 - y8) ** 2)
                    if r < 19:
                        cv2.circle(img, (x4, y4), 11, (255,0,0), cv2.FILLED)
                        cv2.putText(img, "Fingers Close", (10, 120), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 5)
                        if close_start_time is None:
                            close_start_time = time.time()  # Start the timer
                        break
    
    # Check if the fingers have been close for 1 seconds
    if close_start_time is not None and (time.time() - close_start_time) > 1:
        break

                
    
    # fps
    cTime = time.time()
    fps = 1 / (cTime- pTime)
    pTime = cTime
    
    cv2.putText(img, "FPS: "+str(int(fps)), (10,75), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 5)
    
    cv2.imshow("img", img)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
