import cv2
import os

class VideoCamera(object):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.video = cv2.VideoCapture(0)

        if not self.video.isOpened():
            print("Erro ao acessar a câmera.")

        self.img_dir = "./tmp"
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)

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
            print("Falha ao capturar o frame.")
            return None

        altura, largura, _ = frame.shape
        centro_x, centro_y = int(largura / 2), int(altura / 2)
        a, b = 140, 180
        x1, y1 = centro_x - a, centro_y - b
        x2, y2 = centro_x + a, centro_y + b
        roi = frame[y1:y2, x1:x2]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        ellipse_color = (0, 255, 0) if len(faces) > 0 else (0, 0, 255)
        cv2.ellipse(frame, (centro_x, centro_y), (a, b), 0, 0, 360, ellipse_color, 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def sample_faces(self, frame):
        if frame is None:
            return None

        frame = cv2.resize(frame, (480, 360))  # Redimensiona para consistência
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50)
        )

        for (x, y, w, h) in faces:
            cropped_face = frame[y:y+h, x:x+w]
            return cropped_face

        return None
