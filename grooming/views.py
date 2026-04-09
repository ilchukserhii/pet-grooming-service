from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, UpdateView

from grooming.forms import UserUpdateForm
from grooming.models import Service, Groomer, Pet, Appointment

Client = get_user_model()

def index(request):
    our_services = Service.objects.all()
    our_works = Pet.objects.filter(
        appointments__is_completed=True
    ).distinct()
    context = {
        "our_services": our_services,
        "our_works": our_works,
    }
    return render(request, "grooming/index.html", context=context)

class ServiceListView(generic.ListView):
    model = Service
    context_object_name = "services"
    paginate_by = 4


class GroomerListView(generic.ListView):
    model = Groomer
    context_object_name = "groomers"
    queryset = Groomer.objects.prefetch_related("service").distinct()
    paginate_by = 4


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


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = UserUpdateForm
    template_name = "grooming/client_update.html"
    success_url = reverse_lazy("grooming:cabinet")

    def get_object(self, queryset=None):
        return self.request.user