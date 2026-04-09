from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView

from grooming.forms import ClientUpdateForm, ClientPetCreateForm
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