from django.conf import settings
from rest_framework import serializers
from . import google
from . import facebook
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed


class FacebookAuthSerializer(serializers.Serializer):
    credential = serializers.CharField()

    def validate_credential(self, credential):
        user_data = facebook.Facebook.validate(credential)

        try:
            email = user_data["email"]
            first_name = user_data["name"].split(" ")[0]
            last_name = user_data["name"].split(" ")[1]
            provider = "facebook"
            return register_social_user(provider, email, first_name, last_name)
        except:
            raise serializers.ValidationError(
                "This token is invalid or expired, please login again"
            )

    pass


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
