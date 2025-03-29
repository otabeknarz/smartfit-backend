from django.urls import path
from . import views

urlpatterns = [
    path("watch-video/<str:uuid>/", views.video, name="video"),
]
