from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import User
from . import serializers
from courses.models import Category, Course, Progress, Lesson


@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    categories = Category.objects.all()
    serializer = serializers.CategorySerializer(categories, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_courses(request):
    courses = Course.objects.all()
    serializer = serializers.CoursesSerializer(courses, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_courses(request):
    courses = [enrollment.course for enrollment in request.user.enrollments.all()]
    serializer = serializers.CoursesSerializer(courses, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course(request, slug):
    courses = [enrollment.course for enrollment in request.user.enrollments.all() if enrollment.course.slug == slug]
    if len(courses) == 0:
        course = Course.objects.filter(slug=slug).first()
        if course:
            serializer = serializers.CourseSerializer(course)
            response = serializer.data
            response["is_enrolled"] = False
            return Response(response, status=200)

        return Response({"status": "false", "error": "We couldn't find any course with this slug"}, status=404)
    serializer = serializers.CourseSerializer(courses[0])
    response = serializer.data
    response["is_enrolled"] = True
    return Response(response, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def update_progress(request):
    lesson = Lesson.objects.filter(id=request.data.get('lesson_id')).first()
    if not lesson:
        return Response({"error": "Lesson is not found"}, status=404)

    if not request.user.progress:
        progress = Progress(user=request.user)
        progress.lessons.add()
    else:
        progress = request.user.progress
        progress.lessons.add(lesson)

    progress.save()
    serializer = serializers.ProgressSerializer(progress, many=True)
    return Response(serializer.data, status=200)


# TODO: fix this function
@api_view(['GET'])
@permission_classes([AllowAny])
def get_progress(request):
    user = User.objects.filter(id=request.data.get('user_id'))
    progress = request.user.progress
    if not progress:
        Progress.objects.create(user=request.user)

    progress_serializer = serializers.ProgressSerializer(progress)
    return Response(progress_serializer.data, status=200)
