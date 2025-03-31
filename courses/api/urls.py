from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("get-categories/", views.get_categories, name="get_categories"),
    path("get-courses/", views.get_courses, name="get_courses"),
    path("get-progress/", views.get_progress, name="get_progress"),
    path("get-my-courses/", views.get_my_courses, name="get_my_courses"),
    path("get-course/<slug:slug>/", views.get_course, name="get_course"),
    path(
        "get-one-time-video-token/<uuid:lesson_id>/",
        views.get_one_time_video_token,
        name="get_one_time_video",
    ),
]
