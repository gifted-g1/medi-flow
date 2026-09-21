from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import LoginView, LogoutView, MeView, UserViewSet
from apps.patients.views import DepartmentViewSet, PatientViewSet, VisitViewSet
from apps.operations.views import DashboardView, QueueView


def health_check(request):
    return JsonResponse({
        "status": "ok",
        "service": "MediFlow API",
        "message": "MediFlow backend is running",
    })


router = DefaultRouter()
router.trailing_slash = ""

router.register("users", UserViewSet, basename="user")
router.register("patients", PatientViewSet, basename="patient")
router.register("departments", DepartmentViewSet, basename="department")
router.register("visits", VisitViewSet, basename="visit")


urlpatterns = [
    # Root / health check
    path("", health_check, name="health"),

    # Admin
    path("admin/", admin.site.urls),

    # Authentication
    path("api/login", LoginView.as_view()),
    path("api/logout", LogoutView.as_view()),
    path("api/me", MeView.as_view()),

    # Operations
    path("api/queue", QueueView.as_view()),
    path("api/dashboard", DashboardView.as_view()),

    # REST API
    path("api/", include(router.urls)),
]
