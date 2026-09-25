from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AcademicYearForm,
    SchoolClassForm,
    SectionForm,
    SubjectForm,
)
from .models import AcademicYear, SchoolClass, Section, Subject


@login_required
def academics_home(request):
    context = {
        "academic_years": AcademicYear.objects.all().order_by("-year"),
        "classes": SchoolClass.objects.all().order_by("name"),
        "sections": Section.objects.select_related(
            "school_class"
        ).order_by(
            "school_class__name",
            "name",
        ),
        "subjects": Subject.objects.all().order_by("name"),
    }

    return render(
        request,
        "academics/home.html",
        context,
    )


@login_required
def create_academic_year(request):

    if request.method == "POST":
        form = AcademicYearForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("academics_home")

    else:
        form = AcademicYearForm()

    return render(
        request,
        "academics/form.html",
        {
            "form": form,
            "title": "Add Academic Year",
        },
    )


@login_required
def create_class(request):

    if request.method == "POST":
        form = SchoolClassForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("academics_home")

    else:
        form = SchoolClassForm()

    return render(
        request,
        "academics/form.html",
        {
            "form": form,
            "title": "Add Class",
        },
    )


@login_required
def create_section(request):

    if request.method == "POST":
        form = SectionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("academics_home")

    else:
        form = SectionForm()

    return render(
        request,
        "academics/form.html",
        {
            "form": form,
            "title": "Add Section",
        },
    )


@login_required
def create_subject(request):

    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("academics_home")

    else:
        form = SubjectForm()

    return render(
        request,
        "academics/form.html",
        {
            "form": form,
            "title": "Add Subject",
        },
    )