from django.conf import settings
from rest_framework import serializers
from . import google
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed


class GoogleAuthSerializer(serializers.Serializer):
    credential = serializers.CharField()

    def validate_credential(self, credentials):
        user_data = google.Google.validate(credentials)  # returns user info from google

        try:
            user_data["sub"]
        except:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again"
            )
        if (
            user_data["aud"] != settings.CLIENTID
        ):  # check if the credential was generated using our app
            raise AuthenticationFailed(
                "oops, invalid token or your token cannot authorized by this app "
            )

        email = user_data["email"]
        first_name = user_data["given_name"]
        last_name = user_data["family_name"]
        auth_provider = "google"

        return register_social_user(
            provider=auth_provider,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
