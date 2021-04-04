import uuid

from django.db import models
from stdimage.models import StdImageField
from django.db.models import signals
from django.conf import settings

import src
from src.classification.train import predictDiagnostic

def get_file_path(instace, filename):
  ext = filename.split('.')[-1]
  filename = f'{uuid.uuid4()}.{ext}'
  return filename

class Base(models.Model):
  created_at = models.DateField('Criado em', auto_now_add=True)
  updated_at = models.DateField('Atualizado em', auto_now=True)
  activated_at = models.BooleanField('Ativo em', default=True)

  class Meta:
    abstract = True


class Image(Base):
  image = StdImageField('Imagem', upload_to=get_file_path, delete_orphans=True)
  predict_covid = models.FloatField('Previsão Covid', null=True, blank=True)
  predict_no_findings = models.FloatField('Previsão Sem Doença', null=True, blank=True)
  predict_pneumonia = models.FloatField('Previsão Pneumonia', null=True, blank=True)

  class Meta:
    verbose_name = 'Imagem'
    verbose_name_plural = 'Imagens'
  
  def __str__(self):
    return f'{self.image}'

def image_post_save(signal, instance, sender, **kwargs):
  signals.post_save.disconnect(image_post_save, sender=Image)

  filenameImage = settings.BASE_DIR/'media'/instance.image.name
  filenameModel = settings.BASE_DIR/'cnndiagnostic'/'model.json'
  filenameWeights = settings.BASE_DIR/'cnndiagnostic'/'model.h5'

  instance.predict_covid, instance.predict_no_findings, instance.predict_pneumonia = predictDiagnostic(filenameImage, filenameModel, filenameWeights)

  instance.save()
  signals.post_save.connect(image_post_save, sender=Image)  

signals.post_save.connect(image_post_save, sender=Image)

