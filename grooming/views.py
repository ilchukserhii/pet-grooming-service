from django.shortcuts import render
from django.views import generic

from grooming.models import Service, Groomer, Pet


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