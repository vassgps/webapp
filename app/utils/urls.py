# webapp/utils/urls.py

from django.urls import path
from .views import welcome, about

urlpatterns = [
    path('', welcome, name='welcome'),
    path('about', about, name='about'),
]
