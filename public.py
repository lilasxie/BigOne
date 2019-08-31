from urllib import request, parse
import json
import tools
import globalval



#--------------------获取前10挂单簿--------------------

def get_order_book(pair):
	headers = tools.get_headers()
	parameters = parse.urlencode({'limit': '20'})
	url = globalval.GL_API_URL_PREFIX + 'asset_pairs/' + pair +'/depth'+'?'+ parameters
	req_book = request.Request(url, headers = headers, origin_req_host = 'b1.run', method = 'GET')
	resp_book = request.urlopen(req_book).read().decode()
	book = json.loads(resp_book)
	return book['data']