from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return redirect("register")

        User.objects.create_user(username, email, password)
        return redirect("login")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username_login = request.POST.get("username")
        password_login = request.POST.get("password")
        user_view = authenticate(request, username=username_login, password=password_login)

        if user_view is not None:
            login(request, user_view)
            return redirect("feed")
        messages.add_message(request, messages.ERROR, "Login errado ou inexistente" )

        return redirect("login")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("ini")
