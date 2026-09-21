from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def post(self, request):
        username = request.data.get("staffId") or request.data.get("username")
        password = request.data.get("password")
        if not username or not password: return Response({"detail": "staffId and password are required."}, status=400)
        user = authenticate(request, username=username, password=password)
        if not user or not user.is_active: return Response({"detail": "Invalid credentials."}, status=401)
        login(request, user)
        return Response({"message": "Login successful", "id": user.id, "username": user.username, "displayName": user.display_name or user.get_full_name() or user.username, "role": user.role})

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully."})

class MeView(APIView):
    def get(self, request): return Response(UserSerializer(request.user).data)

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view): return bool(request.user.is_authenticated and request.user.role == User.Role.ADMIN)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
