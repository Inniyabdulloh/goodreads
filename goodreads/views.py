from django.http import HttpResponse


def landing_page(request):
    return HttpResponse("<h1>Landing Page</h1>")