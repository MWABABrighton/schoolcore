from django import forms

from .models import Examination, Result


class ExaminationForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user and user.role == "TEACHER":

            teacher = getattr(
                user,
                "teacher_profile",
                None,
            )

            if teacher is not None:

                assignments = (
                    teacher.teaching_assignments
                    .filter(
                        is_active=True,
                    )
                    .select_related(
                        "academic_year",
                        "section",
                        "subject",
                    )
                )

                academic_year_ids = assignments.values_list(
                    "academic_year_id",
                    flat=True,
                )

                section_ids = assignments.values_list(
                    "section_id",
                    flat=True,
                )

                subject_ids = assignments.values_list(
                    "subject_id",
                    flat=True,
                )

                self.fields[
                    "academic_year"
                ].queryset = (
                    self.fields[
                        "academic_year"
                    ].queryset.filter(
                        id__in=academic_year_ids
                    )
                )

                self.fields[
                    "class_section"
                ].queryset = (
                    self.fields[
                        "class_section"
                    ].queryset.filter(
                        id__in=section_ids
                    )
                )

                self.fields[
                    "subject"
                ].queryset = (
                    self.fields[
                        "subject"
                    ].queryset.filter(
                        id__in=subject_ids
                    )
                )

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