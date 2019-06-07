
import sys
from ruamel.yaml import YAML
import yaml

def yaml_loader(filepath):
	with open(filename,"r") as file_descriptor:
		data = yaml.load(file_descriptor)
	return data

def yaml_dump(filepath,data):
	with open(filename,"w") as file_descriptor:
		yaml.dump(data, file_descriptor)

# d = dict(metric_relabel_configs=['source_labels:[ __name__ ]'],regex='my_too_large_metric',action='drop')        
# d = dict(metric_relabel_configs=dict(metric_relabel_configs=['source_labels:[ __name__ ]'],regex='my_too_large_metric',action='drop'))
# d = dict(metric_relabel_configs=dict(source_labels='[ __name__ ]',regex='my_too_large_metric',action='drop'))
#d = dict(c=[dict(b=2,d=4)])
#d = [dict(b=2), [3, 4]]


if __name__ == "__main__":
	filename = "/home/irinarozalio/prometheus_metrics_drop/prometheus/prometheus.yml"
	d = dict(metric_relabel_configs=[dict(source_labels='[ __name__ ]',regex='my_too_large_metric',action='drop')])
	yaml = YAML()

	with open(filename, "a") as file:
		yaml.indent(mapping=3, sequence=6, offset=2)
		yaml.dump(d, file)
		yaml.dump(d, sys.stdout)
