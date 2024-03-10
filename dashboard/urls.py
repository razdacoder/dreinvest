from django.urls import path
from dashboard import views

urlpatterns = [
    path("auth/sign-up/", views.sign_up, name="sign-up"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/logout/", views.logout_view, name="logout"),
    path("auth/reset_password/", views.reset_password, name="reset_password"),
    path(
        "auth/reset_password_confirm/<str:uid>/<str:token>/",
        views.reset_password_confirm,
        name="reset_password_confirm",
    ),
    path("", views.home, name="dashboard_home"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("investment/", views.investment, name="investment"),
    path("investment-plan/", views.investment_plan, name="investment_plan"),
    path("transactions/", views.transactions, name="transactions"),
]
