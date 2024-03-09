from django.urls import path
from dashboard import views

urlpatterns = [
    path("auth/sign-up/", views.sign_up, name="sign-up"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/reset_password/", views.reset_password, name="reset_password"),
    path(
        "auth/reset_password_confirm/<str:uid>/<str:token>/",
        views.reset_password_confirm,
        name="reset_password_confirm",
    ),
    path("", views.home, name="dashboard_home"),
]
