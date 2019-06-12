import datetime
import time
import requests 
import sys
from ruamel.yaml import YAML
import pprint


def change_prom_yaml(filepath,metric_name,prom_target):
	yaml = YAML()
	# data = yaml_loader(filepath)
	with open(filename,"r") as file_descriptor:
		data = yaml.load(file_descriptor)
	#yaml.dump(data, sys.stdout)

	for i in data['scrape_configs']:
		targ = i['static_configs'][0]['targets']
		if prom_target in targ:
			if 'metric_relabel_configs' in i.keys():
				if ( metric_name not in i['metric_relabel_configs'][0]['regex']):
					i['metric_relabel_configs'].append(dict(source_labels=[ '__name__' ],regex=metric_name,action='drop'))
				else:
					print('Metric ' + metric_name + " already exist.")
			else:
				i['metric_relabel_configs'] = [dict(source_labels=[ '__name__' ],regex=metric_name,action='drop')]

			with open(filename, "w") as file:
				yaml.indent(mapping=2)
				yaml.dump(data, file)
				# yaml.dump(data, sys.stdout)

def prom_yam_target(filepath):
	yaml = YAML()
	targets = []
	with open(filename,"r") as file_descriptor:
		data = yaml.load(file_descriptor)
	for i in data['scrape_configs']: 
		target = i['static_configs'][0]['targets']
		targets.append(i['static_configs'][0]['targets'])
	return(targets)


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
	targets = prom_yam_target(filename)

	
	for i in targets:
		prom_list = {}
		prom_target = str(i).split("'")[1]
		tunix_5 = time.mktime((datetime.datetime.now() - datetime.timedelta(minutes=24*60)).timetuple())
		tunix_now = time.mktime(datetime.datetime.now().timetuple())

		instance = 'count({instance="' + prom_target + '"})  by  (__name__)'
		response_now = requests.get(prometheus + '/api/v1/query',
			params={
					'query': instance,
					'time': tunix_now})		
		results_now = response_now.json()['data']['result']
		response_5 = requests.get(prometheus + '/api/v1/query',
			params={
					'query': instance,
					'time': tunix_5})
		# print(response_5.json())
		# print(response_5.url)
		# quit()
		results_5 = response_5.json()['data']['result']

		print("******************************")
		print("Starting Target=" + prom_target)
		# print(response_now.url)

		# prom_list = {}
		for result_now in results_now:
			metric_name = result_now['metric']['__name__']
			metric_values = int(result_now['value'][1])
			prom_list[metric_name] = {'now': metric_values, 'last_5': None}

		# print(results_5)
		for result_5 in results_5:
			metric_name = result_5['metric']['__name__']
			# print(metric_name)
			metric_values = int(result_5['value'][1])
			if metric_name in prom_list.keys():
				prom_list[metric_name]['last_5'] = metric_values
		# quit()
		# pprint.pprint(prom_list)
		for k, v in prom_list.items():
			if v['now'] != v['last_5'] and v['last_5'] and v['now']:
				perc = abs(float(((v['now'] - v['last_5']) * 100 ) / v['now']))				
				if perc > 30:
					# print(perc)
					print(k, v)
					#print(prom_list[metric_name])
					# prom_target = '35.222.74.15:5000'
					# metric_name='fake_aborting'
					change_prom_yaml(filename,k,prom_target)
		# quit()
	prom_reload(prometheus)
	
	