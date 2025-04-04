from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import UsuarioForm, PerfilForm, MatriculaForm
from .models import Usuarios, Escola, Turma, Professor, Sala
from django.contrib.auth import logout
from django.http import JsonResponse


def home(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'Aplicativo/home.html', {'usuarios': usuarios})


def cadastro_usuario(request):
    form = UsuarioForm()

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('login')

    return render(request, 'Aplicativo/cadastro.html', {'form': form})


def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("password")

        usuario = authenticate(request, username=email, password=senha)

        if usuario is not None:
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


@login_required(login_url='login')
def painel_admin(request):
    usuario = request.user
    if usuario.usu_tipo == "administrador" and not usuario.escolas.exists():
        return redirect('associar_escola')

    escola = Escola.objects.filter(usuarios_associados=usuario).first()

    if not escola:
        return render(request, 'Aplicativo/painel/admin.html', {
            'usuario': usuario,
            'escola': None,
            'sem_escola': True
        })

    return render(request, 'Aplicativo/painel/admin.html', {
        'usuario': usuario,
        'escola': escola,
        'sem_escola': False
    })


@login_required(login_url='login')
def listar(request):
    turmas = Turma.objects.all()
    return render(request, 'Aplicativo/painel/funcao/salas_page.html', {'turmas': turmas})


@login_required(login_url='login')
def painel_professor(request):
    if request.session.get("usuario_tipo") != "professor":
        return redirect("login")

    usuario = request.user
    escolas = usuario.escolas.all()

    if not escolas:
        escolas = []

    context = {
        "usuario": usuario,
        "escolas": escolas,
    }

    return render(request, "Aplicativo/painel/professor.html", context)

@login_required
def associar_escola(request):
    usuario = request.user  # Obtém o usuário logado

    if request.method == "POST":
        escola_id = request.POST.get("escola")
        escola = get_object_or_404(Escola, id=escola_id)

        # Verifica se o usuário já está vinculado a essa escola
        if escola not in usuario.escolas.all():
            usuario.escolas.add(escola)
            return JsonResponse({"status": "success", "message": "Instituição vinculada com sucesso!"})
        else:
            return JsonResponse({"status": "info", "message": "Você já está vinculado a essa instituição."})

    escolas = Escola.objects.all()
    return render(request, "Aplicativo/painel/associar_escola.html", {"escolas": escolas})

@login_required
def perfil(request):
    usuario = request.user

    context = {
        'usuario': usuario,
    }

    return render(request, 'Aplicativo/painel/perfil.html', context)

@login_required
def editar_perfil(request):
    usuario = request.user  # Assume que o usuário está logado
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redireciona para a página de perfil
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'Aplicativo/painel/editar_perfil.html', {'usuario': usuario, 'form': form})

@login_required
def criar_escola(request):
    if request.method == 'POST':
        if 'esc_name' in request.POST and 'esc_desc' in request.POST:
            esc_name = request.POST.get('esc_name')
            esc_desc = request.POST.get('esc_desc')

            try:
                escola = Escola.objects.create(
                    esc_name=esc_name,
                    esc_desc=esc_desc
                )
                return JsonResponse({'status': 'success', 'message': 'Escola registrada com sucesso!'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Erro ao registrar a escola: {str(e)}'})

        elif 'escola_id' in request.POST:
            escola_id = request.POST.get('escola_id')
            escola = Escola.objects.get(id=escola_id)
            request.user.escola = escola
            request.user.save()

            return JsonResponse({'status': 'success', 'message': 'Escola associada com sucesso!'})

    escolas = Escola.objects.all()

    return render(request, 'Aplicativo/painel/criar_escola.html', {'escolas': escolas})


def logout_usuario(request):
    logout(request)
    return redirect("login")


def sucesso(request):
    return render(request, 'Aplicativo/sucesso.html')


def contato(request):
    return render(request, 'Aplicativo/contato.html')


def sobre(request):
    return render(request, 'Aplicativo/sobre.html')


def teste(request):
    return render(request, 'Aplicativo/teste.html')

def criar_sala(request):
    return render(request, 'Aplicativo/painel/criar_sala.html')

def editar_sala(request):
    return render(request, 'Aplicativo/painel/editar_sala.html')

def buscar_escolas(request):
    query = request.GET.get('q', '')
    if query:
        escolas = Escola.objects.filter(esc_name__icontains=query)
    else:
        escolas = Escola.objects.all()
    return render(request, 'Aplicativo/painel/professor.html', {'escolas': escolas})


def detalhes_escola(request, id):
    # Usa o get_object_or_404 para garantir que, se a escola não existir, um erro 404 será mostrado
    escola = get_object_or_404(Escola, id=id)

    # Retorna a resposta renderizada com os detalhes da escola
    return render(request, 'Aplicativo/painel/detalhes_escola.html', {'escola': escola})

def alunos_page(request):
    return render(request, 'Aplicativo/painel/funcao/alunos_page.html')

def registrar_aluno(request):
    turmas = Turma.objects.all()
    salas = Sala.objects.all()

    if request.method == "POST":
        form = MatriculaForm(request.POST)
        sala_id = request.POST.get("sala")

        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.sala = Sala.objects.get(id=sala_id)  # Associa a sala ao aluno
            matricula.save()
            return redirect('alunos_page')

    else:
        form = MatriculaForm()

    return render(request, 'Aplicativo/painel/funcao/registrar_aluno.html', {'form': form, 'turmas': turmas, 'salas': salas})

def lista_matriculas(request):
    turmas = Turma.objects.all()
    return render(request, 'Aplicativo/painel/funcao/lista_matriculas.html', {'turmas': turmas})


def professores_lista(request):
    professores = Professor.objects.select_related('usuario').prefetch_related('usuario__escolas').all()

    return render(request, 'Aplicativo/painel/funcao/professores_lista.html', {'professores': professores})

def salas_page(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'Aplicativo/painel/funcao/salas_page.html', {'usuarios': usuarios})

def registrar_sala(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'Aplicativo/painel/funcao/salas_page.html', {'usuarios': usuarios})

def lista_salas(request):
    salas = Sala.objects.select_related('escola').all()
    return render(request, 'Aplicativo/painel/funcao/lista_salas.html', {'salas': salas})


"""
@login_required
def verificar_escola(request):
    if request.user.is_authenticated:
        try:
            usuario = Usuarios.objects.get(usu_email=request.user.email)
            if usuario.escolas.exists():
                return redirect('admin')
            else:
                return redirect('admin_sem')
        except Usuarios.DoesNotExist:
            return redirect('pagina_de_erro')

"""