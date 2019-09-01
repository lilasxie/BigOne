#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib import request, parse
import tools
import globalval
import json

#--------------------------GET ACCOUNT INFO----------------------------
def get_accounts(symbol):
	headers = tools.get_headers()
	url = globalval.GL_API_URL_PREFIX + 'viewer/accounts/' + symbol
	req_accounts = request.Request(url, headers = headers, origin_req_host = 'b1.run', method = 'GET')
	resp_accounts = request.urlopen(req_accounts).read().decode()
	account = json.loads(resp_accounts)
	print(account)
	if account['code'] == 0:
		return account['data'] 
	else:
		return Flase
#--------------------------GET ORDER INFO----------------------------
def get_orders(pair):
	headers = tools.get_headers()
	parameters = parse.urlencode(pair)
	url = globalval.GL_API_URL_PREFIX + 'viewer/orders' + '?' + parameters
	req_orders = request.Request(url, headers = headers, origin_req_host = 'b1.run', method = 'GET')
	resp_orders = request.urlopen(req_orders).read().decode()
	orders = json.loads(resp_orders)
	if orders['code'] == 0:
		return orders['data'] 
	else:
		return False


#--------------------------CREATE ONE ORDER ----------------------------
def create_one_order(order):
	headers = tools.get_headers(custom_headers = {'Content-Type': 'application/json'})
	url = globalval.GL_API_URL_PREFIX + 'viewer/orders'
	data = json.dumps(order).encode(encoding = 'utf-8')
	print(data)
	req_order = request.Request(url, data = data, headers = headers, origin_req_host = 'b1.run', method = 'POST')
	resp_order = request.urlopen(req_order).read().decode()
	print(resp_order)
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
