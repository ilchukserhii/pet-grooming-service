from datetime import datetime

from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import (
    TemplateView,
    UpdateView,
    CreateView,
    DeleteView
)

from grooming.forms import (
    ClientUpdateForm,
    ClientPetCreateForm,
    ClientAppointmentForm,
    ClientCreateForm,
    SearchForm,
    GuestForm
)
from grooming.models import Service, Groomer, Pet, Appointment


Client = get_user_model()


class SearchMixin:
    search_field = None
    placeholder = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchForm(self.request.GET)
        form.fields["search"].widget.attrs["placeholder"] = (
            self.placeholder)
        context["search_form"] = form

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data["search"]
            return queryset.filter(
                **{f"{self.search_field}__icontains": search}
            )
        return queryset


class AppointmentFormSaveMixin:
    def save_appointment_form(self, form):
        appointment = form.save(commit=False)
        appointment.date_time = datetime.combine(
            form.cleaned_data["appointment_date"],
            form.cleaned_data["appointment_time"],
        )
        appointment.save()
        form.save_m2m()
        self.object = appointment
        return super().form_valid(form)


def index(request):
    our_services = Service.objects.all()
    our_works = Pet.objects.filter(
        appointments__is_completed=True
    ).distinct()
    form = GuestForm
    context = {
        "our_services": our_services,
        "our_works": our_works,
        "form": form,
    }
    if request.user.is_authenticated:
        client = request.user
        client_completed_appointments = Appointment.objects.filter(
            pet__client=client, is_completed=True
        ).count()
        client_incompleted_appointments = Appointment.objects.filter(
            pet__client=client, is_completed=False
        ).count()
        context.update(
            {
                "client_completed_appointments":
                    client_completed_appointments,
                "client_incompleted_appointments":
                    client_incompleted_appointments,
            }
        )
    success_url = reverse_lazy("grooming:index")
    if request.method == "POST":
        form = GuestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(success_url)
    return render(request, "grooming/index.html", context=context)


class ServiceListView(SearchMixin, generic.ListView):
    model = Service
    context_object_name = "services"
    paginate_by = 4
    search_field = "type"
    placeholder = "Пошук за послугою"


class GroomerListView(SearchMixin, generic.ListView):
    model = Groomer
    context_object_name = "groomers"
    queryset = Groomer.objects.prefetch_related("service").distinct()
    paginate_by = 4
    search_field = "first_name"
    placeholder = "Пошук за імя`м"


class CabinetView(LoginRequiredMixin, TemplateView):
    template_name = "grooming/cabinet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.request.user
        pets = client.pets.all()
        appointments_for_client = Appointment.objects.filter(
            pet__client=client
        ).select_related("pet", "groomer").prefetch_related("service")

        context["client"] = client
        context["pets"] = pets
        context["appointments"] = appointments_for_client

        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientCreateForm
    template_name = "grooming/client_create.html"
    success_url = reverse_lazy("grooming:cabinet")

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientUpdateForm
    template_name = "grooming/client_update.html"
    success_url = reverse_lazy("grooming:cabinet")

    def get_object(self, queryset=None):
        return self.request.user


class ClientPetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = ClientPetCreateForm
    template_name = "grooming/client_pet_add.html"
    success_url = reverse_lazy("grooming:cabinet")

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.client = self.request.user
        pet.save()
        return super().form_valid(form)


class ClientPetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = "grooming/client_pet_delete.html"
    success_url = reverse_lazy("grooming:cabinet")

    def get_queryset(self):
        return Pet.objects.filter(client=self.request.user)


class ClientAppointmentCreateView(
    LoginRequiredMixin,
    AppointmentFormSaveMixin,
    CreateView
):
    model = Appointment
    form_class = ClientAppointmentForm
    template_name = "grooming/client_appointment_form.html"
    success_url = reverse_lazy("grooming:cabinet")

    def get_initial(self):
        initial = super().get_initial()
        service_id = self.request.GET.get("service")
        if service_id:
            initial["service"] = service_id
        groomer_id = self.request.GET.get("groomer")
        if groomer_id:
            initial["groomer"] = groomer_id
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["pet"].queryset = Pet.objects.filter(
            client=self.request.user
        )
        return form

    def form_valid(self, form):
        return self.save_appointment_form(form)


class ClientAppointmentUpdateView(
    LoginRequiredMixin,
    AppointmentFormSaveMixin,
    UpdateView
):
    model = Appointment
    form_class = ClientAppointmentForm
    template_name = "grooming/client_appointment_form.html"
    success_url = reverse_lazy("grooming:cabinet")

    def get_queryset(self):
        return Appointment.objects.filter(pet__client=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["pet"].queryset = Pet.objects.filter(
            client=self.request.user
        )
        return form

    def form_valid(self, form):
        return self.save_appointment_form(form)

    def get_initial(self):
        initial = super().get_initial()
        initial["appointment_date"] = self.object.date_time.date()
        initial["appointment_time"] = (
            self.object.date_time.time().replace(microsecond=0)
        )
        return initial


class ClientAppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = "grooming/client_appointment_delete.html"
    success_url = reverse_lazy("grooming:cabinet")

    def get_queryset(self):
        return Appointment.objects.filter(pet__client=self.request.user)
