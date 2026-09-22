from django.shortcuts import redirect, render

from .forms import (
    TeacherForm,
    ClassTeacherAssignmentForm,
)
from .models import Teacher


def teacher_list(request):

    teachers = Teacher.objects.filter(
        is_active=True
    ).order_by(
        "last_name",
        "first_name",
    )

    return render(
        request,
        "teachers/teacher_list.html",
        {
            "teachers": teachers,
        },
    )


def teacher_create(request):

    if request.method == "POST":

        form = TeacherForm(request.POST)

        if form.is_valid():

            teacher = form.save()

            return redirect(
                "teacher_list"
            )

    else:

        form = TeacherForm()

    return render(
        request,
        "teachers/teacher_form.html",
        {
            "form": form,
        },
    )


def class_teacher_assignment_create(request):

    if request.method == "POST":

        form = ClassTeacherAssignmentForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "teacher_list"
            )

    else:

        form = ClassTeacherAssignmentForm()

    return render(
        request,
        "teachers/class_teacher_assignment_form.html",
        {
            "form": form,
        },
    )