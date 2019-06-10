import datetime
import time
import requests 
import sys
from ruamel.yaml import YAML
import pprint
import datetime
import time
import requests

# def yaml_loader(filepath):
# 	with open(filename,"r") as file_descriptor:
# 		data = yaml.load(file_descriptor)
# 	return data

# def yaml_dump(filepath,data):
# 	with open(filename,"w") as file_descriptor:
# 		yaml.dump(data, file_descriptor)

def change_prom_yaml(filepath,metric_name):
	yaml = YAML()
	# data = yaml_loader(filepath)
	with open(filename,"r") as file_descriptor:
		data = yaml.load(file_descriptor)
	#yaml.dump(data, sys.stdout)

	for i in data['scrape_configs']:
		pprint.pprint(str(i['job_name']))
		if 'metric_relabel_configs' in data['scrape_configs'][0].keys():
			pprint.pprint(data['scrape_configs'][0])
			# if metric_name in data['scrape_configs'][0]['metric_relabel_configs'][1]['regex']:
				#data['scrape_configs'][0]['metric_relabel_configs'].append(dict(source_labels=[ '__name__' ],regex='my_too_large_metric',action='drop'))
			data['scrape_configs'][0]['metric_relabel_configs'].append(dict(source_labels=[ '__name__' ],regex=metric_name,action='drop'))
		else:
			pprint.pprint(data['scrape_configs'][0])
			#data['scrape_configs'][0]['metric_relabel_configs'] = [dict(source_labels=[ '__name__' ],regex='my_too_large_metric',action='drop')]
			data['scrape_configs'][0]['metric_relabel_configs'] = [dict(source_labels=[ '__name__' ],regex=metric_name,action='drop')]
		print(metric_name)
		with open(filepath, "w") as file:
			yaml.indent(mapping=2)
			yaml.dump(data, file)
			#yaml.dump(data, sys.stdout)

def prom_reload(prometheus):
	query = prometheus + '-/reload'
	print (query)
	response_reload = requests.post(prometheus + '-/reload')
	print(response_reload)
	reload_url = response_reload.text 
	print(response_reload.status_code, response_reload.reason)

if __name__ == "__main__":
	prometheus = 'http://localhost:9090/'
	filename = "/home/irinarozalio/prometheus_metrics_drop/prometheus/prometheus.yml"

	end_of_month = datetime.datetime.today().replace(day=1).date()
	ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	tz_5 = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%SZ')
	tz_now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
	tunix_5 = time.mktime((datetime.datetime.now() - datetime.timedelta(minutes=5)).timetuple())
	tunix_now = time.mktime(datetime.datetime.now().timetuple())

	response_now = requests.get(prometheus + '/api/v1/query',
		params={
				'query': 'topk(10, count by (__name__)({__name__=~".+"}))',
				'time': tunix_now})
	results_now = response_now.json()['data']['result']

	response_5 = requests.get(prometheus + '/api/v1/query',
		params={
				'query': 'topk(10, count by (__name__)({__name__=~".+"}))',
				'time': tunix_5})
	results_5 = response_5.json()['data']['result']

	for result_5 in results_5:
		for result_now in results_now:
			metric_name_5 = result_5['metric']['__name__']
			metric_values_5 = int(result_5['value'][1])
			metric_name = result_now['metric']['__name__']
			metric_values = int(result_now['value'][1])
			p = abs(float(100 - ((metric_values_5 * 100)/metric_values)))
			if (metric_name_5 == metric_name) and (p < 0.6):
				print(p)
				print(metric_name, metric_values)
	metric_name="irinarozalio1"
	#d = dict(metric_relabel_configs=[dict(source_labels='[ __name__ ]',regex='my_too_large_metric',action='drop')])
	change_prom_yaml(filename,metric_name)
	prom_reload(prometheus)
	