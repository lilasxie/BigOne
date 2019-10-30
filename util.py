from datetime import datetime, timedelta
import time

def formattime2datetime(utc, hours = 8):
	'''
	returns local time as datetime object, default utc -> beijing
	'''
	utc_format = '%Y-%m-%dT%H:%M:%SZ'
	utc_time = datetime.strptime(utc, utc_format)
	local_time = utc_time + timedelta(hours = hours)
	return local_time

local_time = formattime2datetime('2019-10-25T15:22:52Z')
print(local_time.date())
print(datetime.now())
if local_time.date() < datetime.now().date():
	print('OK')
else:
	print('oops')
print(datetime.now().date())