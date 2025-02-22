# admin.py

from django.contrib import admin

from .models import ImgDataset  # sustituir por el nombre de vuestra app

@admin.register(ImgDataset)
class ImgDatasetAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "image",
    )
