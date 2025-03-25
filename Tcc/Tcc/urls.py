"""
URL configuration for Tcc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Aplicativo import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('login/', views.login_usuario, name='login'),
    path("painel/admin/", views.painel_admin, name="painel_admin"),
    path("painel/professor/", views.painel_professor, name="painel_professor"),
    path("logout/", views.logout_usuario, name="logout"),
    path('painel/registrar-aluno/', views.registrar_aluno, name='registrar_aluno'),
    path('painel/listar/', views.listar, name='listar'),
    path('painel/perfil/', views.perfil_usuario, name='perfil'),
    path('painel/associar-escola/', views.associar_escola, name='associar_escola'),
    path('painel/criar_sala/', views.criar_sala, name='criar_sala'),
    path('painel/editar_sala/', views.editar_sala, name='editar_sala'),
    path('painel/buscar_escolas/', views.buscar_escolas, name='buscar_escolas'),
    path('painel/detalhes_escola/<int:id>/', views.detalhes_escola, name='detalhes_escola'),
    #path('painel/verificar/', views.verificar_escola, name='verificar'),

    path('sucesso/', views.sucesso, name='sucesso'),
    path('contato/', views.contato, name='contato'),
    path('sobre/', views.sobre, name='sobre'),

    #path("esqueci-senha/", esqueci_senha, name="esqueci_senha"),
    #path("resetar-senha/<uidb64>/<token>/", resetar_senha, name="resetar_senha"),
]
