from django.urls import path
from .views import segment_image, download_report

urlpatterns = [
    path("segment-image/", segment_image, name="segment_image"),
    path('download-report/<str:filename>/', download_report, name='download_report'),
]