#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
import task, fun
import time
import socket
import json
#from flask import Flask

#app = Flask(__name__)
scheduler = BackgroundScheduler()
out_of_date_job = []
need_cancel_order_pairs = set()
def task_clean_invalid_job_and_order():
	global scheduler
	global out_of_date_job
	global need_cancel_order_pairs
	# remove job
	time.sleep(3)
	if len(out_of_date_job):
		print('remove outdate job starts...')
		out_of_date_job_copy = out_of_date_job.copy()
		for invalid_job in out_of_date_job_copy:
			scheduler.remove_job(invalid_job)
			out_of_date_job.remove(invalid_job)
	else:
		print('No outdate jobs!')
	# cancel order
	if len(need_cancel_order_pairs):
		print('cancel order starts...')
		need_cancel_order_pairs_copy = need_cancel_order_pairs.copy()
		for pair in need_cancel_order_pairs_copy:
			try:
				fun.cancel_orders_by_pair(pair)
				need_cancel_order_pairs.remove(pair)
			except BaseException as e:
				print('cancel ' + pair + ' order excepted.', e)			
			else:
				pass
	else:
		print('No order needs to be cancelled')			
socket.setdefaulttimeout(3)
if __name__ == '__main__':
	scheduler.start()
	asset_pairs_map = {}
	out_of_date_job_temp = []
	need_cancel_order_pairs_temp = set()
	scheduler.add_job(task_clean_invalid_job_and_order, 'interval', seconds = 60, max_instances = 50, id = 'cleaner' )
	with open("config/conf.json", 'r') as load_f:
		asset_pairs_map = json.load(load_f)
	count = 0
	for k, v in asset_pairs_map.items():
		scheduler.add_job(task.task_keep_position, 'interval', args = v["args"], max_instances = v["max_instances"], seconds = v["seconds"], id = k)
		time.sleep(0.5)
		# add to out_of_date_job list and need_cancel_order_pairs
		out_of_date_job_temp.append(k)
		need_cancel_order_pairs_temp.add(v["args"][0])
		count += 1
		if count % 6 == 0:
			# sleep 15m
			time.sleep(15 * 60)
			out_of_date_job = out_of_date_job_temp.copy()
			need_cancel_order_pairs = need_cancel_order_pairs_temp.copy()
			out_of_date_job_temp.clear()
			need_cancel_order_pairs_temp.clear()
	if len(asset_pairs_map) % 6:
		time.sleep(15 * 60)
		out_of_date_job = out_of_date_job_temp.copy()
		need_cancel_order_pairs = need_cancel_order_pairs_temp.copy()	
		out_of_date_job_temp.clear()
		need_cancel_order_pairs_temp.clear()
	scheduler.remove_job('cleaner')	
	time.sleep(70)


	#app.run(host='0.0.0.0', port=8080, debug=True)

