from google.auth import jwt
from datetime import datetime
from django.conf import settings


class Google:
    """Google class to fetch the user's info and return it"""

    @staticmethod
    def validate(credentials):
        try:
            idinfo = jwt.decode(
                credentials, verify=False
            )  # decodes the credentials recieved from the google

            # Note To Self: Needs cert to be able to perform google verification

            if (
                "https://accounts.google.com" in idinfo["iss"]
                and True == idinfo["email_verified"]
                and "gmail.com" in idinfo["email"]
                and datetime.now().timestamp() - idinfo["iat"]
                < settings.SOCIAL_LOGIN_VALIDITY_PERIOD
            ):  # checks if the issuer of the token is google and the email is verified
                return idinfo

        except:
            return "The token is either invalid or has expired"
