import cv2
import mediapipe as mp
import numpy as np
import screeninfo
import pulsectl
import os

# iniciar
try:
    pulse = pulsectl.Pulse('volume-control')
except Exception as e:
    print(f"ERRO: Não foi possível conectar ao PulseAudio: {e}. O controle de volume está desativado.")
    pulse = None

def aumentar_volume():
    if pulse:
        try:
            sink = pulse.sink_list()[0]
            pulse.volume_change_all_chans(sink, 0.05)  # +5%
            # print("Volume Aumentado") # Descomente para logar
        except Exception as e:
            print(f"Erro ao aumentar volume: {e}")

def diminuir_volume():
    if pulse:
        try:
            sink = pulse.sink_list()[0]
            pulse.volume_change_all_chans(sink, -0.05)  # -5%
            # print("Volume Diminuído") # Descomente para logar
        except Exception as e:
            print(f"Erro ao diminuir volume: {e}")

def suspender_pc():
    print("PC Suspenso. Executando systemctl suspend...")
    os.system("systemctl suspend")

def diminuir_brilho():
    os.system("brightnessctl set 10%-")
def aumentar_brilho():
    os.system("brightnessctl set +10%")

    #hands pipe config
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Dimensões da tela 
monitors = screeninfo.get_monitors()
if not monitors:
    print("AVISO: Erro ao obter dimensões da tela.")

# Câmera 
cap = cv2.VideoCapture(0) 
if not cap.isOpened():
    print("ERRO: Não foi possível abrir a câmera.")
    exit()

camera_width = 1280
camera_height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

# Gestos

def dedos_levantados(hand_landmarks, h):
    dedos = {}
    # Lógica do Polegar (x < THUMB_IP.x, depende da orientação da mão)
    dedos["Polegar"] = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    
    # Lógica para outros dedos (ponta no eixo Y < dobra PIP no eixo Y)
    dedos["Indicador"] = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    dedos["Medio"] = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    dedos["Anelar"] = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    dedos["Mindinho"] = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y
    return dedos

cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL) 

# Loop

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Corrige o espelhamento da câmera
    frame = cv2.flip(frame, 1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Desenha a mão
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, c = frame.shape

            # Verifica dedos levantados
            dedos = dedos_levantados(hand_landmarks, h)

            # --- LÓGICA DE CONTROLE DE GESTOS ---
            
            # Conta quantos dedos estão levantados (excluindo o polegar para gestos específicos)
            dedos_normais_levantados = [dedos["Indicador"], dedos["Medio"], dedos["Anelar"], dedos["Mindinho"]]
            num_dedos_normais = sum(dedos_normais_levantados)

            # Gesto 2: Só Indicador Levantado -> Aumentar Volume
            elif dedos["Indicador"] and num_dedos_normais == 1 and not dedos["Polegar"]:
                aumentar_volume()

            # Gesto 3: Só Médio Levantado -> Diminuir Volume
            elif dedos["Medio"] and num_dedos_normais == 1 and not dedos["Polegar"]:
                diminuir_volume()

            # Gesto 4: Só Polegar Levantado -> Diminuir Brilho
            elif dedos["Polegar"] and num_dedos_normais == 0:
                diminuir_brilho()

            # Gesto 5: Polegar e Indicador Levantados -> Aumentar Brilho
            elif dedos["Polegar"] and dedos["Indicador"] and num_dedos_normais == 1:
                aumentar_brilho()

            # Exibe o status dos dedos no frame
            for dedo, estado in dedos.items():
                if estado:
                    cv2.putText(frame, f"{dedo} levantado!", (50, 50 + 30*list(dedos.keys()).index(dedo)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        
    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Esc
        break

# Fim
cap.release()
cv2.destroyAllWindows()
