# analysis/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input/', views.input_form, name='input_form'),
    path('result/', views.process_form, name='process_form'),
]
