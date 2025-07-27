from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'hospitals', views.HospitalView, 'hospitals')

urlpatterns = [
    path('', include(router.urls))
]