from typing import List, TypedDict
from torch import Tensor

ClassList = List[str]

class BoundingBox:
    xmin: int
    ymin: int
    xmax: int
    ymax: int
    area: float

    def __init__(
        self, 
        xmin: int, ymin: int, 
        xmax: int, ymax: int
    ):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        width = xmax - xmin
        height = ymax - ymin
        self.area = abs(width * height)

    @classmethod
    def fromList(cls, box: List[float]):
        return cls(box[0], box[1], box[2], box[3])

    @classmethod
    def fromTensor(cls, box: Tensor):
        tensorList = box.tolist()
        intlist = map(int, tensorList)
        return cls.fromList(list(intlist))

    def __str__(self) -> str:
        return f'({self.xmin},{self.ymin}),({self.xmax},{self.ymax})'
    
    def asPlainText(self) -> str:
        return f'{self.xmin},{self.ymin},{self.xmax},{self.ymax}'

class ImageSize:
    width: int
    height: int
    depth: int

    def __init__(self,  width: int, height: int, depth: int) -> None:
        self.width = width
        self.height = height
        self.depth = depth

    def __str__(self) -> str:
        return f'width: {self.width} height: {self.height} depth: {self.depth}'    

class Prediction(TypedDict):
    name: str
    box: BoundingBox
    score: float