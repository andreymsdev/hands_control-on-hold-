import cv2
import mediapipe as mp
import numpy as np
import pulsectl
import os
import time 

try:
    pulse = pulsectl.Pulse('volume-control')
except Exception as e:
    print(f"ERRO: Não foi possível conectar ao PulseAudio: {e}. O controle de volume está desativado.")
    pulse = None

def aumentar_volume():
    if pulse:
        try:
            sink = pulse.sink_list()[0]
            pulse.volume_change_all_chans(sink, 0.05) # +5%
            print("Volume Aumentado")
        except Exception as e:
            print(f"Erro ao aumentar volume: {e}")

def diminuir_volume():
    if pulse:
        try:
            sink = pulse.sink_list()[0]
            pulse.volume_change_all_chans(sink, -0.05) # -5%
            print("Volume Diminuído")
        except Exception as e:
            print(f"Erro ao diminuir volume: {e}")

# Mediapipe config

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Câmera 
cap = cv2.VideoCapture(0) 
if not cap.isOpened():
    print("ERRO FATAL: Não foi possível abrir a câmera.")
    exit()

camera_width = 1280
camera_height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

# Gestos
def dedos_levantados(hand_landmarks):
    dedos = {}
    dedos["Polegar"] = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x    
    dedos["Indicador"] = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    dedos["Medio"] = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    dedos["Anelar"] = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    dedos["Mindinho"] = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y
    return list(dedos.values())

cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL) 

# Controle do tempo
ultimo_comando_tempo = time.time()
INTERVALO_MINIMO = 0.2 # 200ms

# Loop

while True:
    ret, frame = cap.read()

    # Esc (fecha)
    if cv2.waitKey(1) & 0xFF == 27:  
        break
        
        agora = time.time()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Verificação de tempo
    agora = time.time()
    pode_executar_comando = (agora - ultimo_comando_tempo) > INTERVALO_MINIMO

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            dedos_status = dedos_levantados(hand_landmarks)

            # Controles
            if pode_executar_comando:
                # MÃO ABERTA -> AUMENTAR VOLUME
                if all(dedos_status):
                    cv2.putText(frame, "AUMENTAR VOLUME", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    aumentar_volume()
                    ultimo_comando_tempo = agora

                # MÃO FECHADA -> DIMINUIR VOLUME
                elif not any(dedos_status):
                    cv2.putText(frame, "DIMINUIR VOLUME", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    diminuir_volume()
                    ultimo_comando_tempo = agora
            
    # O imshow fica fora do 'for' das mãos, mas DENTRO do 'while True'
    cv2.imshow("Hand Tracking", frame) 

# Fim
cap.release()
cv2.destroyAllWindows()
