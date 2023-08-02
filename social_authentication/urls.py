from django.urls import path
from .views import GoogleAuthView, FacebookAuthView, TwitterAuthView

urlpatterns = [
    path("google/", GoogleAuthView.as_view()),
    path("facebook/", FacebookAuthView.as_view()),
    path("facebook/", TwitterAuthView.as_view()),
]
