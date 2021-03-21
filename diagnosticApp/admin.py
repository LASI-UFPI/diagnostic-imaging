from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
  list_display = ('image', 'predict_covid', 'predict_no_findings', 'predict_pneumonia', 'created_at', 'updated_at', 'activated_at')
