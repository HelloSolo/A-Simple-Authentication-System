import os
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

load_dotenv()


def get_token_for_social_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def register_social_user(provider, email, first_name, last_name):
    User = get_user_model()
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = authenticate(
                email=email, password=os.environ.get("SECRET_KEY")
            )

            return get_token_for_social_user(
                registered_user
            )  # Token should be returned here
        else:
            raise AuthenticationFailed(
                detail="Please continue your login using"
                + filtered_user_by_email[0].auth_provider
            )  # if the user has the same email but using a different provider
    else:
        user_data = {
            "email": email,
            "password": os.environ.get("SECRET_KEY"),
            "first_name": first_name,
            "last_name": last_name,
        }
        user = User.objects.create_user(**user_data)
        user.is_active = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(email=email, password=os.environ.get("SECRET_KEY"))

        return get_token_for_social_user(new_user)
