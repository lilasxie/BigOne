#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request, parse
import json
import tools
import globalval



#--------------------GET TOP 20 ORDER BOOK--------------------


def get_order_book(asset_pair_name, limit = 20):
	headers = tools.get_headers(auth = False)
	parameters = parse.urlencode({'limit': limit})
	url = globalval.GL_API_URL_PREFIX + 'asset_pairs/' + asset_pair_name +'/depth'+'?'+ parameters
	req_book = request.Request(url, headers = headers, origin_req_host = 'b1.run', method = 'GET')
	resp_book = request.urlopen(req_book).read().decode()
	book = json.loads(resp_book)
	return book['data']

# -------------------GET TICKER-------------------

#def get_current_price(get_ticker):
	#def 
def get_ticker(asset_pair_name):
	'''
	one positional argument: should be string like 'BTC-USDT'
	'''
	headers = tools.get_headers(auth = False)
	url = globalval.GL_API_URL_PREFIX + 'asset_pairs/' + asset_pair_name +'/ticker'
	req_ticker = request.Request(url, headers = headers, origin_req_host = 'b1.run', method = 'GET')
	resp_ticker = request.urlopen(req_ticker).read().decode()
	ticker = json.loads(resp_ticker)
	result = ticker['data']
	return result


