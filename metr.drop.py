import datetime
import time
import requests  
PROMETHEUS = 'http://localhost:9090/'


end_of_month = datetime.datetime.today().replace(day=1).date()
ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
tz_5 = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%SZ')
tz_now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
tunix_5 = time.mktime((datetime.datetime.now() - datetime.timedelta(minutes=5)).timetuple())
tunix_now = time.mktime(datetime.datetime.now().timetuple())


response_now = requests.get(PROMETHEUS + '/api/v1/query',
	params={
			'query': 'topk(10, count by (__name__)({__name__=~".+"}))',
			'time': tunix_now})
results_now = response_now.json()['data']['result']

response_5 = requests.get(PROMETHEUS + '/api/v1/query',
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

	