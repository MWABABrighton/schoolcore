from django import forms

from academics.models import AcademicYear, Section
from .models import Student


class StudentForm(forms.ModelForm):

    academic_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all().order_by("-year"),
        required=True,
        label="Academic Year",
    )

    section = forms.ModelChoiceField(
        queryset=Section.objects.select_related(
            "school_class"
        ).order_by(
            "school_class__name",
            "name",
        ),
        required=True,
        label="Class & Section",
    )

    class Meta:
        model = Student

        fields = [
            "student_number",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "gender",
            "phone_number",
            "email",
            "address",
            "is_active",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
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