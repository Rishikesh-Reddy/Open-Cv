import handTrackingModule as htm
import time
import cv2

cap = cv2.VideoCapture(0)
detector = htm.handDetector(detection_con=0.8, tracking_con=0.8)
cap.set(3, 648)
cap.set(4, 480)
while True:
    success, img = cap.read()

    fingersUp = []
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    # lmlsit1 = detector.findPosition(img, handNO=1)
    if len(lmlist) != 0:

        for i in [8, 12, 16, 20]:
            if lmlist[i][2] < lmlist[i - 2][2]:
                fingersUp.append(1)
            else:
                fingersUp.append(0)
        if lmlist[4][1] > lmlist[17][1]:
            if lmlist[4][1] > lmlist[2][1]:
                fingersUp.append(1)
            else:
                fingersUp.append(0)
        else:
            if lmlist[4][1] < lmlist[2][1]:
                fingersUp.append(1)
            else:
                fingersUp.append(0)

        cv2.putText(img, str(fingersUp.count(1)), (40, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 0), 2)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
