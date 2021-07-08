import cv2
import numpy as np

VFD_CHAR_W = 5
VFD_CHAR_H = 7
VFD_COLS = 8
VFD_ROWS = 3

IMG_W = VFD_COLS * VFD_CHAR_W
IMG_H = VFD_ROWS * VFD_CHAR_H

TARGET_FRAME_TIME = 1.0 / 30.0

def process_frame(frame):
    image = frame[:,:,0]
    image = cv2.resize(image, (IMG_W, IMG_H), interpolation = cv2.INTER_AREA)
    retval, image = cv2.threshold(image, 128, 1, 0)
    return image

def show_processed_image(title, image):
    view = cv2.resize(image * 255, (IMG_W * 16, IMG_H * 16), interpolation = cv2.INTER_NEAREST)
    cv2.imshow(title, view)

def generate_blocks(image):
    for i in range(VFD_ROWS):
        ys = i * VFD_CHAR_H
        ye = ys + VFD_CHAR_H
        for j in range(VFD_COLS):
            xs = j * VFD_CHAR_W
            xe = xs + VFD_CHAR_W
            yield (i, j, image[ys:ye,xs:xe])

def display_block(i, j, blk):
    pass

#====================================================================
# Main
#====================================================================

def main():
    # Open the video
    cap = cv2.VideoCapture("bad_apple.mp4")
    # Play the video
    while cv2.waitKey(33) != 27:
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
        for i, j, blk in generate_blocks(image):
            display_block(i, j, blk)

def cleanup():
    pass

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup()
