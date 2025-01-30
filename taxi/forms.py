import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from taxi.models import Driver, Car
from taxi_service.settings import LICENSE_NUMBER_PATTERN


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.match(LICENSE_NUMBER_PATTERN, license_number):
            raise ValidationError("Invalid license number")
        return license_number

class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
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
                regex=LICENSE_NUMBER_PATTERN,
                message="Insert valid license number",
            )
        ]
    )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(LICENSE_NUMBER_PATTERN, license_number):
            raise ValidationError("Invalid license number")
        return license_number

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )
