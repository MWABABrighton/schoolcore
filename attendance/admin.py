from django.contrib import admin

from .models import Attendance, AttendanceEntry


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = [
        "academic_year",
        "section",
        "date",
        "recorded_by_name",
    ]

    list_filter = [
        "academic_year",
        "section",
        "date",
    ]

    search_fields = [
        "section__school_class__name",
        "section__name",
        "recorded_by_name",
    ]


@admin.register(AttendanceEntry)
class AttendanceEntryAdmin(admin.ModelAdmin):

    list_display = [
        "attendance",
        "student",
        "status",
    ]

    list_filter = [
        "status",
        "attendance__academic_year",
        "attendance__section",
    ]

    search_fields = [
        "student__first_name",
        "student__last_name",
        "student__student_number",
    ]