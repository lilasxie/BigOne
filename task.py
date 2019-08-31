import time, sched
import random
import globalval
from urllib import request, parse
import fun
import public

#------------------------ASK Task----------------------
def keep_ask_position(ask_price_and_id, asset_pair_name, side, amount, min_position, max_position):	
	order_book = public.get_order_book(asset_pair_name)
	asks = order_book['asks']
	ask_order = {"asset_pair_name": asset_pair_name, "side": side, "price": "", "amount": str(amount)}
	if not asks[min_position]['price'] < ask_price_and_id[0] < asks[max_position]['price']:
		fun.cancel_order(ask_price_and_id[1])
		ask_order['price'] = asks[int((max_position+min_position)/2)]['price']
		ask_order = fun.create_orders(ask_order)
		print('The position of {} ask order is not {}-{}, a new ask order created : price: {}, amount:{}'.format(asset_pair_name, min_position, max_position, ask_order['price'], ask_order['amount']))
		return ask_order
	else:
		print('Current ' + asset_pair_name + ' ask order remains')
		return True


def keep_ask_position_task(asset_pair_name, side, amount, min_position, max_position):
	ask_pair = {'asset_pair_name': asset_pair_name, 'side': side}
	current_ask = fun.get_orders(ask_pair)
	ask_order = {"asset_pair_name": asset_pair_name, "side": side, "price": "", "amount": str(amount)}
	ask_price_and_id = []
	if len(current_ask) == 0:
		print('No ' + asset_pair_name + ' current ask order found and gonna create one')
		order_book = public.get_order_book(asset_pair_name)
		asks = order_book['asks']
		ask_order['price'] = asks[int((max_position+min_position)/2)]['price']
		ask_order = fun.create_orders(ask_order)
		print('A new ' + asset_pair_name + ' ask order created')
		ask_price_and_id = (ask_order['price'], ask_order['id'])		
	elif len(current_ask) == 1:
		ask_price_and_id = (current_ask[0]['price'], current_ask[0]['id'])
		print('One {} ask order found. price {}, id {}'.format(asset_pair_name, current_ask[0]['price'], current_ask[0]['id']))
	else:
		for i in current_ask[:-1]:
			fun.cancel_order(i['id'])
			print('Ask ' + asset_pair_name + ' order', i['id'], 'cancelled')
		ask_price_and_id = (current_ask[-1]['price'], current_ask[-1]['id'])
	return keep_ask_position(ask_price_and_id, asset_pair_name, side, amount, min_position, max_position)


#-----------------------------BID TASK----------------------------

def keep_bid_position(bid_price_and_id, asset_pair_name, side, amount, min_position, max_position):	
	order_book = public.get_order_book(asset_pair_name)
	bids = order_book['bids']
	bid_order = {"asset_pair_name": asset_pair_name, "side": side, "price":"", "amount": str(amount)}
	if not bids[max_position]['price'] < bid_price_and_id[0] < bids[min_position]['price']:
		bid_order['price'] = bids[int((max_position+min_position)/2)]['price']
		fun.cancel_order(bid_price_and_id[1])
		bid_order = fun.create_orders(bid_order)
		print('The position of {} bid order is not {}-{}, a new bid order created : price: {}, amount:{}'.format(asset_pair_name, min_position, max_position, bid_order['price'], bid_order['amount']) )
		return bid_order
	else:
		print('Current ' + asset_pair_name + ' bid order remains')
		return True

def keep_bid_position_task(asset_pair_name, side, amount, min_position, max_position):
	bid_pair = {"asset_pair_name": asset_pair_name, "side": side}
	current_bid = fun.get_orders(bid_pair)
	bid_order = {"asset_pair_name": asset_pair_name, "side": side, "price": "", "amount": str(amount)}
	bid_price_and_id = []
	if len(current_bid) == 0:
		print('No ' + asset_pair_name + ' bid order found and gonna create one')
		order_book = public.get_order_book(asset_pair_name)
		bids = order_book['bids']
		bid_order['price'] = bids[int((max_position+min_position)/2)]['price']
		bid_order = fun.create_orders(bid_order)
		print('A new ' + asset_pair_name + ' bid order created')
		bid_price_and_id = (bid_order['price'], bid_order['id'])
	elif len(current_bid) == 1:
		bid_price_and_id = (current_bid[0]['price'], current_bid[0]['id'])
		print('One {} bid order found. price {}, id {}'.format(asset_pair_name, current_bid[0]['price'], current_bid[0]['id']))
	else:
		for i in current_bid[:-1]:
			fun.cancel_order(i['id'])
			print('Bid ' + asset_pair_name + ' order', i['id'], 'cancelled')
		bid_price_and_id = (current_bid[-1]['price'], current_bid[-1]['id'])
	keep_bid_position(bid_price_and_id, asset_pair_name, side, amount, min_position, max_position)

def task_keep_position(asset_pair_name, side, amount, min_position, max_position):
	print('{} job {} exec at: {}'.format(side, asset_pair_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	try:
		if side == globalval.GL_ORDER_ASK_TYPE:
			keep_ask_position_task(asset_pair_name, side, amount, min_position, max_position)
		else:
			keep_bid_position_task(asset_pair_name, side, amount, min_position, max_position)
	except BaseException as e:
		print('job ' + asset_pair_name + ' ' + side + ' excepted.', e)
	else:
		pass
	return True























