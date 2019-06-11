
import sys
from ruamel.yaml import YAML
import pprint
# import yaml

def yaml_loader(filepath):
	with open(filename,"r") as file_descriptor:
		data = yaml.load(file_descriptor)
	return data

def yaml_dump(filepath,data):
	with open(filename,"w") as file_descriptor:
		yaml.dump(data, file_descriptor)


if __name__ == "__main__":
	filename = "/home/irinarozalio/prometheus_metrics_drop/prometheus/prometheus.yml"
	#d = dict(metric_relabel_configs=[dict(source_labels='[ __name__ ]',regex='my_too_large_metric',action='drop')])
	yaml = YAML()
	data = yaml_loader(filename)
	#pprint.pprint(data['scrape_configs'][0]['metric_relabel_configs'][1]['regex'])
	yaml.dump(data, sys.stdout)
	print ("*************************")
	# print(data['scrape_configs'][0]['metric_relabel_configs'])


	# pprint.pprint(data['scrape_configs'])
	# pprint.pprint(data['scrape_configs'][0])

	metric = "ira"
	for i in data['scrape_configs']:
		# pprint.pprint(i)
	
		if 'metric_relabel_configs' in i.keys():
			if (metric not in i['metric_relabel_configs'][0]['regex']):
				pprint.pprint("YYY=" + i['metric_relabel_configs'][0]['regex'])
				i['metric_relabel_configs'].append(dict(source_labels=[ '__name__' ],regex=metric,action='drop'))
			else:
				print('Metric ' + metric + " already exist.")
		else:
			i['metric_relabel_configs'] = [dict(source_labels=[ '__name__' ],regex=metric,action='drop')]

	print("++++++++++++++++++++++++++++++++++")

	with open(filename, "w") as file:

		yaml.indent(mapping=2)
		yaml.dump(data, file)
		yaml.dump(data, sys.stdout)

	pprint.pprint(data['scrape_configs'][0])


	# if 'metric_relabel_configs' in data['scrape_configs'][0].keys():
	# 	data['scrape_configs'][0]['metric_relabel_configs'].append(dict(source_labels=[ '__name__' ],regex='my_too_large_metric',action='drop'))
	# else:
	# 	data['scrape_configs'][0]['metric_relabel_configs'] = [dict(source_labels=[ '__name__' ],regex='my_too_large_metric',action='drop')]
	# # pprint.pprint(data['scrape_configs'][0])
	# with open(filename, "w") as file:

	# 	yaml.indent(mapping=2)
	# 	yaml.dump(data, file)
	# 	yaml.dump(data, sys.stdout)

