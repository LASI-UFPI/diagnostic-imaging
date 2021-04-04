from django import forms
from .models import Image

class ImageModelForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ['image']