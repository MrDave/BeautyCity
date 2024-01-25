from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def service(request):
    return render(request, 'service.html')


def service_final(request):
    return render(request, 'serviceFinally.html')


def notes(request):
    return render(request, 'notes.html')


def manager(request):
    return render(request, 'admin.html')
