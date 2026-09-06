from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import CustomCakeRequest


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("ONLINE", "Razorpay Online Payment"),
    ]
    customer_name = forms.CharField(max_length=120, label="Full Name")
    phone = forms.CharField(max_length=20, label="Phone")
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    city = forms.CharField(max_length=80)
    pincode = forms.CharField(max_length=10)
    delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Delivery Date",
    )
    delivery_slot = forms.ChoiceField(
        choices=[
            ("Morning (9 AM - 12 PM)", "Morning (9 AM - 12 PM)"),
            ("Afternoon (12 PM - 4 PM)", "Afternoon (12 PM - 4 PM)"),
            ("Evening (4 PM - 8 PM)", "Evening (4 PM - 8 PM)"),
        ]
    )
    custom_message = forms.CharField(
        max_length=120, required=False,
        label="Message on Cake",
        widget=forms.TextInput(attrs={"placeholder": "Happy Birthday!"}),
    )
    notes = forms.CharField(
        required=False, label="Special Instructions",
        widget=forms.Textarea(attrs={"rows": 2}),
    )
    coupon_code = forms.CharField(
        max_length=30, required=False, label="Coupon Code",
        widget=forms.TextInput(attrs={"placeholder": "Try SWEET10"}),
    )
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)

    def clean_delivery_date(self):
        value = self.cleaned_data["delivery_date"]
        if value < timezone.localdate():
            raise forms.ValidationError("Delivery date cannot be in the past.")
        return value


class CustomCakeForm(forms.ModelForm):
    class Meta:
        model = CustomCakeRequest
        fields = ("message_on_cake", "flavour", "size", "theme", "delivery_date", "notes")
        widgets = {
            "delivery_date": forms.DateInput(attrs={"type": "date"}),
            "message_on_cake": forms.TextInput(attrs={"placeholder": "Happy Birthday!"}),
            "theme": forms.TextInput(attrs={"placeholder": "Pink floral / cartoon / minimal"}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Tell us any special requirement"}),
        }

    def clean_delivery_date(self):
        value = self.cleaned_data["delivery_date"]
        if value < timezone.localdate():
            raise forms.ValidationError("Choose today or a future date.")
        return value
