from django.urls import path
from .views import LoginView, RegisterView, VerifyEmail


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("email_verification/", VerifyEmail.as_view(), name="email_verification"),
]
