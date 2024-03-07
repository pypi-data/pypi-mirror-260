from research_framework.base.container.model.bind_model import BindModel
from research_framework.base.pipeline.base_pipeline import BasePipeline
from research_framework.container.container import Container
from research_framework.flyweight.flyweight_manager import FitPredictFlyManager, WandbSeepsFlyManager
# from research_framework.pipeline.pipeline import FitPredictPipeline, FitPredictGridSearchPipeline
from research_framework.container.model.global_config import GlobalConfig
from research_framework.flyweight.flyweight import FlyWeight
from pydantic import BaseModel
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.pipeline.model.pipeline_model import PipelineModel
from research_framework.base.storage.base_storage import BaseStorage
from research_framework.storage.local_storage import LocalStorage

import json
from fastapi.encoders import jsonable_encoder



class PipelineManager:
    
    @staticmethod
    def init_fly(fly):
        if Container.fly is None:
            Container.fly = fly()
    
    @staticmethod
    def start_pipeline(project:str, pl_conf:BaseModel, log:bool=False, store:bool=True, overwrite:bool=False, storage:BaseStorage=LocalStorage()):
        PipelineManager.init_fly(FlyWeight)
        
        Container.storage = storage
        Container.global_config = GlobalConfig(
            log=log,
            overwrite=overwrite,
            store=store
        )
        
        pipeline:BasePipeline = Container.PIPELINES[pl_conf._clazz](pl_conf, project)
        pipeline.start()
        pipeline.log_metrics()
        return pipeline
    
    @staticmethod
    def fill_pipline_items(config:PipelineModel):
        PipelineManager.init_fly(FlyWeight)
        
        train_item:ItemModel = Container.fly.item_from_name(config.train_input.name)
        config.train_input.item = train_item
        
        if config.test_input is not None:
            test_item:ItemModel = Container.fly.item_from_name(config.test_input.name)
            config.test_input.item = test_item
        
        for f in config.filters:
            bind: BindModel = Container.BINDINGS[f.clazz]   
            
            if bind.manager in [FitPredictFlyManager, WandbSeepsFlyManager]:
                filter_item:ItemModel = Container.fly.item_from_name_and_prev(f'{f.clazz}{jsonable_encoder(f.params)}[Trained]({train_item.hash_code})', train_item)
            else:
                filter_item:ItemModel = Container.fly.item_from_name(f'{f.clazz}{jsonable_encoder(f.params)}[-]')
            
            f.item = filter_item
                
            train_item = Container.fly.item_from_name_and_prev(f'{train_item.name} -> {filter_item.name}', train_item)
            config.train_input.items.append(train_item)
            
            if config.test_input is not None:
                test_item = Container.fly.item_from_name_and_prev( f'{test_item.name} -> {filter_item.name}', test_item)
                config.test_input.items.append(test_item)
            
        
        return config
    