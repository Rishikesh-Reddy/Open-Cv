import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 4, 0.8, 0.8)
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)


    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:

        for handlms in results.multi_hand_landmarks:
            lmlist = []
            for id, lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
                lmlist.append([id, cx, cy])
            if lmlist[4][1] > lmlist[17][1]:
                cv2.putText(img, "right", (10, 110), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                # print(True)

            else:
                cv2.putText(img, "left", (10, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)

    cv2.imshow("image", img)
    k = cv2.waitKey(1) & 0xFF == ord('q')
    if k:
        break
