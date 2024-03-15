from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User, Transaction, Proof, Investment
from django.db.models import Sum
from django.conf import settings

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
    return render(
        request,
        template_name="dashboard/core/deposit.html",
        context={"address": settings.WALLETS},
    )


@login_required(redirect_field_name="login")
def withdraw(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        asset = request.POST.get("asset")

        if amount > request.user.wallet_balance:
            messages.error(request, "Insuficient balnace")
            return redirect("withdraw")
        if request.user.btc_wallet == None:
            return redirect("addWallet")
        transaction = Transaction.objects.create(
            type="withdraw", asset=asset, amount=amount, user=request.user
        )
        transaction.save()
        messages.success(
            request,
            f"Your withdrawal of ${amount} worth of asset {asset} will be transfered to you soon.",
        )
        return redirect("withdraw")
    return render(request, template_name="dashboard/core/withdraw.html")


@login_required(redirect_field_name="login")
def investment(request):
    investments = Investment.objects.filter(user=request.user)
    return render(
        request,
        template_name="dashboard/core/investment.html",
        context={"investments": investments},
    )


@login_required(redirect_field_name="login")
def investment_plan(request):
    plans = [
        {
            "key": "basic",
            "name": "Basic Plan",
            "minimum": 500,
            "maximum": 999,
            "roi": 20,
            "duration": 14,
        },
        {
            "key": "standard",
            "name": "Standard Plan",
            "minimum": 1000,
            "maximum": 4999,
            "roi": 20,
            "duration": 14,
        },
        {
            "key": "professional",
            "name": "Professional Plan",
            "minimum": 5000,
            "maximum": 9990,
            "roi": 20,
            "duration": 14,
        },
        {
            "key": "expert",
            "name": "Expert Plan",
            "minimum": 10000,
            "maximum": 35999,
            "roi": 20,
            "duration": 14,
        },
        {
            "key": "executive",
            "name": "Executive Plan",
            "minimum": 50000,
            "maximum": 100000,
            "roi": 20,
            "duration": 14,
        },
    ]
    if request.method == "POST":
        plan = request.POST.get("plan")
        asset = request.POST.get("asset")
        amount = float(request.POST.get("amount"))
        if amount > request.user.wallet_balance:
            return redirect("deposit")
        investment = Investment.objects.create(
            user=request.user, plan=plan, amount=amount, asset=asset
        )
        investment.save()
        return redirect("investment")
    return render(
        request,
        template_name="dashboard/core/investment-plan.html",
        context={"plans": plans},
    )


@login_required(redirect_field_name="login")
def transactions(request):
    deposits = Transaction.objects.filter(user=request.user, type="deposit")
    withdrawals = Transaction.objects.filter(user=request.user, type="withdraw")
    return render(
        request,
        template_name="dashboard/core/transactions.html",
        context={"deposits": deposits, "withdrawals": withdrawals},
    )


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


@login_required(redirect_field_name="login")
def add_wallet(request):
    if request.method == "POST":
        btc = request.POST.get("btc")
        eth = request.POST.get("eth")
        usdt = request.POST.get("usdt")
        ltc = request.POST.get("ltc")
        usdc = request.POST.get("usdc")
        doge = request.POST.get("doge")
        user = request.user
        user.btc_wallet = btc
        user.eth_wallet = eth
        user.usdt_wallet = usdt
        user.ltc_wallet = ltc
        user.usdc_wallet = usdc
        user.doge_wallet = doge
        user.save()
        messages.success(request, "Wallet Address Updated")
        return redirect("addWallet")
    return render(request, "dashboard/core/add_wallet.html")
