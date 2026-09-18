from django.shortcuts import get_object_or_404, render

from students.models import Student


def student_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    return render(
        request,
        "reports/student_report_card.html",
        {
            "student": student,
        },
    )