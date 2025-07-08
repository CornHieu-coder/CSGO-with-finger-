import cv2, mediapipe as mp, pydirectinput, pyautogui, pygetwindow as gw

# 1) Setup
SCREEN_W, SCREEN_H = pyautogui.size()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.4, min_tracking_confidence=0.1)
cap = cv2.VideoCapture(0)

def csgo_is_focused():
    win = gw.getActiveWindow()
    return win and "Counter-Strike" in win.title

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1) 
    if not success: break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        lm = results.multi_hand_landmarks[0].landmark
        nx, ny = lm[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, lm[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        px, py = int(nx * frame.shape[1]), int(ny * frame.shape[0])
        sx, sy = int(nx * SCREEN_W), int(ny * SCREEN_H)

        # Move & click only if CS:GO is focused
        if csgo_is_focused():
            pydirectinput.moveTo(sx, sy, duration=0)
            if lm[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > lm[mp_hands.HandLandmark.INDEX_FINGER_PIP].y + 0.07:
                pydirectinput.click()

        # Draw crosshair for debugging
        cv2.line(image, (px-15, py), (px+15, py), (0, 255, 0), 2)
        cv2.line(image, (px, py-15), (px, py+15), (0, 255, 0), 2)

    cv2.imshow("Hand Gun Controller", image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
