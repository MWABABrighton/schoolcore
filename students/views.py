from django.shortcuts import get_object_or_404, render

from .models import Student


def student_list(request):
    students = Student.objects.filter(
        is_active=True
    ).order_by(
        "last_name",
        "first_name",
    )

    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
        },
    )


def student_detail(request, student_id):
    student = get_object_or_404(
        Student,
        id=student_id,
    )

    enrolments = student.enrolments.select_related(
        "academic_year",
        "section",
        "section__school_class",
    ).order_by(
        "-academic_year__year"
    )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
            "enrolments": enrolments,
        },
    )