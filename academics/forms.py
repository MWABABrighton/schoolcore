from django import forms

from .models import AcademicYear, SchoolClass, Section, Subject


class AcademicYearForm(forms.ModelForm):

    class Meta:
        model = AcademicYear
        fields = [
            "year",
            "is_current",
        ]


class SchoolClassForm(forms.ModelForm):

    class Meta:
        model = SchoolClass
        fields = [
            "name",
            "description",
        ]


class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = [
            "school_class",
            "name",
        ]


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = [
            "code",
            "name",
            "description",
            "is_active",
        ]