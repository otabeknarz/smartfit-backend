from rest_framework import serializers
from courses.models import (
    Category,
    Course,
    CoursePart,
    Lesson,
    Comment,
    Enrollment,
    Progress,
    OneTimeVideoToken,
)
from users.api.serializers import UserSerializer, UserCommentSerializer, TrainerSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"


class CoursePartSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = CoursePart
        fields = "__all__"


class CoursesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    trainers = TrainerSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    trainers = TrainerSerializer(many=True, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    parts = CoursePartSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = "__all__"


class OneTimeVideoTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneTimeVideoToken
        fields = "id", "lesson", "is_used", "created_at"
