from django import forms

from academics.models import AcademicYear, Section
from students.models import Student

from .models import Attendance


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = [
            "academic_year",
            "section",
            "date",
            "recorded_by_name",
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "recorded_by_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter your name",
                }
            ),
        }


class AttendanceEntryForm(forms.Form):

    student = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        widget=forms.HiddenInput(),
    )

    status = forms.ChoiceField(
        choices=[
            ("PRESENT", "Present"),
            ("ABSENT", "Absent"),
            ("PERMISSION", "Permission"),
            ("SICK", "Sick"),
        ],
        widget=forms.RadioSelect,
    )


class AttendanceStudentForm(forms.Form):

    student_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    status = forms.ChoiceField(
        choices=[
            ("PRESENT", "Present"),
            ("ABSENT", "Absent"),
            ("PERMISSION", "Permission"),
            ("SICK", "Sick"),
        ],
        widget=forms.RadioSelect,
    )