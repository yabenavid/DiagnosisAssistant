# segmentation/apps.py
from django.apps import AppConfig
import os
import sys
from django.conf import settings

class SegmentationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'segmentation'

    def ready(self):
        # Prevent the model from loading in the first process (the autoreloader)
        is_main_process = os.environ.get('RUN_MAIN') == 'true' or 'gunicorn' in sys.argv or 'uwsgi' in sys.argv

        if not is_main_process:
            return

        from .models import SamImageSegmenter
        global segmenter_instance

        print("Cargando modelo SAM...")
        segmenter_instance = SamImageSegmenter()
        # segmenter_instance = None
        print("Modelo SAM cargado exitosamente.")
