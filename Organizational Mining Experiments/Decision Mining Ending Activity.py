import pathlib
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.transformation.log_to_features import algorithm as log_to_features
from pm4py.objects.log.util import get_class_representation
from sklearn import tree
from pm4py.visualization.decisiontree import visualizer as dectree_visualizer
from pm4py.visualization.petri_net import visualizer

# log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\Event Logs\\running-example.xes")
log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\Final Organization Involved\\final_organization_involved_log_k_2.xes")
data, features = log_to_features.apply(log)

target, classes = get_class_representation.get_class_representation_by_str_ev_attr_value_value(log, "concept:name")
clf = tree.DecisionTreeClassifier()
clf.fit(data, target)
gviz = dectree_visualizer.apply(clf, features, classes)

visualizer.view(gviz)