import pandas as pd 
import numpy as np
import tools
import json
#df = pd.DataFrame(np.random.randn(6, 4), index = list('123456'), columns = list('ABCD'))
#df.to_csv('test_csv', mode = 'a+')




#timestamp = time.mktime(utc_time)


#print(type(timestamp))
#print(timestamp)
#help(datep)
#with open('config/contribute_value.csv', 'r') as f:
	#data = f.readlines()
'''
pair_list = []
pair_dict = {}
for s in data:
	pair = s.strip().split(',')
	pair_list.append(pair)
pair_dict = dict(pair_list)
print(pair_dict)
with open('config/contribute_value.json', 'w') as file:
	json.dump(pair_dict, file)
'''
import public
asset_pair_name = 'ONE-USDT'
book = public.get_order_book(asset_pair_name, limit = 20)
print(book)