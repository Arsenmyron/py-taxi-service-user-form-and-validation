from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Invalid license number")
        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise ValidationError("Invalid license number")
        if not license_number[3:].isdigit():
            raise ValidationError("Invalid license number")
        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
                message="Insert valid license number",
            )
        ]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )
