from django.urls import path
from .views import evaluate_images, download_report, send_report_to_emails, HistoryView

urlpatterns = [
    path("evaluate-images/", evaluate_images, name="evaluate_images"),
    path('history/', HistoryView.as_view(), name='history'),
    path('history/<int:report_id>/send/', send_report_to_emails, name='send-report'),
    path('download-report/<int:report_id>/', download_report, name='download_report'),
]