from django.shortcuts import render, redirect
from forms import UsuarioForm
from Tcc.models import Usuarios, Escola

def home(request):
    return render(request, 'html/home.html')

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = Usuarios(
                usu_home=form.cleaned_data['usu_home'],
                usu_email=form.cleaned_data['usu_email'],
                usu_senha=form.cleaned_data['usu_senha'],
                usu_tipo=form.cleaned_data['tipo_usuario']
            )
            usuario.save()

            if form.cleaned_data['tipo_usuario'] == 'professor':
                escola = Escola(
                    esc_name=form.cleaned_data['esc_name'],
                    Usuarios_idUsuarios=usuario
                )
                escola.save()

            return redirect('sucesso')
    else:
        form = UsuarioForm()

    return render(request, 'cadastro.html', {'form': form})