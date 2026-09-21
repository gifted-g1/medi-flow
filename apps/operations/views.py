from django.db.models import Count
from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.patients.models import Visit

class QueueView(APIView):
    def get(self, request):
        department = request.query_params.get("department")
        visits = Visit.objects.select_related("patient", "department").filter(status=Visit.Status.WAITING)
        if department: visits = visits.filter(department__code=department)
        return Response([{"visitId": visit.visit_number, "patientId": visit.patient_id, "fullName": visit.patient.full_name, "hospitalNumber": visit.patient.hospital_number, "department": visit.department.code, "priority": visit.esi, "status": "Urgent" if visit.esi <= 2 else "Waiting", "arrival": timezone.localtime(visit.checked_in_at).strftime("%H:%M"), "wait": f"{index * 10} min" if index else "Now"} for index, visit in enumerate(visits.order_by("esi", "checked_in_at"))])

class DashboardView(APIView):
    def get(self, request):
        today = timezone.localdate()
        visits = Visit.objects.filter(checked_in_at__date=today)
        return Response({"patientsToday": visits.values("patient").distinct().count(), "currentlyWaiting": visits.filter(status=Visit.Status.WAITING).count(), "emergencyCases": visits.filter(esi__lte=2, status=Visit.Status.WAITING).count(), "byDepartment": list(visits.values("department__name").annotate(total=Count("id")).order_by("department__name"))})
