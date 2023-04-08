from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """Google class to fetch the user's info and return it"""

    @staticmethod  # creates a method that is bound to the class rather than an object of the class
    def validate(auth_token):
        """
        validate method queries the google oauth2 api to fetch the user's info
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request()
            )  # to verify if the auth_token is issued by google

            if (
                "account.google.com" in idinfo["iss"]
            ):  # checks if the issuer of the token is google
                return idinfo
        except:
            return "The token is either invalid or has expired"
