import cv2
import mediapipe as mp
import math

# Ayarlar
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)

# Oyun Değişkenleri
puck_x, puck_y = 320, 240
speed_x, speed_y = 5, 5
radius = 25
paddle_radius = 50
score = 0

while True:
    success, frame = cap.read()
    if not success: break
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # --- HAREKET VE SINIR KONTROLÜ (GÜNCELLENDİ) ---
    puck_x += speed_x
    puck_y += speed_y

    # Sağ ve Sol Kenar Kontrolü
    if puck_x <= radius:
        puck_x = radius # Topu içeri it
        speed_x *= -1
    elif puck_x >= w - radius:
        puck_x = w - radius # Topu içeri it
        speed_x *= -1

    # Alt ve Üst Kenar Kontrolü
    if puck_y <= radius:
        puck_y = radius # Topu içeri it
        speed_y *= -1
    elif puck_y >= h - radius:
        puck_y = h - radius # Topu içeri it
        speed_y *= -1

    # --- EL TAKİBİ ---
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            cx = int(hand_landmarks.landmark[8].x * w)
            cy = int(hand_landmarks.landmark[8].y * h)
            
            distance = math.hypot(cx - puck_x, cy - puck_y)
            
            if distance < (radius + paddle_radius):
                speed_x *= -1
                speed_y *= -1
                score += 1
                # Çarpışma anında topun elin içinde hapsolmasını engelle
                puck_x += speed_x * 4
                puck_y += speed_y * 4

            # Raketi çiz
            cv2.circle(frame, (cx, cy), paddle_radius, (255, 0, 0), 2)

    # --- GÖRSEL ÖĞELER ---
    cv2.putText(frame, f"SKOR: {score}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
    cv2.circle(frame, (int(puck_x), int(puck_y)), radius, (0, 255, 0), -1)
    cv2.circle(frame, (int(puck_x), int(puck_y)), radius, (0, 0, 0), 2)

    cv2.imshow("Hava Hokeyi - Osmen Kaya", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()