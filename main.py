from apscheduler.schedulers.background import BackgroundScheduler
import task, fun
import time
import socket
import json
#from flask import Flask

#app = Flask(__name__)
scheduler = BackgroundScheduler()

def task_clean_invalid_job_and_order(out_of_date_job = [], need_cancell_order_pairs = set()):
	global scheduler
	# 清理过期job
	for invalid_job in out_of_date_job:
		scheduler.remove_job(invalid_job)
	# 重置过期job列表
	out_of_date_job.clear()
	time.sleep(4)
	# 取消订单
	for pair in need_cancell_order_pairs:
		fun.cancel_orders_by_pair(pair)
	# 重置待取消订单对
	need_cancell_order_pairs.clear()

socket.setdefaulttimeout(3)
if __name__ == '__main__':
	scheduler.start()
	asset_pairs_map = {}
	with open("config/conf.json", 'r') as load_f:
		asset_pairs_map = json.load(load_f)
	count = 0
	out_of_date_job = []
	need_cancell_order_pairs = set()
	for k, v in asset_pairs_map.items():
		scheduler.add_job(task.task_keep_position, 'interval', args = v["args"], max_instances = v["max_instances"], seconds = v["seconds"], id = k)
		time.sleep(0.5)
		# 加入到待清理job列表和待取消订单对
		out_of_date_job.append(k)
		need_cancell_order_pairs.add(v["args"][0])
		# 计数器+1
		count += 1
		# 每4个任务主进程休眠15m
		if count % 4 == 0:
			# sleep 15m
			time.sleep(15 * 60)
			# 清理过期job和订单
			task_clean_invalid_job_and_order(out_of_date_job, need_cancell_order_pairs)
	if len(asset_pairs_map) % 4:
		time.sleep(15 * 60)
		# 清理过期job和订单
		task_clean_invalid_job_and_order(out_of_date_job, need_cancell_order_pairs)
	#app.run(host='0.0.0.0', port=8080, debug=True)

