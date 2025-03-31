from django.contrib import admin
from .models import (
    Category,
    Course,
    CoursePart,
    Lesson,
    Enrollment,
    Progress,
    OneTimeVideoToken
)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'part', 'order', 'duration', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    list_filter = ('part', 'order', 'created_at')


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CoursePart)
admin.site.register(Enrollment)
admin.site.register(Progress)
admin.site.register(OneTimeVideoToken)
