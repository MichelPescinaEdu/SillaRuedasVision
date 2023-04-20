import cv2
from PIL import Image
import numpy as np
import torch
from custom_types import BoundingBox, Prediction
from typing import Any, List
from torch import Tensor
from torchvision.transforms.functional import to_pil_image, to_tensor
from torchvision.models.detection import RetinaNet, retinanet_resnet50_fpn_v2, RetinaNet_ResNet50_FPN_V2_Weights

class ResNet50:
    device: torch.device
    weights: RetinaNet_ResNet50_FPN_V2_Weights
    model: RetinaNet
    preprocess: Any

    def __init__(self, device = 'cpu', min_conf = 0.5) -> None:
        self.weights = RetinaNet_ResNet50_FPN_V2_Weights.DEFAULT
        self.model = retinanet_resnet50_fpn_v2(weights=self.weights, score_thresh=min_conf)
        self.device = torch.device(device)
        self.model.to(self.device, non_blocking=True)
        # Put the model in inference mode
        self.model.eval()
        # Get the transforms for the model's weights
        self.preprocess = self.weights.transforms()

    def predict(self, img: str | np.ndarray) -> List[Prediction]:
        image = cv2.imread(img) if isinstance(img, str) else img
        imageTensor = self.toTensor(image)
        imageTensorNormalized = self.normalize(imageTensor)

        batch = [self.preprocess(imageTensorNormalized)]
        with torch.no_grad():
            results = self.model(batch)[0]

        labels = labels = [self.weights.meta["categories"][i] for i in results["labels"]]
        scores:List[Tensor] = results['scores']
        boxes:List[Tensor] = results['boxes']    

        predictions: List[Prediction] = []
        for(className, score, box) in zip(labels,scores,boxes):
            predictions.append(
                Prediction(
                    name=className,
                    score=score.item(),
                    box=BoundingBox.fromTensor(box)
                )
            )   

        return predictions


    def toTensor(self, img: np.ndarray) -> Tensor:
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        tensor = to_tensor(pil_image)
        return tensor.to(self.device, non_blocking=True)

    def normalize(self, tensor: Tensor) -> Tensor:
        mn = tensor.min()
        mx = tensor.max()
        mx -= mn

        normalized = ((tensor - mn)/mx) * 255
        return normalized.to(torch.uint8, non_blocking=True)

    def toCVImage(self, tensor: Tensor) -> np.ndarray:
        pilImage = to_pil_image(tensor)
        pilArray = np.array(pilImage)
        return pilArray[:,:,::-1].copy()
