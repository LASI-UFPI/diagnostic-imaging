from django.shortcuts import render
from django.contrib import messages

from .forms import ImageModelForm
from .models import Image

def index(request):
  if str(request.method) == 'POST':
    form = ImageModelForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      response = result(request)
      return response
    else:
      message = 'Erro ao enviar a imagem, por favor tente novamente!'
      messages.error(request, message)
  else:
    form = ImageModelForm()
  context = {
    'form': form,
  }
  return render(request, 'index.html', context)

def result(request):
  image = Image.objects.all().last().image
  predict_covid = Image.objects.all().last().predict_covid*100
  predict_no_findings = Image.objects.all().last().predict_no_findings*100
  predict_pneumonia = Image.objects.all().last().predict_pneumonia*100
  # O resultado da CNN é dado pelo ultimo dado que entrou no banco de dados, isso pode ocorrer um bug, pensar em um jeito de passar o id do models no post_save para a view
  context = {
    'image': image,
    'predict_covid': predict_covid,
    'predict_no_findings': predict_no_findings,
    'predict_pneumonia': predict_pneumonia,
  }
  return render(request, 'result.html',context)
