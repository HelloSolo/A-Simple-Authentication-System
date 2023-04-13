from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import GoogleAuthSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class GoogleAuthView(GenericAPIView):
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["credential"]
        return Response(data, status=status.HTTP_200_OK)
