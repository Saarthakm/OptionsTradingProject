import alpaca_trade_api as ap
import threading
from time import sleep
import json
import logging

from alpaca_trade_api.rest import APIError

api_key = 'PK3Y5N2FQHN84K1BWSJ7'
luis_api_key = 'AKM8I6JTLDYHNMQT9RLN'
luis_secret_key = 'Ala8vPXcuMxQieOhay8OUmpCP01AWTndVhpAbPPA'
api_secret = '/LhQfCCcu1n5E6eNLVXHVOA3FQhIuaj8JfmjtMYB'
base_trade = 'https://paper-api.alpaca.markets'  # for trading
base_data = 'https://data.alpaca.markets/v1'  # for data
trades = []
partial_trades = []
requested_trades = []
api = ap.REST(api_key, api_secret, base_trade, api_version='v2')

account = api.get_account()
print(account)
active_assets = api.list_assets(status='active')
print(active_assets[0])
for i in range(3):
    # api.submit_order(symbol=active_assets[i].symbol, qty=2, side='sell', type='market',
    #                  time_in_force='day')
    api.submit_order(symbol="GOOG", qty=10, side='buy', type='market',
                     time_in_force='day')
print(api.list_orders())
# for i in range(200):
#     try:
#         print(api.get_last_quote(active_assets[i].symbol))
#     except APIError:
#         print(active_assets[i])

trade_conn = ap.stream2.StreamConn(api_key, api_secret, base_trade)
data_conn = ap.stream2.StreamConn(api_key, api_secret,
                                  base_trade)  # will use this when we have live acc, not for paper trading


# monitor cash balance
@trade_conn.on(r'^account_updates$')
async def on_account_updates(conn, channel, account):
    balance = account['cash']  # maybe make this cash_withdrawable?


# writes all trades to respective csvs, logs filled, partially filled, etc
@trade_conn.on(r'^trade_updates$')
async def on_trade_updates(conn, channel, trade):
    trades.append(trade)  # maybe remove
    if 'partial_fill' in trade.event:
        trades.append([trade.order['updated_at'], trade.order['symbol'], trade.order['side'],
                       trade['price'], trade.order['filled_qty'], trade.order['filled_avg_price']])

        with open('partial_trades.csv', 'w') as f:
            json.dump(partial_trades, f, indent=4)
    if 'fill' in trade.event:
        partial_trades.append([trade.order['updated_at'], trade.order['symbol'], trade.order['side'],
                               trade.order['filled_qty'], trade.order['filled_avg_price']])
        with open('past_trades.csv', 'w') as f:
            json.dump(trades, f, indent=4)
    # if 'done_for_the_day' in trade.event:
    # maybe set something true here
    if 'new' in trade.event:
        requested_trades.append([trade.order['updated_at'], trade.order['symbol'], trade.order['side'],
                                 trade['price']])
        with open('new_trades.csv', 'w') as f:
            json.dump(requested_trades, f, indent=4)


# starts
def ws_start():
    trade_conn.run(['account_updates', 'trade_updates'])


# pass in asset with buy or sell direction
# TO-DO add quantity once we determine how we will do quantity
def submit_order(asset, direction):
    api.submit_order(symbol=asset['symbol'], qty=1, side=direction, type='market',
                     time_in_force='day')  # change market buy later on
    # add stuff for stop limits, limits, etc once non market order


# only trades active hours, no after hours currently
def check_open():
    clock = api.get_clock()
    close = clock.next_close
    return clock.next_close > clock.timestamp


# within limits we define, I.E. probably stop trading within 20 mins of close
def actively_trading():
    clock = api.get_clock()
    #
    #
    #
    pass


# parse holdings from  holdings csv
def parse_holdings():
    # read in holdings from csv
    return list


# update holdings from trade csv to ensure only assets that are actually filled are bought
# make sure to acc for quantity
def update_holdings():
    # read in past_trades

    # maybe use trades[] instead of csv
    return list


def get_buys():
    # gets stocks to buy from algo
    # TO DO if quantity added, make dict with ticker key, val pair
    return list


def get_sell():
    # gets sells from holdings
    return list


# something something stop loss
def stop_loss():
    pass


# starts trader and cancels all current orders to avoid any monkey business
def start_trader():
    api.cancel_all_orders()
    holdings = parse_holdings()
    balance = api.get_account()['cash']
    ws_thread = threading.Thread(target=ws_start, daemon=True)  # low prio thread? maybe no daemon
    ws_thread.start()
    sleep(10)  # buffer for initialize

    # trading next
    while check_open() == True:
        assets = parse_holdings()  # check current holdings
        buys = get_buys()  # get stocks to buy
        sells = get_sell()  # get sells
        # maybe add some sleeps
        while actively_trading() is True and balance >= 1.00:
            for i in range(len(buys)):  # change to for each when dict implement for qty
                submit_order(buys[i], 'buy')
            for g in range(len(sells)):
                submit_order(sells[g], 'sell')
            update_holdings()
            assets = parse_holdings()
            # update buys
            # update sells
            balance = api.get_account()['cash']
            # if we dont update data as frequent as possible then it will just do same buying an selling XD
