import globalval
import json

asset_pairs_BTC = ['BCHABC-BTC', 'ETH-BTC', 'EOS-BTC', 'LTC-BTC', 'XRP-BTC', 'ATOM-BTC', 'BCHSV-BTC','DASH-BTC', 'ETC-BTC', 'NEO-BTC', 'ONE-BTC', 'QTUM-BTC', 'TRX-BTC', 'XLM-BTC', 'XMR-BTC', 'XTZ-BTC', 'ZEC-BTC']
asset_pairs_USDT = ['BTC-USDT', 'ONE-USDT','BCHABC-USDT', 'ETH-USDT', 'EOS-USDT', 'LTC-USDT', 'XRP-USDT', 'ATOM-USDT', 'BCHSV-USDT','DASH-USDT',  'NEO-USDT', 'QTUM-USDT', 'TRX-USDT', 'XLM-USDT', 'XMR-USDT', 'XTZ-USDT', 'ZEC-USDT']
asset_pair_ELSE = ['EOS-ETH', 'ONE-ETH', 'ONE-EOS']
asset_pairs = []
asset_pairs.extend(asset_pairs_USDT)
asset_pairs.extend(asset_pairs_BTC)
asset_pairs.extend(asset_pair_ELSE)

min_position = 9
max_position = 13
max_instances = 50
cron_interval = 3
asset_pairs_map = {}
for pair in asset_pairs:

	ask_job_prefix = "ask_job_"
	ask_job_key = ask_job_prefix + pair.lower().replace("-", "_")
	asset_pairs_map[ask_job_key] = {"args": [pair, globalval.GL_ORDER_ASK_TYPE, 1, min_position, max_position], "max_instances": max_instances, "seconds": cron_interval}

	bid_job_prefix = "bid_job_"
	bid_job_key = bid_job_prefix + pair.lower().replace("-", "_")
	asset_pairs_map[bid_job_key] = {"args": [pair, globalval.GL_ORDER_BID_TYPE, 1, min_position, max_position], "max_instances": max_instances, "seconds": cron_interval}
'''
with open("config/conf.json", "w") as dump_f:
    json.dump(asset_pairs_map, dump_f)
'''
load_dict = {}
with open("config/conf.json", 'r') as load_f:
	load_dict = json.load(load_f)
for k in load_dict:
	print(k)