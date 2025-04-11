from django.urls import path
from .views import evaluate_images, download_report, HistoryView

urlpatterns = [
    path("evaluate-images/", evaluate_images, name="evaluate_images"),
    path('history/', HistoryView.as_view(), name='history'),
    path('download-report/<int:report_id>/', download_report, name='download_report'),
]