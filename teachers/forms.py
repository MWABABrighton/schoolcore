from django import forms

from .models import (
    Teacher,
    ClassTeacherAssignment,
)


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher

        fields = [
            "employee_number",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "date_of_birth",
            "phone_number",
            "email",
            "address",
            "employment_date",
            "is_active",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "employment_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),
        }


class ClassTeacherAssignmentForm(forms.ModelForm):

    class Meta:
        model = ClassTeacherAssignment

        fields = [
            "teacher",
            "section",
            "academic_year",
            "is_active",
        ]