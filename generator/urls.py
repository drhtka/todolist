# -*- coding: utf-8 -*-

from django.urls import path, include
from generator import views

urlpatterns = [
    path('generator/', views.generator, name='generator'),
    path('password/', views.password, name='password'),
]