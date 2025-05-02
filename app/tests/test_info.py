from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

Window.size = (340, 680)

class MainScreen(MDScreen):
    def show_recognized_user(self):
        # Exibe informações fictícias do funcionário reconhecido
        self.clear_widgets()
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)
        layout.add_widget(MDLabel(text="Nome: Letícia Lima", halign="center"))
        layout.add_widget(MDLabel(text="CPF: 123.456.789-00", halign="center"))
        layout.add_widget(MDLabel(text="Reconhecimento realizado com sucesso!", halign="center"))
        self.add_widget(layout)

        # Atribui os valores aos widgets

        self.ids.foto.source = funcionario["foto"]
        self.ids.nome.text = f"Nome: {funcionario['nome']}"
        self.ids.cpf.text = f"CPF: {funcionario['cpf']}"
        self.ids.data_hora.text = f"Data e Hora: {datetime.now().strftime('%d/%m/%Y às %H')
        # Torna o cartão visível

        self.ids.card.opacity = 1

class ScreenManagerApp(ScreenManager):
    def show_recognized_user(self):
        # Chama o método da tela principal
        self.get_screen('main').show_recognized_user()


class MainApp(MDApp):
    def build(self):
        return Builder.load_string("""
ScreenManagerApp:
    MainScreen:
        name: "main"

<MainScreen>:
    MDBoxLayout:
        orientation: "vertical"
        spacing: 20
        padding: 20

    MDCard:
    id: card
    size_hint: None, None
    size: "280dp", "300dp"
    pos_hint: {"center_x": 0.5, "center_y": 0.6}
    opacity: 0
    orientation: "vertical"
    padding: "10dp"
    spacing: "10dp"

    AsyncImage:
        id: foto
        size_hint: (1, 0.5)
        pos_hint: {"center_x": 0.5}

    BoxLayout:
        orientation: "vertical"
        spacing: "10dp"

        MDLabel:
            id: nome
            text: ""
            adaptive_size: True
            theme_text_color: "Secondary"
            size_hint_y: None
            pos_hint: {"center_x": 0.5}
            padding: "4dp", "4dp"

        MDLabel:
            id: cpf
            text: ""
            adaptive_size: True
            theme_text_color: "Secondary"
            size_hint_y: None
            pos_hint: {"center_x": 0.5}
            padding: "4dp", "4dp"

        MDLabel:
            id: data_hora
            text: ""
            adaptive_size: True
            theme_text_color: "Secondary"
            size_hint_y: None
            pos_hint: {"center_x": 0.5}
            padding: "4dp", "4dp"

        MDLabel:
            text: "Clique no botão para reconhecimento"
            halign: "center"
            theme_text_color: "Secondary"

        MDRaisedButton:
            text: "Iniciar Reconhecimento"
            size_hint: None, None
            size: "200dp", "50dp"
            pos_hint: {"center_x": 0.5}
            on_press: root.show_recognized_user()
""")


if __name__ == '__main__':
    MainApp().run()
