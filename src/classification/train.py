from .datasetImage import select_data_set
from pathlib import Path

import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.applications import VGG19

BASE_DIR = Path(__file__).resolve().parent.parent.parent
path_dataset = BASE_DIR/'ImageDataSet'

class TrainClass():
  def __init__(self):
    self.batch_size   = 32
    self.input_shape  = (150, 150, 3)
    self.random_states = 42
    self.alpha        = 1e-5
    self.epoch        = 60

  # Essa função busca as imagens e os labels no banco de dados  
  def normalize(self): 
    imagens, labels = select_data_set(path_dataset)
    imagens = np.array(imagens)/255 # normaliza as imagens e colocar em forma de array
    labels = np.array(labels)
    lb = LabelBinarizer()
    labels = lb.fit_transform(labels) # transforma os labels em binário
    return imagens, labels

  # Essa função será usada para salvar os callbacks enquanto faz o treinamento
  def checkpointFunction(self):
    filepath = 'tranferlearning_weights.hdf5'
    checkpoint = ModelCheckpoint(filepath,monitor='val_acc',verbose=1, save_best_only=True,mode='max')
    lr_reduce = ReduceLROnPlateau(monitor='val_acc',factor=0.1, min_delta=self.alpha, patience=5, verbose=1)
    callbacks = [checkpoint, lr_reduce]
    return callbacks
    
  # Função de treinamento
  def train(self):
    imagens, labels = self.normalize()
    
    (trainX, testX, trainY, testY) = train_test_split(imagens, labels, test_size=0.20, stratify=labels, random_state=self.random_states) # separa os dados em treinamento e teste

    conv_base = VGG19(weights='imagenet',include_top=False, input_shape=self.input_shape) # pega o modelo da CNN VGG19

    # Esse bloco tem como função setar como treinável somento o bloco 4 e 5 da VGG19
    conv_base.trainable = True
    set_trainable = False
    
    for layer in conv_base.layers:
      if layer.name == 'block4_conv4':
        set_trainable = True
      if set_trainable:
        layer.trainable = True
      else:
        layer.trainable = False
    
    return conv_base.summary() 