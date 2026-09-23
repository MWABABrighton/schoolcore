from django import forms

from .models import FeeStructure, Payment


class FeeStructureForm(forms.ModelForm):

    class Meta:
        model = FeeStructure

        fields = [
            "academic_year",
            "school_class",
            "fee_type",
            "amount",
            "description",
            "is_active",
        ]

        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                }
            ),
        }


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment

        fields = [
            "student_fee",
            "amount",
            "payment_date",
            "payment_method",
            "receipt_number",
            "reference",
            "remarks",
        ]

        widgets = {
            "payment_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def clean_amount(self):

        amount = self.cleaned_data["amount"]

        student_fee = self.cleaned_data.get("student_fee")

        if student_fee:

            balance = student_fee.balance

            if amount <= 0:
                raise forms.ValidationError(
                    "Payment amount must be greater than zero."
                )

            if amount > balance:
                raise forms.ValidationError(
                    f"Payment cannot exceed the outstanding "
                    f"balance of K{balance:.2f}."
                )

        return amount