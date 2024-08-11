# webapp/utils/views.py
from django.shortcuts import render
from django.http import JsonResponse

def welcome(request):
    return render(request, 'utils/welcome.html')

def about(request):
    data = {
        "project": "VASS Django Project Base Template",
        "version": "1.0.0",
        "description": "This is a simple Django project with Postgress, Docker and Nginx",
        "author": "Anand VM",
        "contact": "info@vasssystems.com",
        "pipeline_version": "v1.03"
    }
    return JsonResponse(data)