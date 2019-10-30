import pandas as pd 
import public
import public
import json


#计算单一方向总得分
def cal_side_total_point(close_price, book, side = 'asks'):
	min_valid_price = 0.98 * close_price
	max_valid_price = 1.02 * close_price
	side_book = book[side]
	total_side_point = 0
	count = 0
	for order in side_book:		
		if float(order['price']) > max_valid_price or float(order['price']) < min_valid_price:
			print('the number of valid {} {} order is {}'.format(book['asset_pair_name'], side, count))
			break
		weight = (1 - 50 * abs(float(order['price'])/close_price-1))**4
		total_side_point +=  float(order['price']) * float(order['quantity']) * weight
		count += 1
	return total_side_point



bias = 0.006
weight = 0.24


with open('config/contribute_value.json', 'r') as f:
	asset_pair_dict = json.load(f)
	#print(asset_pair_dict)

all_pair_point_value = []
for k, v in asset_pair_dict.items():
	quote_currency = k.split('-')[1]
	close_price = float(public.get_ticker(k)['close'])
	book = public.get_order_book(k, limit = 60)
	point_and_value = {'asset_pair_name' : k, 'close_price' : close_price}
	for side in ['asks', 'bids']:
		total_side_point = cal_side_total_point(close_price, book, side = side)
		point_and_value[side + '_total_point'] = total_side_point
		amount_per_value = [total_side_point / (int(v) * weight), quote_currency]
		point_and_value[side + '_amount_per_value'] = amount_per_value
		
	all_pair_point_value.append(point_and_value)
print(all_pair_point_value)


# 提取最小成本交易对
ask_values_BTC = []
bid_values_BTC = []
ask_values_USDT = []
bid_values_USDT = []
ask_values_ETH = []
bid_values_ETH = []

for i in all_pair_point_value:
	if i['asks_amount_per_value'][1] == 'BTC':
		ask_values_BTC.append(i['asks_amount_per_value'][0])
		bid_values_BTC.append(i['bids_amount_per_value'][0])
	elif i['asks_amount_per_value'][1] == 'USDT':
		ask_values_USDT.append(i['asks_amount_per_value'][0])
		bid_values_USDT.append(i['bids_amount_per_value'][0])
	elif i['asks_amount_per_value'][1] == 'ETH':
		ask_values_ETH.append(i['asks_amount_per_value'][0])
		bid_values_ETH.append(i['bids_amount_per_value'][0])

min_ask_BTC = min(ask_values_BTC)
min_bid_BTC = min(bid_values_BTC)
min_ask_USDT = min(ask_values_USDT)
min_bid_USDT = min(bid_values_USDT)
min_ask_ETH = min(ask_values_ETH)
min_bid_ETH = min(bid_values_ETH)

print('min_ask_BTC : {}, min_bid_BTC: {}, min_ask_USDT: {}, min_bid_USDT: {}, min_ask_ETH: {}, min_bid_ETH: {}'.format(min_ask_BTC, min_bid_BTC, min_ask_USDT, min_bid_USDT, min_ask_ETH, min_bid_ETH))





#print(df)
#asset_pair_name = 'EOS-USDT'









