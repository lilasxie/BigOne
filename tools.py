import jwt
import time
import json

# 获取bigone api接口的jwt
def get_jwt(key, secret_key):
	current_time = str(time.time_ns())
	data = {"type" : "OpenAPIV2", "sub" : key, "nonce": current_time}
	secret = secret_key
	data_signed = jwt.encode(data, secret, algorithm = "HS256").decode()
	bearer_token = 'Bearer ' + data_signed
	return bearer_token

# 获取UA
def get_ua():
	return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
#获取access_key配置
key_conf = {}
with open("config/auth.json", 'r') as load_f:
	key_conf = json.load(load_f)
# 获取headers
def get_headers(custom_headers = {}):
	global key_conf
	headers = {"Authorization": get_jwt(key_conf["key"], key_conf["secret_key"]), 'User-Agent': get_ua()}
	if custom_headers:
		headers.update(custom_headers)
	return headers
