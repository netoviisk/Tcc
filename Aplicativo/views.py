from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .forms import UsuarioForm, PerfilForm, MatriculaForm, SalaForm
from .models import Usuarios, Escola, Turma, Professor, Sala
import random
import string


def home(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'Aplicativo/home.html', {'usuarios': usuarios})


def cadastro_usuario(request):
    form = UsuarioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'Aplicativo/cadastro.html', {'form': form})


def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("password")
        usuario = authenticate(request, username=email, password=senha)

        if usuario:
            login(request, usuario)
            request.session["usuario_id"] = usuario.id
            request.session["usuario_tipo"] = usuario.usu_tipo

            if usuario.usu_tipo == "professor":
                return redirect("painel_professor")
            elif usuario.usu_tipo == "administrador":
                return redirect("painel_admin")
        else:
            messages.error(request, "E-mail ou senha incorretos.")

    return render(request, "Aplicativo/login.html")


def editar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        imagem_capa = request.FILES.get('imagem_capa')
        imagem_perfil = request.FILES.get('imagem_perfil')
        usu_home = request.POST.get('usu_home')
        usu_email = request.POST.get('usu_email')

        if imagem_capa:
            usuario.imagem_capa = imagem_capa
        if imagem_perfil:
            usuario.imagem_perfil = imagem_perfil

        usuario.usu_home = usu_home
        usuario.usu_email = usu_email
        usuario.save()

        return redirect('perfil')  # <- Troque pelo nome correto da sua URL

    return render(request, 'Aplicativo/painel/editar_perfil.html', {'usuario': usuario})



def logout_usuario(request):
    logout(request)
    return redirect("login")


def contato(request):
    return render(request, 'Aplicativo/contato.html')


def sobre(request):
    return render(request, 'Aplicativo/sobre.html')




@login_required(login_url='login')
def painel_professor(request):
    if request.session.get("usuario_tipo") != "professor":
        return redirect("login")

    usuario = request.user
    escolas = usuario.escolas.all()

    return render(request, "Aplicativo/painel/professor.html", {
        "usuario": usuario,
        "escolas": escolas
    })


@login_required
def associar_escola(request):
    usuario = request.user

    if request.method == "POST":
        escola_id = request.POST.get("escola")
        escola = get_object_or_404(Escola, id=escola_id)

        if escola not in usuario.escolas.all():
            usuario.escolas.add(escola)
            return JsonResponse({"status": "success", "message": "Instituição vinculada com sucesso!"})
        return JsonResponse({"status": "info", "message": "Você já está vinculado a essa instituição."})

    escolas = Escola.objects.all()
    return render(request, "Aplicativo/painel/associar_escola.html", {
        "escolas": escolas,
        "usuario": usuario
    })


@login_required
def perfil(request):
    return render(request, 'Aplicativo/painel/perfil.html', {
        'usuario': request.user
    })


@login_required
def editar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        imagem_capa = request.FILES.get('imagem_capa')
        imagem_perfil = request.FILES.get('imagem_perfil')
        usu_home = request.POST.get('usu_home')
        usu_email = request.POST.get('usu_email')

        if imagem_capa:
            usuario.imagem_capa = imagem_capa
        if imagem_perfil:
            usuario.imagem_perfil = imagem_perfil

        usuario.usu_home = usu_home
        usuario.usu_email = usu_email
        usuario.save()

        return redirect('perfil')

    return render(request, 'Aplicativo/painel/editar_perfil.html', {
        'usuario': usuario
    })


