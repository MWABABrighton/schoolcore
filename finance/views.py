from accounts.decorators import role_required
from django.shortcuts import get_object_or_404, redirect, render

from academics.models import SchoolClass, Section
from students.models import Enrolment

from .forms import FeeStructureForm, PaymentForm
from .models import FeeStructure, Payment, StudentFee
from .services import allocate_fees_for_enrolment


def finance_dashboard(request):

    class_id = request.GET.get("class_id", "")
    section_id = request.GET.get("section_id", "")

    student_fees = (
        StudentFee.objects
        .filter(is_active=True)
        .select_related(
            "student",
            "academic_year",
            "fee_structure",
        )
    )

    if class_id:
        student_fees = student_fees.filter(
            fee_structure__school_class_id=class_id
        )

    if section_id:
        student_fees = student_fees.filter(
            student__enrolments__section_id=section_id,
            student__enrolments__is_active=True,
        )

    student_fees = student_fees.order_by(
        "student__last_name",
        "student__first_name",
    ).distinct()

    total_due = sum(
        fee.amount_due for fee in student_fees
    )

    total_paid = sum(
        fee.amount_paid for fee in student_fees
    )

    total_balance = sum(
        fee.balance for fee in student_fees
    )

    school_classes = SchoolClass.objects.all().order_by(
        "name"
    )

    sections = Section.objects.select_related(
        "school_class"
    ).order_by(
        "school_class__name",
        "name",
    )

    context = {
        "student_fees": student_fees,
        "total_due": total_due,
        "total_paid": total_paid,
        "total_balance": total_balance,
        "school_classes": school_classes,
        "sections": sections,
        "selected_class": class_id,
        "selected_section": section_id,
    }

    return render(
        request,
        "finance/dashboard.html",
        context,
    )


@role_required("DIRECTOR", "ACCOUNTANT")
def create_fee_structure(request):

    if request.method == "POST":

        form = FeeStructureForm(request.POST)

        if form.is_valid():

            fee_structure = form.save()

            # Automatically create StudentFee accounts
            # for existing students when a Tuition fee
            # structure is created after enrolment.
            if fee_structure.fee_type == "TUITION":

                enrolments = Enrolment.objects.filter(
                    academic_year=fee_structure.academic_year,
                    section__school_class=fee_structure.school_class,
                    is_active=True,
                )

                for enrolment in enrolments:
                    allocate_fees_for_enrolment(enrolment)

            return redirect("finance_dashboard")

    else:

        form = FeeStructureForm()

    return render(
        request,
        "finance/fee_structure_form.html",
        {
            "form": form,
        },
    )


@role_required("DIRECTOR", "ACCOUNTANT")
def record_payment(request):

    if request.method == "POST":

        form = PaymentForm(request.POST)

        if form.is_valid():

            payment = form.save(commit=False)

            payment.recorded_by = request.user

            payment.save()

            return redirect("finance_dashboard")

    else:

        form = PaymentForm()

    return render(
        request,
        "finance/payment_form.html",
        {
            "form": form,
        },
    )


def payment_list(request):

    payments = (
        Payment.objects
        .select_related(
            "student_fee",
            "student_fee__student",
            "recorded_by",
        )
        .order_by(
            "-payment_date",
            "-created_at",
        )
    )

    total_payments = sum(
        payment.amount for payment in payments
    )

    return render(
        request,
        "finance/payment_list.html",
        {
            "payments": payments,
            "total_payments": total_payments,
        },
    )


def student_finance(request, student_id):

    student_fee = get_object_or_404(
        StudentFee.objects.select_related(
            "student",
            "academic_year",
            "fee_structure",
        ),
        student_id=student_id,
        is_active=True,
    )

    payments = (
        student_fee.payments
        .select_related("recorded_by")
        .order_by(
            "-payment_date",
            "-created_at",
        )
    )

    context = {
        "student_fee": student_fee,
        "payments": payments,
        "amount_due": student_fee.amount_due,
        "amount_paid": student_fee.amount_paid,
        "balance": student_fee.balance,
    }

    return render(
        request,
        "finance/student_finance.html",
        context,
    )


@role_required("DIRECTOR", "ACCOUNTANT")
def payment_detail(request, payment_id):

    payment = get_object_or_404(
        Payment.objects.select_related(
            "student_fee",
            "student_fee__student",
            "student_fee__academic_year",
            "student_fee__fee_structure",
            "recorded_by",
        ),
        id=payment_id,
    )

    return render(
        request,
        "finance/payment_detail.html",
        {
            "payment": payment,
        },
    )