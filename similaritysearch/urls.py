# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('compare-images/', views.compare_images, name='compare_images'),
]