import os
import cv2
import numpy as np
import time
from typing import List, Tuple
from resnet import ResNet50
from custom_types import Prediction

cameras = ['iDS', 'PerfectChoice', 'Realsense']
resultDir = 'ResNet_Results'

resnet = ResNet50()
totalTime = 0
totalPredictions = 0

def findPred(preds: List[Prediction], name: str) -> List[Prediction]:
    predsFound: List[Prediction] = [] 
    for pred in preds:
        if pred['name'] == name:
            predsFound.append(pred)
    return predsFound

def drawPreds(img: np.ndarray, preds: List[Prediction], color: Tuple[int,int,int] = (0, 0, 255), text = True) -> np.ndarray:
    image =  img.copy()
    for pred in preds:
        box = pred['box']
        name = pred['name']
        cv2.rectangle(image, (box.xmin, box.ymin), (box.xmax, box.ymax),
                    color=color, 
                    thickness=2)
        if text:
            cv2.putText(image, name, (box.xmin, box.ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                color=color, 
                thickness=2)

    return image

def formatPredictions(predictions: List[Prediction]) -> list[str]:
    text: List[str] = []
    for prediction in predictions:
        name = prediction['name']
        score = prediction['score']
        box = prediction['box'].asPlainText()
        line = f'{name},{score},{box}\n'
        text.append(line)
    return text    

for camera in cameras:
    for imageName in os.listdir(f'./images/{camera}'):
        currentImage = f'./images/{camera}/{imageName}'
        sceneImage = imageName.split('.')[0]
        print(sceneImage)
        currentImageCV = cv2.imread(currentImage)

        start = time.time()
        predictions = resnet.predict(currentImageCV)
        end = time.time()
        totalTime += end - start
        totalPredictions += 1

        imagePredicted = drawPreds(currentImageCV, predictions)

        resultImageFile = f'./{resultDir}/{camera}/{sceneImage}.jpg'
        cv2.imwrite(resultImageFile, imagePredicted)

        resultfile = open(f'./{resultDir}/{camera}/{sceneImage}.txt', 'w')
        resultfile.writelines(formatPredictions(predictions))
        resultfile.close()
print(f"Average prediction time: {totalTime/totalPredictions}s")