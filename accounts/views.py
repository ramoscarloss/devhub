from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):

    if request.method == 'POST': #Se o pagina do registro der um POST(enviar um formulario de registro)
        username = request.POST.get("username")#Variavel Username, Email e Password é a que foi mandada pela request la do site
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            return redirect("/register")
        User.objects.create_user(username,email,password)#Cria um usuario no sistema auth do django com os dados que recebemos e identificamos
        return redirect("/login")#Redireciona pra pagina de login

    return render(request, "accounts/register.html")#Renderiza a pagina de registro

def login_view(request):

    if request.method == 'POST': #Se o pagina do registro der um POST(enviar um formulario de login)
        username_login = request.POST.get("username")#Variavel Username, Email e Password é a que foi mandada pela request la do site
        password_login = request.POST.get("password")
        user_view = authenticate(request,username=username_login,password=password_login)#Verifica se a autenticação esta correta
        if user_view is not None:
            login(request, user_view)#Loga na sessão
            return redirect("/feed")
        else:
            return redirect("/login")



    return render(request, "accounts/login.html")#Renderiza a pagina de Login

def logout_view(request):
    logout(request)
    return redirect("/")