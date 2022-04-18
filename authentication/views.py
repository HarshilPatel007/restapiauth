from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .models import User
from .utils import Utils
import jwt


# Create your views here.
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data["email"])

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request)
        current_site_url = current_site.domain
        relative_link = reverse("email_verification")
        absolute_url = f"http://{current_site_url}{relative_link}?token={str(token)}"
        email_body = f"Hi {user.get_full_name()},\nUse below link to verify your email.\n\n{absolute_url}"
        token_data = {
            # "domain": absolute_url,
            "email_to": user.email,
            "email_subject": "Please verify your email.",
            "email_body": email_body,
        }

        Utils.send_email(token_data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get("token")
        try:
            decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS512"])
            user = User.objects.get(id=decode_token["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {
                    "account_verification": "Account Successfully Verified",
                },
                status=status.HTTP_200_OK,
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {
                    "account_verification": "Account Is Not Verified (Verification Token Expired)",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {
                    "account_verification": "Account Is Not Verified (Invalid Verification Token)",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
