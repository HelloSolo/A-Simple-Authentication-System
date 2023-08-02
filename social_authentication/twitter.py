import twitter
from django.conf import settings
from rest_framework import serializers


class TwitterAuthTokenVerification:
    @staticmethod
    def validate_twitter_auth_tokens(access_token_key, access_token_secret):
        """
        validate_twitter_auth_tokens methods returns a twitter
        user profile info
        """

        consumer_key = settings.TWITTER_ACCESS_TOKEN
        consumer_secret = settings.TWITTER_TOKEN_SECRET

        try:
            api = twitter.Api(
                consumer_key, consumer_secret, access_token_key, access_token_secret
            )
            user_profile_info = api.VerifyCredentials(include_email=True)
            return user_profile_info.__dict__
        except:
            raise serializers.ValidationError(
                {"token": ["The tokens are invalid or expired"]}
            )
