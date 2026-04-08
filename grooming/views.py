from django.shortcuts import render

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