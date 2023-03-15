from rest_framework.response import Response
from djoser.views import UserViewSet as BaseUserViewset
from rest_framework import status


# Create your views here.
class UserViewset(BaseUserViewset):
    """
    User Account Activation, making the activation action(method)
    accept post request.
    """

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        # this line is the only change from the base implementation.
        kwargs["data"] = {"uid": self.kwargs["uid"], "token": self.kwargs["token"]}

        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response("Account activation successful", status=status.HTTP_200_OK)
