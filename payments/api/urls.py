from django.urls import path
from . import views

urlpatterns = [
    path("payme/", views.PaymeAPIView.as_view()),
]
