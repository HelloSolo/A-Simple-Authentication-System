from django.urls import path
from .views import GoogleAuthView, FacebookAuthView

urlpatterns = [
    path("google/", GoogleAuthView.as_view()),
    path("facebook/", FacebookAuthView.as_view()),
]
