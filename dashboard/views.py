from django.shortcuts import render

# Create your views here.


def sign_up(request):
    return render(request, "dashboard/auth/sign-up.html")


def login_view(request):
    return render(request, "dashboard/auth/login.html")


def reset_password(request):
    return render(request, "dashboard/auth/reset-password.html")


def reset_password_confirm(request, uid, token):
    return render(request, "dashboard/auth/reset-password-confirm.html")


def home(request):
    return render(request, template_name="dashboard/core/home.html")
