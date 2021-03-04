from .datasetImage import select_data_set
from pathlib import Path
from PIL import Image

import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.applications import VGG19
from tensorflow.keras import models, layers

import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix

BASE_DIR = Path(__file__).resolve().parent.parent.parent
path_dataset = BASE_DIR/'ImageDataSet'

class TrainClass():
  def __init__(self):
    self.batch_size   = 32
    self.input_shape  = (150, 150, 3) # esse valor tem que condizer com image.resize do arquivo datasetImage.py
    self.random_states = 42 
    self.alpha        = 1e-5
    self.epoch        = 10 # não colocar muitas épocas max 100

  # Essa função busca as imagens e os labels no banco de dados  
  def normalize(self): 
    imagens, labels = select_data_set(path_dataset)
    imagens = np.array(imagens)/255 # normaliza as imagens e colocar em forma de array
    labels = np.array(labels)
    lb = LabelBinarizer()
    labels = lb.fit_transform(labels) # transforma os labels em binário
    
    (trainX, testX, trainY, testY) = train_test_split(imagens, labels, test_size=0.20, stratify=labels, random_state=self.random_states) # separa os dados em treinamento e teste

    return trainX, testX, trainY, testY

  # Essa função será usada para salvar os callbacks enquanto faz o treinamento, além de fazer o ajuste da taxa de apredizagem
  def checkpointFunction(self):
    filepath = 'tranferlearning_weights.hdf5'
    checkpoint = ModelCheckpoint(filepath,monitor='val_acc',verbose=1, save_best_only=True,mode='max')
    lr_reduce = ReduceLROnPlateau(monitor='val_acc',factor=0.1, min_delta=self.alpha, patience=5, verbose=1)# ajuste lr
    callbacks = [checkpoint, lr_reduce]
    return callbacks
    
  # Função de treinamento
  def train(self):
    trainX, testX, trainY, testY = self.normalize() # recebe os dados 
    callbacks = self.checkpointFunction() #recebe os callbacks

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
    
    # bloco referente as camadas do model
    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.BatchNormalization())
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.6))
    model.add(layers.Dense(3, activation='softmax'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    # treinamento da CNN
    history = model.fit(
      trainX, 
      trainY, 
      batch_size=self.batch_size,
      steps_per_epoch=len(trainX)//self.batch_size, 
      validation_data=(testX, testY), 
      validation_steps=len(testX)//self.batch_size,
      callbacks=callbacks, 
      epochs=self.epoch,
      )

    model.save('cnndiagnostic') # salvar os parâmetros da CNN

    message_sucess = f'Treinamento realizado com sucesso!!' #Mensagem de sucesso na tela

    return message_sucess 
  
  # Função de test da CNN
  def test(self):
    trainX, testX, trainY, testY = self.normalize() # busca os dados
    filename = BASE_DIR/'cnndiagnostic' # caminho da cnn treinada
    model = models.load_model(filename) # atribui o model da cnn treinada

    pred = model.predict_classes(testX) # função para prever as classes a partir do vetor de testX
    y_true = np.argmax(testY,axis = 1) # saída para fins de comparação da cnn

    cm = confusion_matrix(y_true, pred) # Matriz de confusão da CNN
    total = sum(sum(cm))
    acc = (cm[0, 0] + cm[1, 1]+cm[2, 2]) / total
    sensitivity_covid = cm[0, 0] / (cm[0, 0] + cm[0, 1] + cm[0, 2])
    specificity_nocovid = cm[1, 1] / (cm[1, 0] + cm[1, 1] + cm[1, 2])
    sensitivity_pneumonia = cm[2, 2] / (cm[2, 0] + cm[2, 1] + cm[2, 2])
    # Posição 0: Covid-19
    # Posição 1: No_findings
    # Posição 2: Pneumonia 
    
    # mesagem de resposta na tela
    print("Acurácia: {:.4f}".format(acc))
    print("Sensitividade ao covid: {:.4f}".format(sensitivity_covid))
    print("Sensitividade a pneumonia: {:.4f}".format(sensitivity_pneumonia))
    print("Especificidade: {:.4f}".format(specificity_nocovid))

    # gráfico da matriz de confusão
    fig, ax = plot_confusion_matrix(conf_mat=cm ,  figsize=(5, 5))
    plt.show()
  
  # Função para retornar o resultado a partir de um modelo de CNN
  def predictDiagnostic(self, filenameImage, filenameModel):
    filenameImage = BASE_DIR/filenameImage
    filenameModel = BASE_DIR/filenameModel
    image = Image.open(filenameImage) # busca da imagem
    image = image.convert('RGB') # converção para RBG
    image = image.resize((150,150)) # organização para o shape de entrada
    image = np.array(image, ndmin=4)/255 # normalização da imagem

    model = models.load_model(filenameModel) # busca o modelo da CNN

    result_predict = int(model.predict_classes(image)) # faz a previsão e converte para inteiro
    
    # Bloco para verificação do resultado
    if result_predict == 0:
      result = 'COVID-19'
    elif result_predict == 1:
      result = 'NENHUMA DETECÇÃO'
    elif result_predict == 2:
      result = 'PNEUMONIA'
    else:
      result = 'Erro de processamento'
    
    return result
