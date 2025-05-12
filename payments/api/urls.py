from django.urls import path

from . import views

urlpatterns = [
    path("payme/", views.PaymeCallBackAPIView.as_view()),
]
