# analysis/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input/', views.result_page, name='result_page'),
    path('popularity_chart/', views.popularity_chart, name='popularity_chart'),
    path('iit_branches/', views.iit_branches, name='iit_branches'),
]
