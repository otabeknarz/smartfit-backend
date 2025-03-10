from django.contrib import admin
from .models import Category, Course, CoursePart, Lesson, Enrollment, Progress

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CoursePart)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Progress)
