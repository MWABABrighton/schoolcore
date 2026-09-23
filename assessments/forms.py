from django import forms

from .models import Examination, Result


class ExaminationForm(forms.ModelForm):

    class Meta:
        model = Examination

        fields = [
            "academic_year",
            "term",
            "class_section",
            "subject",
            "exam_date",
            "is_active",
        ]

        widgets = {
            "exam_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }


class ResultForm(forms.ModelForm):

    class Meta:
        model = Result

        fields = [
            "marks",
            "remarks",
        ]

        widgets = {
            "marks": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "max": "100",
                }
            ),
        }