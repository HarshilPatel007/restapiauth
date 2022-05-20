from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=150,
        min_length=10,
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        if not username.isalnum():
            msg = _("Username should only contains alphanumeric characters")
            raise serializers.ValidationError(msg)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  # type: ignore
