from abc import ABC, abstractmethod
from typing import Any
from research_framework.flyweight.model.item_model import ItemModel

class BaseFlyManager(ABC):
    @abstractmethod
    def fit(self, filter_item:ItemModel, data:Any): ...
    @abstractmethod
    def predict(self, filter_item:ItemModel,  data:Any): ...