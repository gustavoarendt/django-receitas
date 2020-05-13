from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from receitas.models import Receita

# Create your views here.


def cadastro(request):
    """Cadastra o usuário no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        print(nome, email, password, password2)
        if empty_field(nome):
            messages.error(request, 'Campo Nome não pode ficar em branco')
            return redirect('cadastro')
        if empty_field(email):
            messages.error(request, 'Campo email não pode ficar em branco')
            return redirect('cadastro')
        if password_unmatch(password, password2):
            messages.error(request, 'As senhas precisam ser iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(
            username=nome, email=email, password=password)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    """Realiza o login no sistema"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if empty_field(email) or empty_field(senha):
            messages.error(request, 'Os campos não podem estarem vazios')
            return redirect('login')
        print(email, senha)
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(
                email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
        messages.error(request, "email ou senha incorretos")
    return render(request, 'usuarios/login.html')


def dashboard(request):
    """Autentica o usuário e renderiza o dashboard ou redireciona para a página inicial"""
    if request.user.is_authenticated:
        receitas = Receita.objects.order_by(
            '-date_receita').filter(pessoa=request.user.id)

        dados = {
            'receitas': receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def logout(request):
    """Realiza o logout do usuário"""
    auth.logout(request)
    return redirect('index')


def empty_field(field):
    """Verifica se há campos vazios"""
    return not field.strip()


def password_unmatch(password, password2):
    """Verifica a confirmação de senha está correta"""
    return password != password2
