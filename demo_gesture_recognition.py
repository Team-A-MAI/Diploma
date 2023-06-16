import cv2
import mediapipe as mp
from pynput.keyboard import Controller

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)


keyboard = Controller()

with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Не удалось получить кадр с камеры.")
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(image_rgb)

        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                )

                if handedness.classification[0].label == "Left":
                    right_hand_landmarks = hand_landmarks.landmark
                    right_hand_coordinates = {
                        'wrist_x': right_hand_landmarks[mp_hands.HandLandmark.WRIST].x,
                        'thumb_x': right_hand_landmarks[mp_hands.HandLandmark.THUMB_TIP].x,
                        'index_x': right_hand_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
                        'middle_x': right_hand_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,
                        'ring_x': right_hand_landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].x,
                        'pinky_x': right_hand_landmarks[mp_hands.HandLandmark.PINKY_TIP].x,
                        'wrist_y': right_hand_landmarks[mp_hands.HandLandmark.WRIST].y,
                        'thumb_y': right_hand_landmarks[mp_hands.HandLandmark.THUMB_TIP].y,
                        'index_y': right_hand_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y,
                        'middle_y': right_hand_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y,
                        'ring_y': right_hand_landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y,
                        'pinky_y': right_hand_landmarks[mp_hands.HandLandmark.PINKY_TIP].y,
                    }

                    if (
                            right_hand_coordinates['wrist_y'] > right_hand_coordinates['thumb_y'] and
                            right_hand_coordinates['wrist_y'] > right_hand_coordinates['index_y'] and
                            right_hand_coordinates['wrist_y'] > right_hand_coordinates['middle_y'] and
                            right_hand_coordinates['wrist_y'] > right_hand_coordinates['ring_y'] and
                            right_hand_coordinates['wrist_y'] > right_hand_coordinates['pinky_y']
                    ):
                        if right_hand_coordinates['thumb_x'] > right_hand_coordinates['pinky_x']:
                            print("Правая рука поднята и повернута ладонью к экрану.")
                        else:
                            print("Правая рука поднята.")
                    elif (
                            right_hand_coordinates['wrist_y'] < right_hand_coordinates['thumb_y'] and
                            right_hand_coordinates['wrist_y'] < right_hand_coordinates['index_y'] and
                            right_hand_coordinates['wrist_y'] < right_hand_coordinates['middle_y'] and
                            right_hand_coordinates['wrist_y'] < right_hand_coordinates['ring_y'] and
                            right_hand_coordinates['wrist_y'] < right_hand_coordinates['pinky_y']
                    ):
                        if right_hand_coordinates['thumb_x'] < right_hand_coordinates['pinky_x']:
                            print("Правая рука опущена и повернута ладонью к экрану.")
                        else:
                            print("Правая рука опущена.")

                elif handedness.classification[0].label == "Right":
                    left_hand_landmarks = hand_landmarks.landmark
                    left_hand_coordinates = {
                        'wrist_x': left_hand_landmarks[mp_hands.HandLandmark.WRIST].x,
                        'thumb_x': left_hand_landmarks[mp_hands.HandLandmark.THUMB_TIP].x,
                        'index_x': left_hand_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
                        'middle_x': left_hand_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,
                        'ring_x': left_hand_landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].x,
                        'pinky_x': left_hand_landmarks[mp_hands.HandLandmark.PINKY_TIP].x,
                        'wrist_y': left_hand_landmarks[mp_hands.HandLandmark.WRIST].y,
                        'thumb_y': left_hand_landmarks[mp_hands.HandLandmark.THUMB_TIP].y,
                        'index_y': left_hand_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y,
                        'middle_y': left_hand_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y,
                        'ring_y': left_hand_landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y,
                        'pinky_y': left_hand_landmarks[mp_hands.HandLandmark.PINKY_TIP].y
                    }

                    if (
                            left_hand_coordinates['wrist_y'] > left_hand_coordinates['thumb_y'] and
                            left_hand_coordinates['wrist_y'] > left_hand_coordinates['index_y'] and
                            left_hand_coordinates['wrist_y'] > left_hand_coordinates['middle_y'] and
                            left_hand_coordinates['wrist_y'] > left_hand_coordinates['ring_y'] and
                            left_hand_coordinates['wrist_y'] > left_hand_coordinates['pinky_y']
                    ):
                        if left_hand_coordinates['thumb_x'] < left_hand_coordinates['pinky_x']:
                            print("Левая рука поднята и повернута ладонью к экрану")
                        else:
                            print("Левая рука поднята")
                    elif (
                            left_hand_coordinates['wrist_y'] < left_hand_coordinates['thumb_y'] and
                            left_hand_coordinates['wrist_y'] < left_hand_coordinates['index_y'] and
                            left_hand_coordinates['wrist_y'] < left_hand_coordinates['middle_y'] and
                            left_hand_coordinates['wrist_y'] < left_hand_coordinates['ring_y'] and
                            left_hand_coordinates['wrist_y'] < left_hand_coordinates['pinky_y']
                    ):
                        if left_hand_coordinates['thumb_x'] > left_hand_coordinates['pinky_x']:
                            print("Левая рука опущена и повернута ладонью к экрану")
                        else:
                            print("Левая рука опущена")
                    else:
                        print("*** Никакая рука не опущена и не поднята, но есть в кадре ***")

        cv2.imshow('MediaPipe Hands', image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
