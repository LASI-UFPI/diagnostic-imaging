from PIL import Image
import numpy as np
from tensorflow.keras import models

def predictDiagnostic(filenameImage, filenameModel, filenameWeights):
  image = Image.open(filenameImage) # busca da imagem
  image = image.convert('RGB') # converção para RBG
  image = image.resize((360,360)) # organização para o shape de entrada
  image = np.array(image, ndmin=4)/255 # normalização da imagem

  json_file = open(filenameModel, 'r')
  loaded_model_json = json_file.read()
  json_file.close()
  model = models.model_from_json(loaded_model_json)
  # load weights into new model
  model.load_weights(filenameWeights)

  result_predict = model.predict(image) # faz a previsão e converte para inteiro
  print(result_predict)

  result_covid = float(result_predict[0][0])
  result_no_findings =  float(result_predict[0][1])
  result_pneumonia = float(result_predict[0][2])

  return result_covid, result_no_findings, result_pneumonia
