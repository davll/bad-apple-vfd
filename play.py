import cv2
import numpy as np
from vfd import *

VFD_CHAR_W = 5
VFD_CHAR_H = 7
VFD_COLS = 8
VFD_ROWS = 3

IMG_W = VFD_COLS * VFD_CHAR_W
IMG_H = VFD_ROWS * VFD_CHAR_H

TARGET_FRAME_TIME = 1.0 / 30.0

# Video Frame Processing

def process_frame(frame):
    image = frame[:,:,0]
    image = cv2.resize(image, (IMG_W, IMG_H), interpolation = cv2.INTER_AREA)
    retval, image = cv2.threshold(image, 128, 1, 0)
    return image

def show_processed_image(title, image):
    view = cv2.resize(image * 255, (IMG_W * 16, IMG_H * 16), interpolation = cv2.INTER_NEAREST)
    cv2.imshow(title, view)

def generate_rows(image):
    for i in range(VFD_ROWS):
        ys = i * VFD_CHAR_H
        ye = ys + VFD_CHAR_H
        yield (i, image[ys:ye,:])

def display_row(i, row):
    pad = np.zeros(row.shape[1], dtype=np.uint8)
    row = np.vstack((row, pad))
    data = np.packbits(np.flipud(row), 0)
    data = data.flatten()
    cs = VFD_CSs[i]
    vfd_write_cgram(cs, 0, data)
    vfd_write_dcram(cs, 0, [0,1,2,3,4,5,6,7])
    vfd_show(cs)

#====================================================================
# Main
#====================================================================

def main():
    # Prepare VFD
    vfd_boot()
    vfd_init(VFD_CS0)
    vfd_init(VFD_CS1)
    vfd_init(VFD_CS2)
    vfd_text(VFD_CS0, b"HELLO")
    vfd_show(VFD_CS0)
    vfd_text(VFD_CS1, b"WORLD")
    vfd_show(VFD_CS1)
    vfd_text(VFD_CS2, b"RASPI")
    vfd_show(VFD_CS2)
    # Open the video
    cap = cv2.VideoCapture("bad_apple.mp4")
    # Play the video
    while cv2.waitKey(1) != 27:
        # Read a frame
        retval, frame = cap.read()
        if not retval:
            break
        # Display the frame
        cv2.imshow("Bad Apple - Original", frame)
        # Process the frame
        image = process_frame(frame)
        show_processed_image("Bad Apple - Processed", image)
        # Send data to the VFD
        for i, row in generate_rows(image):
            display_row(i, row)

if __name__ == "__main__":
    try:
        main()
    finally:
        vfd_reset()
