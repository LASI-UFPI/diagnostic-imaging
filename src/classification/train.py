from .datasetImage import select_data_set
from pathlib import Path

import numpy as np
from sklearn.preprocessing import LabelBinarizer

BASE_DIR = Path(__file__).resolve().parent.parent.parent
path_dataset = BASE_DIR/'ImageDataSet'

class TrainClass():
  batch_size   = 32
  input_shape  = (150, 150, 3)
  random_state = 42
  alpha        = 1e-5
  epoch        = 60
  def normalize():
    imagens, labels = select_data_set(path_dataset)
    imagens = np.array(imagens)/255
    labels = np.array(labels)
    lb = LabelBinarizer()
    labels = lb.fit_transform(labels)
    return labels # Esta função não tem retorno, por enquanto é para teste esse retorno