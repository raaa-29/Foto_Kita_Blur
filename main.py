import cv2
import mediapipe as mp
from animation import EnergyRing
# ======================================
# MediaPipe
# ======================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ======================================
# Kamera
# ======================================

camera = cv2.VideoCapture(0)
animations = []

# ======================================
# Blur Animation
# ======================================

blur_level = 1
target_blur = 1
MAX_BLUR = 55

# ======================================
# Fungsi Deteksi Peace
# ======================================

def is_peace(hand):

    index = hand.landmark[8].y < hand.landmark[6].y
    middle = hand.landmark[12].y < hand.landmark[10].y

    ring = hand.landmark[16].y > hand.landmark[14].y
    pinky = hand.landmark[20].y > hand.landmark[18].y

    return index and middle and ring and pinky


# ======================================
# Main Loop
# ======================================

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    peace = False

    if result.multi_hand_landmarks:

        for hand in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            if is_peace(hand):

                peace = True

                h, w, _ = frame.shape

                palm = hand.landmark[9]

                x = int(palm.x * w)
                y = int(palm.y * h)

                if len(animations) == 0:
                    animations.append(EnergyRing(x, y))

                cv2.putText(
                    frame,
                    "PEACE DETECTED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

    # ======================================
    # Smooth Blur Animation
    # ======================================

    if peace:
        target_blur = MAX_BLUR
    else:
        target_blur = 1

    speed = 4

    if blur_level < target_blur:
        blur_level += speed

    elif blur_level > target_blur:
        blur_level -= speed

    blur_level = max(1, min(MAX_BLUR, blur_level))

    kernel = blur_level

    if kernel % 2 == 0:
        kernel += 1

    if kernel > 1:
        frame = cv2.GaussianBlur(frame, (kernel, kernel), 0)

    # ======================================
    # Info
    # ======================================

    cv2.putText(
        frame,
        f"Blur : {kernel}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )
    for animation in animations:

        animation.update()

        animation.draw(frame)

    animations = [a for a in animations if not a.finished]
    cv2.imshow("Foto Kita Blur", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()