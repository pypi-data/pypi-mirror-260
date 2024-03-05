from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.base.flyweight.base_flyweight import BaseFlyweight

from typing import Dict, Any, Optional
from rich import print
from research_framework.flyweight.model.item_model import ItemModel

class FitPredictFlyManager(BaseFlyManager):
    def __init__(self, wrapper: BaseWrapper, fly: BaseFlyweight, store:bool, overwrite:bool):
        self.wrapper: BaseWrapper = wrapper
        self.fly: BaseFlyweight = fly
        self.filter_item:ItemModel = None
        self.store:bool = store
        self.overwrite:bool = overwrite
        
    def fit(self, filter_item:ItemModel, data:Any):
        print("---------------------[Filter Training]----------------------------")
        print(f"Trained_filter_name -> {filter_item.name}")
        print(f'Trained_filter_hashcode -> {filter_item.hash_code}')
        filter_trained_item = self.fly.get_item(filter_item.hash_code)
        print(filter_trained_item)
        print("-------------------------------------------------")
        if filter_trained_item is None or self.overwrite:
            self.wrapper.fit(data)
            
            if self.store:
                if filter_trained_item is None:
                    if not self.fly.set_item(filter_item, self.wrapper.plugin):
                        raise Exception("Couldn't save item")
                else:
                    if not self.fly.set_item(filter_item, self.wrapper.plugin, self.overwrite):
                        raise Exception("Couldn't save item")
        else:
            self.wrapper = lambda : self.fly.wrap_plugin_from_cloud(filter_trained_item.params)
            print(f"* Wrapping data -> {filter_item.hash_code}")
        
        filter_item.stored = True
        self.filter_item = filter_item
            
                
    def predict(self, data_item:ItemModel, data:Any):
        if self.filter_item is None:
            raise Exception("Model not trained, call fit() before calling predict()!")
        else:
            print("-------------------------------------------------")
            print(f"Data_name -> {data_item.name}")
            print(f'Hash_code -> {data_item.hash_code}')
            print(data_item)
            print("-------------------------------------------------")
            stored_item = self.fly.get_item(data_item.hash_code)
            if stored_item is None or self.overwrite:
                
                if callable(self.wrapper) and self.wrapper.__name__ == "<lambda>":
                    self.wrapper = self.wrapper()
                
                data = self.wrapper.predict(data)
                
                if self.store:
                    if stored_item is None:
                        if not self.fly.set_item(data_item, data):
                            raise Exception("Couldn't save item")
                    else:
                        if not self.fly.set_item(data_item, data, self.overwrite):
                            raise Exception("Couldn't save item")
                
            else:
                print(f"* lambda data -> {data_item.hash_code}")
                data = lambda : self.fly.get_data_from_item(data_item)
                data_item.stored = True
            
            return data
                
class PassThroughFlyManager(BaseFlyManager):
    def __init__(self,  wrapper: BaseWrapper, fly: BaseFlyweight, store:bool, overwrite:bool, *args, **kwargs):
        self.wrapper: BaseWrapper = wrapper
        self.fly: BaseFlyweight = fly
        self.hashcode:Optional[str] = None
        self.store:bool = store
        self.overwrite:bool = overwrite
        
    def fit(self, *args, **kwargs): ...
        
    def predict(self, data_item:ItemModel, data):
        print("-------------------------------------------------")
        print(f"Data_name -> {data_item.name}")
        print(f'Hash_code -> {data_item.hash_code}')
        stored_item = self.fly.get_item(data_item.hash_code)
        print(stored_item)
        print("-------------------------------------------------")
        if stored_item is None or self.overwrite:            
            data = self.wrapper.predict(data)
            
            if self.store:
                if stored_item is None:
                    if not self.fly.set_item(data_item, data):
                        raise Exception("Couldn't save item")
                else:
                    if not self.fly.set_item(data_item, data, self.overwrite):
                        raise Exception("Couldn't save item")
                    
        else:
            print(f"* lambda data -> {data_item.hash_code}")
            data = lambda : self.fly.get_data_from_item(data_item)
            data_item.stored = True
        
        return data
    
