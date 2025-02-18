from django.shortcuts import render, redirect
from .forms import UsuarioForm
from .models import Usuarios, Escola

def home(request):
    usuarios = Usuarios.objects.all()  # Busca todos os usuários no banco de dados
    return render(request, 'Aplicativo/home.html', {'usuarios': usuarios})

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.usu_tipo = form.cleaned_data['usu_tipo']

            if usuario.usu_tipo == 'professor':
                nome_escola = request.POST.get('esc_name')
                if nome_escola:
                    usuario.save()
                    escola = Escola(esc_name=nome_escola, Usuarios_idUsuarios=usuario)
                    escola.save()

            else:
                usuario.save()

            return redirect('sucesso')  # Redireciona para a URL nomeada 'sucesso'
    else:
        form = UsuarioForm()

    return render(request, 'Aplicativo/cadastro.html', {'form': form})

def sucesso(request):
    return render(request, 'Aplicativo/sucesso.html')

def contato(request):
    return render(request, 'Aplicativo/contato.html')

def sobre(request):
    return render(request, 'Aplicativo/sobre.html')

def login(request):
    return render(request, 'Aplicativo/login.html')