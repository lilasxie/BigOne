import fun, tools
import pandas as pd
import numpy as np
from datetime import datetime
import time


def account_snapshot(symbols):
	today = str(datetime.now())
	for symbol in symbols:		
		account = fun.get_accounts(symbol, auth_filename = 'auth-query')
		if account:
			df = pd.DataFrame(account, index = [today])
			df.to_csv('data_saved/balance_snapshot_' + symbol + '.csv', mode = 'a+', header = False)
			

def account_change(symbols):
	account_change = {}
	for symbol in symbols:
		df = pd.read_csv('data_saved/balance_snapshot_' + symbol + '.csv')
		df_latest = df.tail(2)
		delta = df_latest.iat[1,2] - df_latest.iat[0,2]
		account_change[symbol] = delta
	return account_change

#def out_of_balance_notify(symbols):





symbols = ['BTC', 'ONE', 'USDT', 'EOS']
account_snapshot(symbols)

#change = account_change(symbols)
#print(change)

#a = account_info(symbols)
#print(a)
#today = str(datetime.now().date())
#print(today, type(today))
#account = fun.get_accounts('BTC', auth_filename = 'auth-query')
#print(account)
#, columns = ['date', 'asset_symbol', 'balance', 'locked_balance']