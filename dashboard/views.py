from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User, Transaction, Proof
from django.db.models import Sum

# Create your views here.


def sign_up(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        agree = request.POST.get("agree")

        if not agree:
            messages.error(request, "Please agree to terms and conditions")
            return redirect("sign-up")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("sign-up")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("sign-up")
        user = User.objects.create_user(
            email=email, first_name=first_name, last_name=last_name, password=password1
        )
        user.save()
        messages.success(request, "Account created successfully")
        return redirect("login")
    return render(request, "dashboard/auth/sign-up.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard_home")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")
    return render(request, "dashboard/auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def reset_password(request):
    return render(request, "dashboard/auth/reset-password.html")


def reset_password_confirm(request, uid, token):
    return render(request, "dashboard/auth/reset-password-confirm.html")


@login_required(redirect_field_name="login")
def home(request):
    total_deposits = (
        Transaction.objects.filter(user=request.user, type="deposit")
        .aggregate(total_amount=Sum("amount"))
        .get("total_amount")
        or 0
    )

    total_withdraw = (
        Transaction.objects.filter(user=request.user, type="withdraw")
        .aggregate(total_amount=Sum("amount"))
        .get("total_amount")
        or 0
    )

    context = {"total_deposits": total_deposits, "total_withdraw": total_withdraw}

    return render(request, template_name="dashboard/core/home.html", context=context)


@login_required(redirect_field_name="login")
def deposit(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        asset = request.POST.get("asset")
        transaction = Transaction.objects.create(
            type="deposit",
            user=request.user,
            amount=float(amount),
            asset=asset,
        )
        transaction.save()
        return redirect("confirm-deposit")
    return render(request, template_name="dashboard/core/deposit.html")


@login_required(redirect_field_name="login")
def withdraw(request):
    return render(request, template_name="dashboard/core/withdraw.html")


@login_required(redirect_field_name="login")
def investment(request):
    return render(request, template_name="dashboard/core/investment.html")


@login_required(redirect_field_name="login")
def investment_plan(request):
    return render(request, template_name="dashboard/core/investment-plan.html")


@login_required(redirect_field_name="login")
def transactions(request):
    return render(request, template_name="dashboard/core/transactions.html")


@login_required(redirect_field_name="login")
def confirm_deposit(request):
    transaction = (
        Transaction.objects.filter(user=request.user).order_by("-created_at").first()
    )
    if request.method == "POST":
        file = request.FILES.get("file")
        proof = Proof.objects.create(transaction=transaction, file=file)
        proof.save()
        messages.success(
            request, "Deposit succssfull!! We will verify your payment soon"
        )
        return redirect("dashboard_home")
    return render(
        request,
        template_name="dashboard/core/confirm-deposit.html",
        context={"transaction": transaction},
    )
