from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(
        template_name="accounts/login.html", name="login",
        redirect_authenticated_user=True
    ), name="login"),
    path("logout/", views.LogoutView.as_view(
        template_name="accounts/logged_out.html",
    ), name="logout"),
]