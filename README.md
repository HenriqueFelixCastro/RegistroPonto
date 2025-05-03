
# RegistroPonto

**RegistroPonto** é um sistema de registro de ponto que utiliza reconhecimento facial para autenticar e registrar a presença de usuários. Desenvolvido com o objetivo de modernizar e automatizar o controle de frequência em ambientes corporativos e educacionais.

## 🚀 Funcionalidades

- Captura de imagem facial do usuário no momento do registro de ponto.
- Processamento e reconhecimento facial para autenticação segura.
- Armazenamento dos registros de entrada e saída com marcação de data e hora.
- Interface intuitiva para usuários realizarem o registro de ponto.
- Painel administrativo para visualização e gerenciamento dos registros.

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal para o desenvolvimento.
- **Django**: Framework web robusto usado para construção do backend e painel administrativo.
- **OpenCV**: Biblioteca de visão computacional para captura e processamento de imagens.
- **Dlib**: Biblioteca para detecção e reconhecimento facial.
- **SQLite**: Banco de dados leve para armazenamento local dos registros.

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/HenriqueFelixCastro/RegistroPonto.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd RegistroPonto
   ```

3. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate   # Para Windows
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Execute as migrações do banco de dados:
   ```bash
   python manage.py migrate
   ```

6. Crie um superusuário para acessar o admin:
   ```bash
   python manage.py createsuperuser
   ```

7. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

## 📷 Captura de Imagem

Certifique-se de que o dispositivo possui uma câmera funcional. O sistema utilizará a câmera padrão para capturar as imagens faciais dos usuários durante o registro de ponto.


## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests. Para maiores informações, consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 📬 Contato

Para dúvidas ou sugestões, entre em contato:

- **Henrique Felix Castro**
- Email: [henrique.felix@example.com](mailto:henrique.felix.castro@hotmail.com)
- GitHub: [@HenriqueFelixCastro](https://github.com/HenriqueFelixCastro)
