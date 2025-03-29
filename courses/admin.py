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

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CoursePart)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Progress)
admin.site.register(OneTimeVideoToken)
