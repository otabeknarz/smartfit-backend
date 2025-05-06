from django.urls import path
from . import views

urlpatterns = [
    path("payme/", views.payme_payment_view),
]
