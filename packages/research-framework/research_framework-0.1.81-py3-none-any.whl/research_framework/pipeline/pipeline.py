from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.pipeline.base_pipeline import BasePipeline
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container
from research_framework.pipeline.model.pipeline_model import FilterModel, InputFilterModel, PipelineModel
from research_framework.base.utils.grid_seach import generate_combis

from rich import print
import json
import numpy as np

from research_framework.pipeline.pipeline_manager import PipelineManager

@Container.register_pipeline
class FitPredictPipeline(BasePipeline):
    def __init__(self, doc:PipelineModel, project:str):
        print("\n* Pipeline: ")
        self.pipeline:PipelineModel = PipelineManager.fill_pipline_items(doc) 
        print(self.pipeline)
        
        config = {'dataset': self.pipeline.train_input.name}
        for f in self.pipeline.filters:
            config[f.clazz] = f.params
            
        project_hash = Container.fly.hashcode_from_name("->".join(list(map(lambda x: f'({x.clazz}:{x.params})', self.pipeline.filters))))
        Container.global_config.project_name = project
        Container.global_config.run_name = self.pipeline.train_input.name+"->("+project_hash+")"
        Container.init_wandb_logger(
            project=project, 
            name=self.pipeline.train_input.name+"->("+project_hash+")",
            config=config
        )
        
        Container.send_to_logger(message={"dataset": self.pipeline.train_input.name})
        
    def start(self) -> None:
        try:
            train_input = self.pipeline.train_input
            test_input = self.pipeline.test_input
            
            train_f = Container.get_filter_manager(train_input.clazz, train_input.params).predict(data_item=train_input.item)
            if test_input is not None:
                test_f = Container.get_filter_manager(test_input.clazz, test_input.params).predict(data_item=test_input.item)
            
            for f_idx, filter_model in enumerate(self.pipeline.filters):
                filter_manager:BaseFlyManager = Container.get_filter_manager(
                    filter_model.clazz, 
                    filter_model.params, 
                    filter_model.overwrite, 
                    filter_model.store
                )
                
                filter_manager.fit(filter_model.item, train_f)
                
                train_f = filter_manager.predict(train_input.items[f_idx], train_f)
                if test_input is not None:
                    test_f = filter_manager.predict(test_input.items[f_idx], test_f)

            if test_input is None:
                test_f = train_f

            for idx, metric in enumerate(self.pipeline.metrics):
                m_wrapper = Container.get_metric(metric.clazz, metric.params)
                metric.value = m_wrapper.predict(test_f)
                self.pipeline.metrics[idx] = metric
                
        except Exception as ex:
            raise ex
        
    def log_metrics(self) -> None:
        print(self.pipeline.metrics)
        for metric in self.pipeline.metrics:
            Container.send_to_logger(message={metric.clazz: metric.value})

    def finish(self) -> None:
        if not Container.logger is None:
            Container.logger.finish()

        
@Container.register_pipeline
class FitPredictGridSearchPipeline(BasePipeline):
    def __init__(self, doc:PipelineModel, project:str):
        print("\n* Pipeline: ")
        print(doc.model_dump())
        self.pipeline:PipelineModel = doc 
        self.project = project
        
    def start(self) -> None:
        try:
            combis = generate_combis(self.pipeline.filters)
            filter_map = dict(map(lambda x: (x.clazz, x) , self.pipeline.filters))
            pipelines = []
            for combi in combis:
                
                pipeline_model = PipelineModel(
                    name=self.pipeline.name,
                    train_input=InputFilterModel(**self.pipeline.train_input.model_dump()),
                    test_input=InputFilterModel(**self.pipeline.test_input.model_dump()),

                    filters=list(map(lambda itm: FilterModel(
                            clazz=itm[0], 
                            params=itm[1], 
                            overwrite=filter_map[itm[0]].overwrite,
                            store=filter_map[itm[0]].store
                        ), combi.items()
                    )),

                    params=self.pipeline.params,
                    metrics=self.pipeline.metrics 
                )
                
                pipeline = FitPredictPipeline(pipeline_model, self.project)
                pipeline.start()
                pipeline.log_metrics()
                
                pipelines.append(pipeline_model)
                
            for idx, metric in enumerate(self.pipeline.metrics):
                if metric.higher_better:
                    top_pipeline = max(pipelines, key=lambda x: x.metrics[idx].value)
                else:
                    top_pipeline = min(pipelines, key=lambda x: x.metrics[idx].value)
                    
                self.pipeline.metrics[idx] = top_pipeline.metrics[idx]
                
        except Exception as ex:
            raise ex

    def log_metrics(self) -> None: 
        for metric in self.pipeline.metrics:
            print(metric)

    def finish(self) -> None: ...