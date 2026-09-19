from django.shortcuts import render

from students.models import Student
from teachers.models import Teacher
from academics.models import SchoolClass, Subject
from attendance.models import Attendance


def dashboard_home(request):
    context = {
        "student_count": Student.objects.filter(is_active=True).count(),
        "teacher_count": Teacher.objects.filter(is_active=True).count(),
        "class_count": SchoolClass.objects.count(),
        "subject_count": Subject.objects.filter(is_active=True).count(),
        "attendance_count": Attendance.objects.count(),
    }

    return render(
        request,
        "dashboard/home.html",
        context,
    )