from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from academics.models import AcademicYear, Section
from students.models import Enrolment

from .forms import AttendanceForm
from .models import Attendance, AttendanceEntry


@login_required
def attendance_home(request):
    attendances = (
        Attendance.objects
        .select_related(
            "academic_year",
            "section",
            "section__school_class",
        )
        .order_by("-date")
    )

    return render(
        request,
        "attendance/home.html",
        {
            "attendances": attendances,
        },
    )


@login_required
def record_attendance(request):

    if request.method == "POST":

        form = AttendanceForm(request.POST)

        if form.is_valid():

            academic_year = form.cleaned_data["academic_year"]
            section = form.cleaned_data["section"]
            date = form.cleaned_data["date"]
            recorded_by_name = form.cleaned_data["recorded_by_name"]

            existing = Attendance.objects.filter(
                academic_year=academic_year,
                section=section,
                date=date,
            ).first()

            if existing:
                return redirect(
                    "attendance_edit",
                    attendance_id=existing.id,
                )

            enrolments = (
                Enrolment.objects
                .filter(
                    academic_year=academic_year,
                    section=section,
                    is_active=True,
                    student__is_active=True,
                )
                .select_related("student")
                .order_by(
                    "student__last_name",
                    "student__first_name",
                )
            )

            return render(
                request,
                "attendance/record.html",
                {
                    "form": form,
                    "enrolments": enrolments,
                    "academic_year": academic_year,
                    "section": section,
                    "date": date,
                    "recorded_by_name": recorded_by_name,
                },
            )

    else:
        form = AttendanceForm()

    return render(
        request,
        "attendance/record_form.html",
        {
            "form": form,
        },
    )


@login_required
@transaction.atomic
def save_attendance(request):

    if request.method != "POST":
        return redirect("attendance_home")

    form = AttendanceForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "attendance/record_form.html",
            {
                "form": form,
            },
        )

    academic_year = form.cleaned_data["academic_year"]
    section = form.cleaned_data["section"]
    date = form.cleaned_data["date"]
    recorded_by_name = form.cleaned_data["recorded_by_name"]

    attendance, created = Attendance.objects.get_or_create(
        academic_year=academic_year,
        section=section,
        date=date,
        defaults={
            "recorded_by_name": recorded_by_name,
        },
    )

    if not created:
        return redirect(
            "attendance_edit",
            attendance_id=attendance.id,
        )

    enrolments = Enrolment.objects.filter(
        academic_year=academic_year,
        section=section,
        is_active=True,
        student__is_active=True,
    )

    for enrolment in enrolments:

        status = request.POST.get(
            f"status_{enrolment.student.id}"
        )

        if status in {
            "PRESENT",
            "ABSENT",
            "PERMISSION",
            "SICK",
        }:
            AttendanceEntry.objects.create(
                attendance=attendance,
                student=enrolment.student,
                status=status,
            )

    return redirect(
        "attendance_home"
    )


@login_required
def attendance_edit(request, attendance_id):

    attendance = get_object_or_404(
        Attendance.objects.select_related(
            "academic_year",
            "section",
            "section__school_class",
        ),
        id=attendance_id,
    )

    enrolments = (
        Enrolment.objects
        .filter(
            academic_year=attendance.academic_year,
            section=attendance.section,
            is_active=True,
            student__is_active=True,
        )
        .select_related("student")
        .order_by(
            "student__last_name",
            "student__first_name",
        )
    )

    existing_entries = {
        entry.student_id: entry.status
        for entry in attendance.entries.all()
    }

    if request.method == "POST":

        recorded_by_name = request.POST.get(
            "recorded_by_name",
            "",
        ).strip()

        if recorded_by_name:
            attendance.recorded_by_name = recorded_by_name
            attendance.save(
                update_fields=[
                    "recorded_by_name",
                    "updated_at",
                ]
            )

        for enrolment in enrolments:

            status = request.POST.get(
                f"status_{enrolment.student.id}"
            )

            if status in {
                "PRESENT",
                "ABSENT",
                "PERMISSION",
                "SICK",
            }:

                AttendanceEntry.objects.update_or_create(
                    attendance=attendance,
                    student=enrolment.student,
                    defaults={
                        "status": status,
                    },
                )

        return redirect(
            "attendance_home"
        )

    return render(
        request,
        "attendance/edit.html",
        {
            "attendance": attendance,
            "enrolments": enrolments,
            "existing_entries": existing_entries,
        },
    )