@login_required
def criar_escola(request):
    usuario = request.user
    if request.method == 'POST':
        esc_name = request.POST.get('esc_name')
        esc_desc = request.POST.get('esc_desc')
        escola_id = request.POST.get('escola_id')

        if esc_name and esc_desc:
            try:
                escola = Escola.objects.create(esc_name=esc_name, esc_desc=esc_desc)
                return JsonResponse({'status': 'success', 'message': 'Escola registrada com sucesso!'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Erro ao registrar a escola: {str(e)}'})

        if escola_id:
            escola = get_object_or_404(Escola, id=escola_id)
            request.user.escolas.add(escola)
            return JsonResponse({'status': 'success', 'message': 'Escola associada com sucesso!'})

    escolas = Escola.objects.all()
    return render(request, 'Aplicativo/painel/criar_escola.html', {
        'escolas': escolas,
        'usuario': usuario
    })


@login_required
def buscar_escolas(request):
    usuario = request.user
    query = request.GET.get('q', '')
    escolas = Escola.objects.filter(esc_name__icontains=query) if query else Escola.objects.all()
    return render(request, 'Aplicativo/painel/professor.html', {
        'escolas': escolas,
        'usuario': usuario
    })


@login_required
def detalhes_escola(request, id):
    escola = get_object_or_404(Escola, id=id)
    return render(request, 'Aplicativo/painel/detalhes_escola.html', {
        'escola': escola,
        'usuario': request.user
    })


@login_required
def alunos_page(request):
    return render(request, 'Aplicativo/painel/funcao/alunos_page.html', {
        'usuario': request.user
    })


@login_required
def registrar_aluno(request):
    usuario = request.user
    escola = usuario.escolas.first()

    if request.method == 'POST':
        nome = request.POST.get('nome')
        matricula = request.POST.get('matricula')
        sala_id = request.POST.get('sala')

        if not all([nome, matricula, sala_id]):
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect('registrar_aluno')

        sala = get_object_or_404(Sala, id=sala_id, escola=escola)

        Turma.objects.create(
            tur_home_aluno=nome,
            tur_matricula=matricula,
            tur_presenca='',
            sala=sala
        )
        messages.success(request, "Aluno registrado com sucesso.")
        return redirect('lista_matriculas')

    salas = Sala.objects.filter(escola=escola)
    return render(request, 'Aplicativo/painel/funcao/registrar_aluno.html', {
        'salas': salas,
        'usuario': usuario
    })


@login_required
def lista_matriculas(request):
    turmas = Turma.objects.all()
    return render(request, 'Aplicativo/painel/funcao/lista_matriculas.html', {
        'turmas': turmas,
        'usuario': request.user
    })


@login_required
def professores_lista(request):
    professores = Professor.objects.select_related('usuario').prefetch_related('usuario__escolas').all()
    return render(request, 'Aplicativo/painel/funcao/professores_lista.html', {
        'professores': professores,
        'usuario': request.user
    })


@login_required
def salas_page(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'Aplicativo/painel/funcao/salas_page.html', {
        'usuarios': usuarios,
        'usuario': request.user
    })


@login_required
def registrar_sala(request):
    usuario = request.user
    escola = usuario.escolas.first()

    if not escola:
        messages.error(request, "Você não está associado a nenhuma escola.")
        return redirect('lista_salas')

    form = SalaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        nova_sala = form.save(commit=False)
        nova_sala.escola = escola
        nova_sala.save()
        messages.success(request, "Sala cadastrada com sucesso.")
        return redirect('lista_salas')

    return render(request, 'Aplicativo/painel/funcao/registrar_sala.html', {
        'form': form,
        'usuario': usuario
    })


@login_required
def lista_salas(request):
    salas = Sala.objects.select_related('escola').all()
    return render(request, 'Aplicativo/painel/funcao/lista_salas.html', {
        'salas': salas,
        'usuario': request.user
    })


@login_required
def editar_turma(request, id):
    matricula = get_object_or_404(Turma, id=id)
    form = MatriculaForm(request.POST or None, instance=matricula)
    salas = Sala.objects.all()

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_matriculas')

    return render(request, 'Aplicativo/painel/funcao/acao/editar_matricula.html', {
        'form': form,
        'matricula': matricula,
        'salas': salas,
        'usuario': request.user
    })


@login_required
def excluir_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == 'POST':
        turma.delete()
        return redirect('lista_matriculas')
    return render(request, 'Aplicativo/painel/funcao/acao/excluir_matricula.html', {
        'turma': turma,
        'usuario': request.user
    })


@login_required
def editar_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    form = SalaForm(request.POST or None, instance=sala)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_salas')

    return render(request, 'Aplicativo/painel/funcao/acao/editar_sala.html', {
        'form': form,
        'sala': sala,
        'usuario': request.user
    })


@login_required
def excluir_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        sala.delete()
        return redirect('lista_salas')
    return render(request, 'Aplicativo/painel/funcao/acao/excluir_sala.html', {
        'sala': sala,
        'usuario': request.user
    })

@login_required(login_url='login')
def painel_admin(request):
    usuario = request.user
    if usuario.usu_tipo == "administrador" and not usuario.escolas.exists():
        return redirect('associar_escola')

    escola = Escola.objects.filter(usuarios_associados=usuario).first()

    return render(request, 'Aplicativo/painel/admin.html', {
        'usuario': usuario,
        'escola': escola,
        'sem_escola': not escola
    })


