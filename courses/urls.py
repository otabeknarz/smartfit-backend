from django.urls import path
from . import views

urlpatterns = [
    path("watch-video/<uuid:uuid>/", views.video, name="video"),
]
