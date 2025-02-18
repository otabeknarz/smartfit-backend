from django.urls import path
from . import views
from . import auth_apis

app_name = "users"

urlpatterns = [
    # Auth APIs
    path('login/', auth_apis.login_view, name="login"),
    path('logout/', auth_apis.logout_view, name="logout"),
    # User APIs
    path('get-me/', views.get_me, name="get_me"),
    path('get/', views.get_users, name="get_users"),
    path('create/', views.create_user, name="create_user"),
    path('update/<str:id>/', views.update_user, name="update_user"),
    path('get-my-sessions/', views.get_my_sessions, name="get_my_sessions"),
]
