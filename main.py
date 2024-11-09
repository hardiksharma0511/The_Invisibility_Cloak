import cv2
import numpy as np
import time


def capture_background(cap):
    time.sleep(2)
    for i in range(30):
        ret, background = cap.read()
    return background


def main():
    cap = cv2.VideoCapture(0)

    print("Capturing background... Please wait")
    background = capture_background(cap)

    lower_blue = np.array([94, 80, 2])
    upper_blue = np.array([126, 255, 255])

    flip_video = False

    print("Starting invisibility cloak effect. Press 'f' to flip video, 'q' to quit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if flip_video:
            frame = cv2.flip(frame, 1)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

        mask_inverse = cv2.bitwise_not(mask)

        cloak_part = cv2.bitwise_and(background, background, mask=mask)

        non_cloak_part = cv2.bitwise_and(frame, frame, mask=mask_inverse)

        final_output = cv2.addWeighted(cloak_part, 1, non_cloak_part, 1, 0)

        cv2.imshow('Invisibility Cloak', final_output)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('f'):
            flip_video = not flip_video

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()