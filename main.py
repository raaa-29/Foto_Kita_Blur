import cv2
import math
import mediapipe as mp

from animation import EnergyRing, AnimationManager
from particles import SakuraParticle

# ======================================
# MediaPipe & Kamera Setup
# ======================================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

camera = cv2.VideoCapture(0)
animation = AnimationManager()

# ======================================
# Blur & Tracking Variables
# ======================================
blur_level = 1
target_blur = 1
MAX_BLUR = 55

last_finger_x = None
last_finger_y = None


# ======================================
# Gesture Detection Functions
# ======================================
def is_peace(hand):
    index = hand.landmark[8].y < hand.landmark[6].y
    middle = hand.landmark[12].y < hand.landmark[10].y
    ring = hand.landmark[16].y > hand.landmark[14].y
    pinky = hand.landmark[20].y > hand.landmark[18].y

    return index and middle and ring and pinky


def is_pointing(hand):
    # Telunjuk Lurus ke atas
    index = hand.landmark[8].y < hand.landmark[6].y
    # Jari tengah, manis, kelingking menekuk
    middle = hand.landmark[12].y > hand.landmark[10].y
    ring = hand.landmark[16].y > hand.landmark[14].y
    pinky = hand.landmark[20].y > hand.landmark[18].y

    return index and middle and ring and pinky


# ======================================
# Main Loop
# ======================================
while True:
    success, frame = camera.read()
    if not success:
        print("Gagal membuka kamera.")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

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

            # ----------------------------------
            # 1. Mode Peace (Hanya Blur + Ring)
            # ----------------------------------
            if is_peace(hand):
                peace = True
                palm = hand.landmark[9]
                x = int(palm.x * w)
                y = int(palm.y * h)

                # Bubble / ParticleExplosion SUDAH DIHILANGKAN
                if len(animation.animations) == 0:
                    animation.add(EnergyRing(x, y))

                cv2.putText(
                    frame, "PEACE DETECTED", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
                )
                last_finger_x, last_finger_y = None, None

            # ----------------------------------
            # 2. Mode Pointing (Canvas Sakura Brush)
            # ----------------------------------
            elif is_pointing(hand):
                index_tip = hand.landmark[8]
                cx, cy = int(index_tip.x * w), int(index_tip.y * h)

                if last_finger_x is not None and last_finger_y is not None:
                    dist = math.hypot(cx - last_finger_x, cy - last_finger_y)

                    # Rapatkan jarak (setiap 5 pixel diisi bunga) agar garis padat & tidak putus
                    steps = max(1, int(dist / 5))
                    for i in range(steps):
                        t = i / steps
                        interp_x = int(last_finger_x + (cx - last_finger_x) * t)
                        interp_y = int(last_finger_y + (cy - last_finger_y) * t)
                        
                        animation.add(SakuraParticle(interp_x, interp_y))
                else:
                    animation.add(SakuraParticle(cx, cy))

                last_finger_x, last_finger_y = cx, cy

                cv2.putText(
                    frame, "CANVAS PAINTING 🌸", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (203, 192, 255), 2
                )
                
            else:
                last_finger_x, last_finger_y = None, None
    else:
        last_finger_x, last_finger_y = None, None

    # ======================================
    # Blur Smooth Transition
    # ======================================
    if peace:
        target_blur = MAX_BLUR
    else:
        target_blur = 1

    speed = 5
    if blur_level < target_blur:
        blur_level += speed
    elif blur_level > target_blur:
        blur_level -= speed

    blur_level = max(1, min(MAX_BLUR, blur_level))
    kernel = int(blur_level)
    if kernel % 2 == 0:
        kernel += 1

    if kernel > 1:
        frame = cv2.GaussianBlur(frame, (kernel, kernel), 0)

    # ======================================
    # Animation Engine Update & Render
    # ======================================
    animation.update()
    animation.draw(frame)

    cv2.imshow("Interactive AR Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()