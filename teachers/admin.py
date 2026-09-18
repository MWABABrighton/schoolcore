from django.contrib import admin
from .models import Teacher, TeachingAssignment


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "employee_number",
        "first_name",
        "last_name",
        "gender",
        "phone_number",
        "is_active",
    )

    list_filter = (
        "gender",
        "is_active",
    )

    search_fields = (
        "employee_number",
        "first_name",
        "middle_name",
        "last_name",
    )


@admin.register(TeachingAssignment)
class TeachingAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "teacher",
        "subject",
        "section",
        "academic_year",
        "is_active",
    )

    list_filter = (
        "academic_year",
        "section",
        "subject",
        "is_active",
    )

    search_fields = (
        "teacher__employee_number",
        "teacher__first_name",
        "teacher__last_name",
        "subject__name",
        "section__name",
    )