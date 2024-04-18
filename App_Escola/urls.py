from django.urls import path, include
from . import views

urlpatterns = [
    path ('', views.abre_index, name='abre_index'),
    path ('enviar_login', views.enviar_login, name='enviar_login'),
    path ('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro'),

    path ('Cons_Turma_Lista', views.enviar_login, name='Cons_Turma_Lista'),
    path ('Cad_Turmas/<int:id_professor>', views.cad_turmas, name='Cad_Turmas'),
    path ('salvar_turma', views.salvar_turma_nova, name='salvar_turma_nova'),
    path ('lista_turma/<int:id_professor>', views.lista_turma, name='lista_turma'),

    path ('Cons_Atividade_Lista', views.enviar_login, name='Cons_Atividade_Lista'),
    path ('Cad_Atividade/<int:id_turma>', views.cad_atividade, name='Cad_Atividade'),
    path ('salvar_atividade', views.salvar_atividade_nova, name='salvar_atividade_nova'),
    path ('lista_atividade/<int:id_turma>', views.lista_atividade, name='lista_atividade'),
]


