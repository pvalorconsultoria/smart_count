import cv2
import numpy as np

PIECE_WIDTH  = 80
PIECE_HEIGHT = 80

video_path = "C:\\Users\\diego\\Code\\OpenCV\\assets\\video_clips.mp4"

cap = cv2.VideoCapture(video_path)

is_moving = False
frame = None
count = 70

target_x, target_y = None, None

def get_mouse_position(event, x, y, flags, param):
    global is_moving, target_x, target_y

    if not is_moving:
        cv2.rectangle(frame, (x,y), (x + PIECE_WIDTH, y + PIECE_HEIGHT), (0, 255, 0), 2)

    if event == cv2.EVENT_LBUTTONDOWN:
        target_x, target_y = x, y

        is_moving = not is_moving

def save_target_to_folder(label):
    global frame, target_x, target_y, count

    target = frame[target_y+2:target_y-2+PIECE_HEIGHT, target_x+2:target_x-2+PIECE_WIDTH, :]

    cv2.imwrite(f'./datasets/CLIPS_1/{count}_{label}.png', target)

    count += 1

cv2.namedWindow('Dataset Maker')

cv2.setMouseCallback('Dataset Maker', get_mouse_position)

_, frame = cap.read()

while cap.isOpened():

    cv2.imshow('Dataset Maker', frame)

    if not is_moving:
        _, frame = cap.read()

    print(frame.shape)

    pressed_key = cv2.waitKey(40)

    if pressed_key == 27:
        break
    elif pressed_key == ord('y'):
        save_target_to_folder('true')
    elif pressed_key == ord('n'):
        save_target_to_folder('false')
