import facebook


class Facebook:
    """
    Facebook class to fetch user info and return it
    """

    @staticmethod
    def validate(credentials):
        """
        Validates queries to fetch the user info and returns it
        """

        try:
            graph = facebook.GraphAPI(access_token=credentials)
            profile = graph.request("/me?fields=name,email")
            return profile
        except:
            return "The token is invalid or expired."
