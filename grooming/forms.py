from django import forms
from django.contrib.auth import get_user_model
from datetime import datetime

from grooming.models import Pet, Appointment, Service, Groomer


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


class ClientCreateAppointmentForm(forms.ModelForm):
    pet = forms.ModelChoiceField(
        queryset=Pet.objects.none(),
        required=True)
    service = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    groomer = forms.ModelChoiceField(
        queryset=Groomer.objects.all(),
        required=True)
    appointment_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    appointment_time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={"type": "time"}),
    )

    class Meta:
        model = Appointment
        fields = ["pet", "service", "groomer",]

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("appointment_date")
        time = cleaned_data.get("appointment_time")
        if date and time:
            combined = datetime.combine(date, time)
            if combined < datetime.now():
                raise forms.ValidationError("Запис повинен бути на майбутнє")
        return cleaned_data