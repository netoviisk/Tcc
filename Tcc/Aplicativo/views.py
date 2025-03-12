from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .forms import UsuarioForm
from .models import Usuarios, Escola


def home(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'Aplicativo/home.html', {'usuarios': usuarios})


def cadastro_usuario(request):
    form = UsuarioForm()

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('sucesso')

    return render(request, 'Aplicativo/cadastro.html', {'form': form})


def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("password")

        usuario = authenticate(request, username=email, password=senha)  # Agora funciona com email

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
    if request.session.get("usuario_tipo") != "administrador":
        return redirect("login")
    return render(request, "Aplicativo/painel/admin.html")


@login_required(login_url='login')
def painel_professor(request):
    if request.session.get("usuario_tipo") != "professor":
        return redirect("login")
    return render(request, "Aplicativo/painel/professor.html")


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


# ======== RECUPERAÇÃO DE SENHA ========
"""
def esqueci_senha(request):
    if request.method == "POST":
        email = request.POST.get("email")
        usuario = Usuarios.objects.filter(usu_email=email).first()

        if usuario:
            nova_senha = Usuarios.objects.make_random_password()
            usuario.set_password(nova_senha)
            usuario.save()

            send_mail(
                "Recuperação de Senha",
                f"Sua nova senha é: {nova_senha}",
                "seu_email@exemplo.com",
                [email],
                fail_silently=False,
            )

            messages.success(request, "Uma nova senha foi enviada para o seu e-mail.")
            return redirect("login")

        messages.error(request, "E-mail não encontrado.")

    return render(request, "Aplicativo/esqueci_senha.html")

def resetar_senha(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = get_object_or_404(Usuarios, pk=uid)

        if not default_token_generator.check_token(usuario, token):
            messages.error(request, "O link de redefinição de senha é inválido.")
            return redirect("login")

    except Exception:
        messages.error(request, "Ocorreu um erro. Tente novamente.")
        return redirect("login")

    if request.method == "POST":
        nova_senha = request.POST.get("password")
        usuario.set_password(nova_senha)
        usuario.save()
        messages.success(request, "Senha redefinida com sucesso!")
        return redirect("login")

    return render(request, "Aplicativo/resetar_senha.html")
"""
