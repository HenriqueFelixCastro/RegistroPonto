from kivymd.app import MDApp
import os
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from datetime import datetime
import cv2
import tempfile
import requests

Window.size = (340, 680)


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Widget de imagem para câmera
        self.image = Image()
        self.add_widget(self.image)

        # Diretório temporário para salvar o modelo
        tmp_dir = "./tmp"
        os.makedirs(tmp_dir, exist_ok=True)

        self.cap = None

        # Classificador e reconhecedor
        self.face_cascade = cv2.CascadeClassifier("./lib/haarcascade_frontalface_default.xml")
        self.reconhecedor = cv2.face.EigenFaceRecognizer_create()

        # Baixar e carregar o modelo
        treinamento = requests.get("http://127.0.0.1:8000/api/treinamento/").json()
        model_url = treinamento[0]['modelo']
        tmp_path = os.path.join(tmp_dir, "modelo.xml")
        with open(tmp_path, "wb") as temp_file:
            temp_file.write(requests.get(model_url).content)
            self.reconhecedor.read(temp_file.name)

    def load_video(self, *args):
        ret, frame = self.cap.read()
        if not ret:
            return

        altura, largura, _ = frame.shape
        centro_x, centro_y = int(largura / 2), int(altura / 2)
        a, b = 140, 180
        x1, y1 = centro_x - a, centro_y - b
        x2, y2 = centro_x + a, centro_y + b

        cv2.ellipse(frame, (centro_x, centro_y), (a, b), 0, 0, 360, (144, 238, 144), 6)

        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
        self.image.texture = texture

        roi = frame[y1:y2, x1:x2]
        imagemCinza = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(imagemCinza, 1.1, 5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            imagemFace = cv2.resize(imagemCinza[y:y+h, x:x+w], (220, 220))
            label, confianca = self.reconhecedor.predict(imagemFace)

            response = requests.get(f"http://127.0.0.1:8000/api/funcionarios/{label}/")
            if response.status_code == 200:
                funcionario = response.json()
                Clock.unschedule(self.load_video)
                self.reset_camera()

                self.manager.get_screen('usuario').mostrar_funcionario(funcionario)
                self.manager.current = 'usuario'
                break

    def open_camera_for_recognition(self):
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            Clock.schedule_interval(self.load_video, 1.0 / 60.0)
            Clock.schedule_once(self.start_face_recognition, 5)
        else:
            print("Erro ao abrir a câmera")

    def reset_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        self.image.texture = None

    def start_face_recognition(self, dt):
        print("Reconhecimento facial iniciado")


class UsuarioScreen(MDScreen):
    funcionario = {}

    def mostrar_funcionario(self, funcionario):
        self.funcionario = funcionario
        self.ids.foto.source = funcionario['foto']
        self.ids.nome.text = f"Nome: {funcionario['nome']}"
        self.ids.cpf.text = f"CPF: {funcionario['cpf']}"
        self.ids.data_hora.text = f"Data e Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        self.ids.card.opacity = 1

    def confirmar(self):
        comprovante = self.manager.get_screen('comprovante')
        comprovante.exibir_comprovante(self.funcionario)
        self.manager.current = 'comprovante'


class ComprovanteScreen(MDScreen):
    def exibir_comprovante(self, funcionario):
        self.ids.foto_comprovante.source = funcionario["foto"]
        self.ids.nome_comprovante.text = f"Nome: {funcionario['nome']}"
        self.ids.cpf_comprovante.text = f"CPF: {funcionario['cpf']}"
        self.ids.data_hora_comprovante.text = f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"


class ScreenManagerApp(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


KV = """
ScreenManagerApp:
    MainScreen:
        name: "main"
    UsuarioScreen:
        name: "usuario"
    ComprovanteScreen:
        name: "comprovante"

<MainScreen>:
    MDBoxLayout:
        orientation: "vertical"
        spacing: "10dp"
        padding: "10dp"

        MDTopAppBar:
            title: "Reconhecimento Facial"
            md_bg_color: 0.1, 0.2, 0.3, 1
            anchor_title: "center"

        Widget:
        MDRaisedButton:
            text: "Iniciar Reconhecimento"
            pos_hint: {"center_x": 0.5}
            on_press: root.open_camera_for_recognition()
        Widget:

<UsuarioScreen>:
    MDBoxLayout:
        orientation: "vertical"
        spacing: "10dp"
        padding: "10dp"

        MDTopAppBar:
            title: "Usuário"
            anchor_title: "center"

        MDCard:
            id: card
            size_hint: None, None
            size: "300dp", "350dp"
            pos_hint: {"center_x": 0.5}
            orientation: "vertical"
            opacity: 0

            AsyncImage:
                id: foto
                size_hint_y: 0.5

            MDLabel:
                id: nome
                halign: "center"
            MDLabel:
                id: cpf
                halign: "center"
            MDLabel:
                id: data_hora
                halign: "center"

        MDRaisedButton:
            text: "Confirmar"
            on_press: root.confirmar()
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            text: "Não sou eu"
            on_press: app.root.current = 'main'
            pos_hint: {"center_x": 0.5}

<ComprovanteScreen>:
    MDBoxLayout:
        orientation: "vertical"
        spacing: "10dp"
        padding: "10dp"

        MDTopAppBar:
            title: "Comprovante"
            anchor_title: "center"

        MDCard:
            size_hint: None, None
            size: "300dp", "350dp"
            pos_hint: {"center_x": 0.5}
            orientation: "vertical"

            AsyncImage:
                id: foto_comprovante
                size_hint_y: 0.5

            MDLabel:
                id: nome_comprovante
                halign: "center"
            MDLabel:
                id: cpf_comprovante
                halign: "center"
            MDLabel:
                id: data_hora_comprovante
                halign: "center"

        MDRaisedButton:
            text: "Fechar"
            on_press: app.root.current = 'main'
            pos_hint: {"center_x": 0.5}
"""

if __name__ == "__main__":
    MainApp().run()
