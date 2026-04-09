from django import forms
from django.contrib.auth import get_user_model

from grooming.models import Pet


class ClientUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10, required=True)
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "phone_number"]

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if not phone:
            return phone

        if not phone.startswith("0"):
            raise forms.ValidationError("Номер повинен починатися с 0")

        return phone


class ClientPetCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    breed = forms.CharField(max_length=100, required=True)
    class Meta:
        model = Pet
        fields = ["name", "pet_type", "breed"]