from PIL import Image # Organização das imagens
import numpy as np # Manipulação de arrays

from os import listdir # Lista os diretórios existentes
from os.path import isdir # Verifica se o caminho é um diretório
from os.path import join # Junta o caminha em um só

# Esta função retorna um array e organiza imagem
def select_image(filename):
  image = Image.open(filename)
  image = image.convert('RGB')
  image = image.resize((150,150))
  return np.asarray(image)
# Esta função tem os seguintes argumentos:
# diretorio: onde está localizada as imagens de uma determinada classe
# classe: nome da classe que ele deve assumir
# imagens: list de imagens
# label: list das classes 
def load_classes(diretorio, classe, imagens, labels):
  for filename in listdir(diretorio):
    path = join(diretorio, filename)

    try:
      imagens.append(select_image(path))
      labels.append(classe)
    except:
      print(f'Erro ao ler imagem {path}')
  return imagens, labels

# Esta função retorna as imagens e os labels de um determinado diretório
def select_data_set(diretorio):
  imagens = list()
  labels = list()

  for subdir in listdir(diretorio):
    path = join(diretorio, subdir)

    if not isdir(path):
      continue
    imagens, labels = load_classes(path, subdir, imagens, labels)
  return imagens, labels