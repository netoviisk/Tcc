from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Aplicativo import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('login/', views.login_usuario, name='login'),
    path("painel/admin/", views.painel_admin, name="painel_admin"),
    path("painel/professor/", views.painel_professor, name="painel_professor"),
    path("logout/", views.logout_usuario, name="logout"),
    path('painel/funcao/registrar_aluno/', views.registrar_aluno, name='registrar_aluno'),
    path('painel/editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('painel/perfil/', views.perfil, name='perfil'),
    path('painel/criar_escola/', views.criar_escola, name='criar_escola'),
    path('painel/buscar_escolas/', views.buscar_escolas, name='buscar_escolas'),
    path('painel/detalhes_escola/<int:id>/', views.detalhes_escola, name='detalhes_escola'),
    path('painel/associar_escola/', views.associar_escola, name='associar_escola'),
    path('painel/funcao/alunos_page/', views.alunos_page, name='alunos_page'),
    path('painel/funcao/salas_page/', views.salas_page, name='salas_page'),
    path('painel/funcao/lista_salas/', views.lista_salas, name='lista_salas'),
    path('painel/funcao/registrar_sala/', views.registrar_sala, name='registrar_sala'),
    path('painel/funcao/lista/', views.lista_matriculas, name='lista_matriculas'),
    path('painel/funcao/professores_lista/', views.professores_lista, name='professores_lista'),


    path('painel/funcao/acao/editar_matricula/<int:id>/', views.editar_turma, name='editar_matricula'),
    path('painel/funcao/acao/excluir_matricula/<int:id>/', views.excluir_turma, name='excluir_matricula'),
    path('painel/funcao/acao/editar_sala/<int:id>/', views.editar_sala, name='editar_sala'),
    path('painel/funcao/acao/excluir_sala/<int:id>/', views.excluir_sala, name='excluir_sala'),


    path('contato/', views.contato, name='contato'),
    path('sobre/', views.sobre, name='sobre'),

    #path("esqueci-senha/", esqueci_senha, name="esqueci_senha"),
    #path("resetar-senha/<uidb64>/<token>/", resetar_senha, name="resetar_senha"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)