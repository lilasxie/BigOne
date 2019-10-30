#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib import request, parse
import tools
import globalval
import json

#--------------------------GET ACCOUNT INFO----------------------------

def get_accounts(symbol, auth_filename = 'auth'):
	headers = tools.get_headers(auth_filename = auth_filename)
	url = globalval.GL_API_URL_PREFIX + 'viewer/accounts/' + symbol
	req_account = request.Request(url, headers = headers, origin_req_host = 'b1.run', method = 'GET')
	resp_account = request.urlopen(req_account).read().decode()
	account = json.loads(resp_account)
	if account['code'] == 0:
		return account['data']
	else:
		return False

#--------------------------GET ORDER INFO----------------------------

def get_orders(asset_pair_name, side = None):
	'''
	returns a list, every element is a dict
	'''
	if side:
		pair2dict = {'asset_pair_name' : asset_pair_name, 'side' : side}
	else:
		pair2dict = {'asset_pair_name' : asset_pair_name}
	headers = tools.get_headers()
	parameters = parse.urlencode(pair2dict)
	url = globalval.GL_API_URL_PREFIX + 'viewer/orders' + '?' + parameters
	req_orders = request.Request(url, headers = headers, origin_req_host = 'b1.run', method = 'GET')
	resp_orders = request.urlopen(req_orders).read().decode()
	orders = json.loads(resp_orders)
	if orders['code'] == 0:
		return orders['data'] 
	else:
		return False

def get_trades(asset_pair_name = None):
	'''
	'''
	headers = tools.get_headers()
	parameters = parse.urlencode({"asset_pair_name" : asset_pair_name})
	url = globalval.GL_API_URL_PREFIX + 'viewer/trades' + '?' + parameters
	req_trades = request.Request(url, headers = headers, origin_req_host = 'b1.run', method = 'GET')
	resp_trades = request.urlopen(req_trades).read().decode()
	trades = json.loads(resp_trades)

	if trades['code'] == 0:
		return trades['data'] 
	else:
		return False


#--------------------------CREATE ONE ORDER ----------------------------
def create_one_order(order):
	headers = tools.get_headers(custom_headers = {'Content-Type': 'application/json'})
	url = globalval.GL_API_URL_PREFIX + 'viewer/orders'
	data = json.dumps(order).encode(encoding = 'utf-8')
	req_order = request.Request(url, data = data, headers = headers, origin_req_host = 'b1.run', method = 'POST')
	resp_order = request.urlopen(req_order).read().decode()
	order = json.loads(resp_order)
	if order['code'] == 0:
		return order['data'] 
	else:
		return False

#--------------------------CREATR MULTI ORDERS 1-10----------------------------
def create_orders(orders):
	headers = tools.get_headers(custom_headers = {'Content-Type': 'application/json'})
	if isinstance(orders, dict):
		url = globalval.GL_API_URL_PREFIX + 'viewer/orders'
	elif isinstance(orders, list):
		url = globalval.GL_API_URL_PREFIX + 'viewer/orders/multi'
	else:
		print('create orders fail!, orders must be a dict or list')
	data = json.dumps(orders).encode(encoding = 'utf-8')
	req_orders = request.Request(url, data = data, headers = headers, origin_req_host = 'b1.run', method = 'POST')
	resp_orders = request.urlopen(req_orders).read().decode()
	orders = json.loads(resp_orders)
	if orders['code'] == 0:
		return orders['data'] 
	else:
		return False

#--------------------------CANCEL ORDER BY ID----------------------------
def cancel_order(order_id):
	headers = tools.get_headers()
	url = globalval.GL_API_URL_PREFIX + 'viewer/orders/' + str(order_id) + '/cancel'
	req_cancel_order = request.Request(url, headers = headers, origin_req_host = 'b1.run', method = 'POST')
	resp_cancel_order = request.urlopen(req_cancel_order).read().decode()
	result = json.loads(resp_cancel_order)
	if result['code'] == 0:
		return result['data']
	else:
		return False

#--------------------------CANCEL ORDERS BY PAIRS----------------------------
def cancel_orders_by_pair(pair):
	pair2dict = {'asset_pair_name':pair}
	headers = tools.get_headers()
	url = globalval.GL_API_URL_PREFIX + 'viewer/orders/cancel'
	data = parse.urlencode(pair2dict).encode()
	req_cancel_orders_by_pair = request.Request(url, data = data, headers = headers, origin_req_host = 'b1.run', method = 'POST')
	resp_cancel_order_by_pair = request.urlopen(req_cancel_orders_by_pair).read().decode()
	result = json.loads(resp_cancel_order_by_pair)
	print(pair + ' canceled : ', result)
	return result['data']