class InputFlyManager(BaseFlyManager):
    def __init__(self, wrapper: BaseWrapper, fly: BaseFlyweight, store:bool, overwrite:bool, *args, **kwargs):
        self.wrapper: BaseWrapper = wrapper
        self.fly: BaseFlyweight = fly
        self.store:bool = store
        self.overwrite:bool = overwrite
        
    def fit(self, *args, **kwargs): ...
    
    
    def predict(self, data_item:ItemModel, *args, **kwargs):
        stored_item = self.fly.get_item(data_item.hash_code)
        
        if stored_item is None or self.overwrite:
            data = self.wrapper.predict(None)
            
            if self.store:
                if data_item is None:
                    if not self.fly.set_item(data_item, data):
                        raise Exception("Couldn't save item")
                else:
                    if not self.fly.set_item(data_item, data, self.overwrite):
                        raise Exception("Couldn't save item")
        else:
            data = lambda: self.wrapper.predict(None)
            data_item.stored = True
        
        return data
    
    
class WandbSeepsFlyManager(BaseFlyManager):
    def __init__(self, wrapper: BaseWrapper, fly: BaseFlyweight,store:bool, overwrite:bool, *args, **kwargs):
        self.wrapper: BaseWrapper = wrapper
        self.fly: BaseFlyweight = fly
        self.filter_item:ItemModel = None
        self.store = store
        self.overwrite = overwrite
        
    def fit(self, filter_item:ItemModel, data):
        print("---------------------[Prev data stored?]--------------------------")
        if not filter_item.prev_model.stored:
            if not self.fly.set_item(filter_item.prev_model, data):
                raise Exception("Couldn't save item")
            
        print("---------------------[Filter Training]----------------------------")
        print(f"Trained_filter_name -> {filter_item.name}")
        print(f'Trained_filter_hashcode -> {filter_item.hash_code}')
        filter_trained_item = self.fly.get_item(filter_item.hash_code)
        print(filter_trained_item)
        
        if filter_trained_item is None or self.overwrite:
            self.wrapper.fit(filter_item.prev_model, overwrite=True)
            
            if not self.fly.set_item(filter_item, self.wrapper.plugin):
                raise Exception("Couldn't save item")
            
            self.filter_item = filter_item
        else:
            self.wrapper = self.fly.wrap_plugin_from_cloud(filter_trained_item.params)
            self.wrapper.fit(filter_item.prev_model, overwrite=False)
            self.filter_item = filter_trained_item
        
        
    
    def predict(self, data_item:ItemModel, data):
        if self.filter_item is None:
            raise Exception("Model not trained, call fit() before calling predict()!")
        else:
            print("-------------------------------------------------")
            print(f"Data_name -> {data_item.name}")
            print(f'Hash_code -> {data_item.hash_code}')
            print(data_item)
            print("-------------------------------------------------")
            stored_item = self.fly.get_item(data_item.hash_code)
            if stored_item is None or self.overwrite:
                
                if callable(self.wrapper) and self.wrapper.__name__ == "<lambda>":
                    self.wrapper = self.wrapper()
                
                data = self.wrapper.predict(data)
                
                if self.store:
                    if stored_item is None:
                        if not self.fly.set_item(data_item, data):
                            raise Exception("Couldn't save item")
                    else:
                        if not self.fly.set_item(data_item, data, self.overwrite):
                            raise Exception("Couldn't save item")
                
            else:
                print(f"* lambda data -> {data_item.hash_code}")
                data = lambda : self.fly.get_data_from_item(data_item)
                data_item.stored = True
            
            return data
        
        
class DummyFlyManager(BaseFlyManager):
    def __init__(self, wrapper: BaseWrapper, fly: BaseFlyweight, *args, **kwargs):
        self.wrapper: BaseWrapper = wrapper
        self.fly: BaseFlyweight = fly

    def fit(self, data_item:ItemModel, data):
        self.wrapper.fit(data)
        
        print("-------------------------------------------------")
        print(f"data_hashcode -> {data_item.hash_code}")
        print(f'filter_name -> {data_item.name}')
        print("-------------------------------------------------")
    
    def predict(self, data_item:ItemModel, data):
        data = self.wrapper.predict(data)
        
        print("-------------------------------------------------")
        print(f"data_hashcode -> {data_item.hash_code}")
        print(f'filter_name -> {data_item.name}')
        print("-------------------------------------------------")
        
        return data
      
class OutputFlyManager(BaseFlyManager):
    def __init__(self, wrapper:BaseWrapper):
        self.wrapper: BaseWrapper = wrapper
        
    def fit(self, *args, **kwargs): ...
    
    def predict(self, data):
        return self.wrapper.predict(data)

 