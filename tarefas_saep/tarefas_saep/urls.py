from django.contrib import admin
from django.urls import path
from aplicativo import views

urlpatterns = [
    path('', views.home, name='home.html'),
    path('tarefas/listar_tarefas/', views.listar_tarefas, name='listar_tarefas'),
    path('usuarios/listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('tarefas/cadastro_tarefas/', views.cadastro_tarefas, name='cadastro_tarefas'),
    path('tarefas/cadastro_usuarios/', views.cadastro_usuarios, name='cadastro_usuarios'),

    path('tarefas/botao/edita_tarefas/<int:tarefa_id>/', views.edita_tarefas, name='edita_tarefas'),
    path('tarefas/botao/exclui_tarefas/<int:tarefa_id>/', views.exclui_tarefas, name='exclui_tarefas'),
    path('usuarios/botao/edita_usuarios/<int:usu_codigo>/', views.edita_usuarios, name='edita_usuarios'),
    path('usuarios/botao/exclui_usuarios/<int:usu_codigo>/', views.exclui_usuarios, name='exclui_usuarios'),

    path('tarefas/botao/alterar_status/<int:tarefa_id>/<str:novo_status>/', views.alterar_status, name='alterar_status'),
    path('tarefas/botao/listar_status/', views.listar_status, name='listar_status'),
]
