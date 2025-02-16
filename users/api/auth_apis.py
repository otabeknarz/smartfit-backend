from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.middleware.csrf import get_token
from users.models import User, CustomSession
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(["GET"])
@permission_classes([AllowAny])
def get_csrf_token(request):
    return Response({"csrfToken": get_token(request)})


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    id = request.data.get("id")

    user = User.objects.filter(id=id).first()
    if user:
        if user.custom_sessions.count() >= 1:
            return Response({"error": "Multiple sessions not allowed"}, status=400)

        login(request, user)
        CustomSession.objects.create(
            user=user,
            sessionid=request.session.session_key,
            ip_address=request.META.get("REMOTE_ADDR"),
            device_info=request.META.get("HTTP_USER_AGENT")
        )
        return Response(
            {
                "message": "Login successful",
                "has_successfully_registered": bool(user.gender) and bool(user.age) and bool(user.height)
            },
            status=200
        )

    return Response({"error": "Invalid credentials"}, status=400)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.custom_sessions.filter(sessionid=request.session.session_key).delete()
    logout(request)
    return Response({"message": "Logged out"}, status=200)
