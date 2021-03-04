import uuid
from django.db import models
from stdimage.models import StdImageField

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
  DIAGNOSTIC_CHOICES = (
    ('covid','COVID'),
    ('no-deteccion','SEM DETECÇAO'),
    ('pneumonia','PNEUMONIA'),
  )
  image = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb':{'width': 360, 'height': 360, 'crop': True}}, delete_orphans=True)
  diagnostic = models.CharField('Diagnóstico',null=True, blank=True, max_length=15, choices=DIAGNOSTIC_CHOICES)

  class Meta:
    verbose_name = 'Imagem'
    verbose_name_plural = 'Imagens'
  
  def __str__(self):
    return f'{self.diagnostic}: {self.image}'
