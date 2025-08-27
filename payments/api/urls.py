from rest_framework.routers import DefaultRouter
from . import views


default_router = DefaultRouter()
default_router.register(r'payments', views.PaymentViewSet)

urlpatterns = default_router.urls
