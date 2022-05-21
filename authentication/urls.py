from django.urls import path
from .views import LoginView, RegisterView, VerifyEmail, ResendVerificationLinkView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("email_verification/", VerifyEmail.as_view(), name="email_verification"),
    path("resend_email_verification_link/", ResendVerificationLinkView.as_view(), name="resend_email_verification_link"),
]
