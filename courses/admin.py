from django.contrib import admin
from .models import (
    Category,
    Course,
    CoursePart,
    Lesson,
    Comment,
    Enrollment,
    Progress,
    OneTimeVideoToken,
)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "part", "order", "duration", "created_at")
    search_fields = ("title",)
    ordering = ("-created_at",)
    list_filter = ("part", "order", "created_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "created_at")
    search_fields = ("user__name", "text")
    ordering = ("-created_at",)
    list_filter = ("lesson", "created_at")


@admin.register(OneTimeVideoToken)
class OneTimeVideoTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "is_used", "created_at")
    search_fields = ("user__name", "lesson__title")
    ordering = ("-created_at",)
    list_filter = ("user", "lesson", "created_at", "is_used")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")
    search_fields = ("student__name", "course__title")
    ordering = ("-enrolled_at",)
    list_filter = ("course", "enrolled_at",)


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CoursePart)
admin.site.register(Progress)
