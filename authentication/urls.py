from django.urls import path

from .views import (
    LoginView,
    LogoutFromAllDevicesView,
    LogoutView,
    RegisterView,
    ResendVerificationLinkView,
    VerifyEmail,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "logout_from_all_devices/",
        LogoutFromAllDevicesView.as_view(),
        name="logout_from_all_devices",
    ),
    path("email_verification/", VerifyEmail.as_view(), name="email_verification"),
    path(
        "resend_email_verification_link/",
        ResendVerificationLinkView.as_view(),
        name="resend_email_verification_link",
    ),
]
