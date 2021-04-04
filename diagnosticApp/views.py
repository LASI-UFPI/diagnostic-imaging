from django.shortcuts import render
from django.contrib import messages

from .forms import ImageModelForm
from .models import Image

def index(request):
  if str(request.method) == 'POST':
    form = ImageModelForm(request.POST, request.FILES)
    if form.is_valid():
      new_image = form.save()
      context = {'id': new_image.pk}
      response = result(request,context)
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

def result(request, newContext):
  imageObject = Image.objects.get(pk=newContext.get('id'))
  image = imageObject.image
  predict_covid = imageObject.predict_covid*100
  predict_no_findings = imageObject.predict_no_findings*100
  predict_pneumonia = imageObject.predict_pneumonia*100
  context = {
    'image': image,
    'predict_covid': predict_covid,
    'predict_no_findings': predict_no_findings,
    'predict_pneumonia': predict_pneumonia,
  }
  return render(request, 'result.html',context)
