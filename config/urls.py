from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.accounts.views import LoginView, LogoutView, MeView, UserViewSet
from apps.patients.views import DepartmentViewSet, PatientViewSet, VisitViewSet
from apps.operations.views import DashboardView, QueueView

router = DefaultRouter()
router.trailing_slash = ""  # Existing MediFlow frontend calls /api/patients, not /api/patients/.
router.register("users", UserViewSet, basename="user")
router.register("patients", PatientViewSet, basename="patient")
router.register("departments", DepartmentViewSet, basename="department")
router.register("visits", VisitViewSet, basename="visit")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login", LoginView.as_view()), path("api/logout", LogoutView.as_view()), path("api/me", MeView.as_view()),
    path("api/queue", QueueView.as_view()), path("api/dashboard", DashboardView.as_view()),
    path("api/", include(router.urls)),
]
