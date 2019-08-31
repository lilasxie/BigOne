from apscheduler.schedulers.background import BackgroundScheduler
import task, fun
import time
import socket
import json
#from flask import Flask

#app = Flask(__name__)
scheduler = BackgroundScheduler()

socket.setdefaulttimeout(3)
if __name__ == '__main__':
	asset_pairs_map = {}
	with open("config/conf.json", 'r') as load_f:
		asset_pairs_map = json.load(load_f)
	count = 0
	# 定时器启动标志
	mark = True
	out_of_date_job = []
	cancelled_order_by_pair = set()
	for k, v in asset_pairs_map.items():
		scheduler.add_job(task.task_keep_position, 'interval', args = v["args"], max_instances = v["max_instances"], seconds = v["seconds"], id = k)
		time.sleep(0.5)
		# 加入到待清理job列表和待取消订单对
		out_of_date_job.append(k)
		cancelled_order_by_pair.add(v["args"][0])
		# 计数器+1
		count += 1
		# 每4个任务主进程休眠15m
		if count % 4 == 0:
			if mark:
				# 保证只启动start一次
				scheduler.start()
				mark = False
			# sleep 15m
			time.sleep(12 * 60)
			# 清理过期job
			for invalid_job in out_of_date_job:
				scheduler.remove_job(invalid_job)
			# 重置过期job列表
			out_of_date_job.clear()
			time.sleep(4)
			# 取消订单
			for pair in cancelled_order_by_pair:
				fun.cancel_orders_by_pair(pair)
			# 重置待取消订单对
			cancelled_order_by_pair.clear()
	time.sleep(12 * 60)
	#app.run(host='0.0.0.0', port=8080, debug=True)

