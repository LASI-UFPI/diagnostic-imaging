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
      message = f'Imagem enviada com sucesso e o resultado dado pela CNN é: {Image.objects.all().last().diagnostic}'
      # O resultado da CNN é dado pelo ultimo dado que entrou no banco de dados, isso pode ocorrer um bug, pensar em um jeito de passar o id do models no post_save para a view
      messages.success(request=request, message=message)
      form = ImageModelForm()
    else:
      messages.error(request, 'Erro ao enviar a imagem.')
  else:
    form = ImageModelForm()
  
  context = {
    'form': form
  }
  return render(request, 'index.html', context)
