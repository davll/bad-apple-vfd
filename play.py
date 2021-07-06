from time import monotonic_ns as abstime_ns
from time import sleep
import cv2
import numpy as np

VFD_CHAR_W = 5
VFD_CHAR_H = 7
VFD_COLS = 8
VFD_ROWS = 3

IMG_W = VFD_COLS * VFD_CHAR_W
IMG_H = VFD_ROWS * VFD_CHAR_H

# Init the GPIO

# Init the VFD

# Open the video
cap = cv2.VideoCapture("bad_apple.mp4")

# Play the video
while cv2.waitKey(30) != 27:
    # Read a frame
    retval, frame = cap.read()
    if not retval:
        break
    # Display the frame
    cv2.imshow("Bad Apple - Original", frame)
    # Process the frame
    image = cv2.resize(frame, (IMG_W, IMG_H), interpolation = cv2.INTER_AREA)
    retval, image = cv2.threshold(image, 128, 1, 0)
    image_pv = cv2.resize(image * 255, (IMG_W * 16, IMG_H * 16), interpolation = cv2.INTER_NEAREST)
    cv2.imshow("Bad Apple - Processed", image_pv)
    # Send data to the VFD
    for i in range(VFD_ROWS):
        ys = i * VFD_CHAR_H
        ye = ys + VFD_CHAR_H
        for j in range(VFD_COLS):
            xs = j * VFD_CHAR_W
            xe = xs + VFD_CHAR_W
            block = image[ys:ye,xs:xe]

