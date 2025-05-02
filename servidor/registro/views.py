import cv2
import os
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.core.management import call_command
from .forms import FuncionarioForm
from .models import Funcionario, ColetaFaces
from registro.camera import VideoCamera

camera_detection = VideoCamera()  # Instância da câmera

# Geração de frames com detecção facial
def gen_detect_face(camera_detection):
    while True:
        frame = camera_detection.detect_face()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Exibe o streaming da câmera no navegador
def face_detection(request):
    return StreamingHttpResponse(gen_detect_face(camera_detection),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


# Criação de um novo funcionário
def criar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, request.FILES)
        if form.is_valid():
            funcionario = form.save()
            return redirect('criar_coleta_faces', funcionario_id=funcionario.id)
    else:
        form = FuncionarioForm()
    return render(request, 'criar_funcionario.html', {'form': form})


# Função para extrair imagens faciais da câmera
def extract(camera_detection, funcionario_slug):
    amostra = 0
    numeroAmostras = 10
    largura, altura = 220, 220
    file_paths = []

    while amostra < numeroAmostras:
        ret, frame = camera_detection.get_camera()
        crop = camera_detection.sample_faces(frame)

        if crop is not None:
            imagemCinza = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            face = cv2.resize(imagemCinza, (largura, altura))
            file_name_path = f'./tmp/{funcionario_slug}_{amostra + 1}.jpg'
            cv2.imwrite(file_name_path, face)
            file_paths.append(file_name_path)
            amostra += 1
        else:
            print("Face não encontrada")

    camera_detection.restart()
    return file_paths


# Processa a extração de rostos e salva no banco
def face_extract(context, funcionario):
    num_coletas = ColetaFaces.objects.filter(funcionario__slug=funcionario.slug).count()

    if num_coletas >= 10:
        context['erro'] = 'Limite máximo de coletas atingido.'
    else:
        files_paths = extract(camera_detection, funcionario.slug)
        for path in files_paths:
            coleta_face = ColetaFaces.objects.create(funcionario=funcionario)
            coleta_face.image.save(os.path.basename(path), open(path, 'rb'))
            os.remove(path)

        context['file_paths'] = ColetaFaces.objects.filter(funcionario__slug=funcionario.slug)
        context['extracao_ok'] = True

        # (Opcional) Re-treina o modelo automaticamente após coleta
        try:
            call_command('treinamento')
        except Exception as e:
            print(f"Erro ao chamar treinamento: {e}")
            context['erro_treinamento'] = "Falha ao treinar modelo automaticamente."

    return context


# View principal de coleta de faces
def criar_coleta_faces(request, funcionario_id):
    funcionario = Funcionario.objects.get(id=funcionario_id)
    botao_clicado = request.GET.get('clicked', 'False') == 'True'

    context = {
        'funcionario': funcionario,
        'face_detection': face_detection,
        'valor_botao': botao_clicado,
    }

    if botao_clicado:
        print("Cliquei em Extrair Imagens")
        context = face_extract(context, funcionario)

    return render(request, 'criar_coleta_faces.html', context)
