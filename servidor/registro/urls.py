from django.urls import path
from registro.views import criar_funcionario, criar_coleta_faces
from .views import face_detection  # Adiciona esta linha para importar a função

urlpatterns = [
    path('', criar_funcionario, name='criar_funcionario'),
    path('criar_coleta_faces/<int:funcionario_id>/', criar_coleta_faces, name='criar_coleta_faces'),
    path('face_detection/', face_detection, name='face_detection'),
]
