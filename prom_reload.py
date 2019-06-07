import datetime
import time
import requests  # Install this if you don't have it already.

PROMETHEUS = 'http://localhost:9090/'

query = PROMETHEUS + '-/reload'
print (query)

response_reload = requests.post(PROMETHEUS + '-/reload')
print(response_reload)

reload_url = response_reload.text 

print(response_reload.status_code, response_reload.reason)


#curl -X POST http://localhost:9090/-/reload
