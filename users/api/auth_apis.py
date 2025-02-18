from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User, CustomSession
from rest_framework.authtoken.models import Token


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    id = request.data.get("id")
    if id is None:
        return Response({"error": "ID is required"}, status=400)
    user = User.objects.filter(id=id).first()
    if user is None:
        return Response({"error": "User not found"}, status=404)
    if user.custom_sessions.all().count() > 0:
        return Response({"error": "User already logged in"}, status=400)
    token, created = Token.objects.get_or_create(user=user)
    CustomSession.objects.create(
        user=user,
        token=token.key,
        ip_address=request.META.get("REMOTE_ADDR"),
        device_info=request.META.get("HTTP_USER_AGENT")
    )
    return Response({"token": token.key}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    request.user.custom_sessions.all().delete()
    return Response({"message": "Logged out successfully"}, status=200)
