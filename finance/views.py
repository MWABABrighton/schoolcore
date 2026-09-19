from django.shortcuts import redirect, render

from .forms import PaymentForm
from .models import StudentFee


def finance_dashboard(request):

    student_fees = (
        StudentFee.objects
        .filter(is_active=True)
        .select_related(
            "student",
            "academic_year",
            "fee_structure",
        )
        .order_by(
            "student__last_name",
            "student__first_name",
        )
    )

    total_due = sum(
        fee.amount_due for fee in student_fees
    )

    total_paid = sum(
        fee.amount_paid for fee in student_fees
    )

    total_balance = sum(
        fee.balance for fee in student_fees
    )

    context = {
        "student_fees": student_fees,
        "total_due": total_due,
        "total_paid": total_paid,
        "total_balance": total_balance,
    }

    return render(
        request,
        "finance/dashboard.html",
        context,
    )


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