from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
    path("api/users/", include("users.api.urls")),
    path("api/courses/", include("courses.api.urls")),
]
