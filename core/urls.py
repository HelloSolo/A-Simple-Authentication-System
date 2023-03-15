from django.urls import path
from .views import UserViewset

urlpatterns = [
    path(
        "activate/<uid>/<token>",
        UserViewset.as_view({"get": "activation"}),
        name="activation",
    ),
]
