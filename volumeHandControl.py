import cv2
import time
import numpy as np
import math
import handTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 648, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
detector = htm.handDetector(maxHands=4, detection_con=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
minVolume = volumeRange[0]
maxVolume = volumeRange[1]
volBar = 400
vol = 0
volper = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2, = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), -1)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), -1)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), -1)
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        vol = np.interp(length, [50, 200], [minVolume, maxVolume])
        volBar = np.interp(length, [50, 200], [400, 150])
        volPer = np.interp(length, [50, 200], [0, 100])
        # print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), -1)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)

    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), -1)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (48, 70), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 3)
    cv2.putText(img, f"{int(volper)}", (40, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), 3)


    cv2.imshow("image", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
