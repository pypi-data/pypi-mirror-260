from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.container.container import Container
from research_framework.flyweight.flyweight_manager import OutputFlyManager
from research_framework.plugins.wrappers import MetricWrapper

from sklearn.metrics import davies_bouldin_score, silhouette_score, calinski_harabasz_score, \
    adjusted_rand_score, rand_score, normalized_mutual_info_score, homogeneity_score, completeness_score, \
    v_measure_score, homogeneity_completeness_v_measure, precision_score, recall_score, f1_score
    
@Container.bind(OutputFlyManager, MetricWrapper)
class Silhouette(BasePlugin):
    def fit(self, *args, **kwargs): ...
    def predict(self, y, predicted):
        return silhouette_score(predicted, y)

@Container.bind(OutputFlyManager, MetricWrapper)
class F1(BasePlugin): 
    def fit(self, *args, **kwargs): ...
    def predict(self, y, predicted):
        return f1_score(y, predicted)

@Container.bind(OutputFlyManager, MetricWrapper)
class Precision(BasePlugin):
    def fit(self, *args, **kwargs): ...
    def predict(self, y, predicted):
        return precision_score(y, predicted)


@Container.bind(OutputFlyManager, MetricWrapper)
class Recall(BasePlugin):
    def fit(self, *args, **kwargs): ...
    def predict(self, y, predicted):
        return recall_score(y, predicted)