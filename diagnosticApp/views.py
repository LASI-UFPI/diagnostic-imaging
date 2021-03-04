from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from .forms import ImageModelForm
from .models import Image

def index(request):
  if str(request.method) == 'POST':
    form = ImageModelForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Imagem enviada com sucesso.')
      form = ImageModelForm()
    else:
      messages.error(request, 'Erro ao enviar a imagem.')
  else:
    form = ImageModelForm()
  
  context = {
    'form': form
  }
  return render(request, 'index.html', context)
