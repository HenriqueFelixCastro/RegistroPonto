import cv2
import os

class VideoCamera(object):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.video = cv2.VideoCapture(0)

        if not self.video.isOpened():
            print("Erro ao acessar a câmera.")

    def __del__(self):
        self.video.release()

    def restart(self):
        self.video.release()
        self.video = cv2.VideoCapture(0)

    def get_camera(self):
        ret, frame = self.video.read()
        if not ret:
            print("Falha ao capturar o frame.")
            return None, None
        return ret, frame

    def detect_face(self):
        ret, frame = self.get_camera()
        if not ret or frame is None:
            print("Falha ao capturar o frame")
            return None

        # Defina a região de interesse (ROI) onde o rosto será detectado

        altura, largura, _ = frame.shape
        centro_x, centro_y = int(largura / 2), int(altura / 2)
        a, b = 140, 180
        x1, y1 = centro_x - a, centro_y - b
        x2, y2 = centro_x + a, centro_y + b
        roi = frame[y1:y2, x1:x2]
        # Converta a ROI em escala de cinza para a detecção de faces
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Define cor do círculo: vermelho (sem rosto) ou verde (com rosto)
        ellipse_color = (0, 255, 0) if len(faces) > 0 else (0, 0, 255)

        # Desenha o círculo principal (verde ou vermelho)
        cv2.ellipse(frame, (centro_x, centro_y), (a, b), 0, 0, 360, ellipse_color, 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
