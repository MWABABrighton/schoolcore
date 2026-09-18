from django.contrib import admin
from .models import Student, Guardian, Enrolment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_number",
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "is_active",
    )
    list_filter = ("gender", "is_active")
    search_fields = (
        "student_number",
        "first_name",
        "middle_name",
        "last_name",
    )


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "student",
        "relationship",
        "phone_number",
        "is_primary",
    )
    list_filter = ("relationship", "is_primary")
    search_fields = (
        "full_name",
        "student__student_number",
        "student__first_name",
        "student__last_name",
    )


@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "academic_year",
        "section",
        "enrolment_date",
        "is_active",
    )
    list_filter = (
        "academic_year",
        "section",
        "is_active",
    )
    search_fields = (
        "student__student_number",
        "student__first_name",
        "student__last_name",
    )