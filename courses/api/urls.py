from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("get-categories/", views.get_categories, name="get_categories"),
    path("get-courses/", views.get_courses, name="get_courses"),
    path("get-progress/", views.get_progress, name="get_progress"),
]