from src.classification.train import TrainClass
from pathlib import Path

train = TrainClass()
BASE_DIR = Path(__file__).resolve().parent

train.train() # comando para executar o treinamento, comentar caso não seja a necessidade 

train.test() # comando para executar o test, comentar caso não seja a nesseidade 

# Bloco a seguir é o código utilizado para teste para previsão do resultado
#filenameModel = BASE_DIR/'cnndiagnostic'
#filenameImage = BASE_DIR/'test.jpeg'
#print(train.predictDiagnostic(filenameImage,filenameModel))

# para rodar basta executar no terminal o comando:
# python server.py