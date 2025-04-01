from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer, SessionSerializer, OnboardingAnswersSerializer
from users.models import User, OnboardingAnswers


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=200)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    user = User.objects.filter(id=request.data.get("id")).first()
    if user:
        return Response(
            {
                "error": "User already exists",
                "has_registered_successfully": bool(user.phone_number),
            },
            status=400,
        )
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def update_user(request, id):
    user = User.objects.filter(id=id).first()
    if not user:
        return Response({"error": "User not found"}, status=404)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_sessions(request):
    sessions = request.user.custom_sessions.all()
    serializer = SessionSerializer(sessions, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_onboarding_answers(request):
    data = request.data
    data.update(user=request.user.id)
    serializer = OnboardingAnswersSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
