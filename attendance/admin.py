from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "enrolment",
        "date",
        "status",
        "recorded_by",
    )

    list_filter = (
        "status",
        "date",
        "enrolment__academic_year",
    )

    search_fields = (
        "student__student_number",
        "student__first_name",
        "student__last_name",
    )

    date_hierarchy = "date"