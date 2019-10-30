
import fun
import time
import util
from datetime import datetime

trades = fun.get_trades(asset_pair_name = 'ONE-BTC')
print(trades)


ask_trades = []
bid_trades = []
asset_pair_name = 'ONE-BTC'
base_currency = asset_pair_name.partition('-')[0]
quote_currency = asset_pair_name.partition('-')[2]
total_base_amount_sold = 0
total_base_amount_bought = 0
total_base_fee = 0
total_quo_fee = 0

for trade in trades:
	if util.formattime2datetime(trade['created_at']).date() >= datetime.now().date()
		continue
	if trade['side'] == 'ASK':
		ask_trades.append(trade)
		total_base_amount_sold += float(trade['amount'])
		if trade['maker_fee']:
			total_quo_fee += float(trade['maker_fee'])
		else:
			total_quo_fee += float(trade['taker_fee'])
	else:
		bid_trades.append(trade)
		total_base_amount_bought += float(trade['amount'])
		if trade['maker_fee']:
			total_base_fee += float(trade['maker_fee'])
		else:
			total_base_fee += float(trade['taker_fee'])
print('total_base_amount_sold: ', total_base_amount_sold)
print('total_base_amount_bought: ', total_base_amount_bought)
print('total_base_fee :' , total_base_fee )
print('total_quo_fee: ', total_quo_fee )


