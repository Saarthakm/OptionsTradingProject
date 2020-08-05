import alpaca_trade_api as ap
import threading
from time import sleep
import json
import logging
import alpaca_backtrader_api as ap_bt
from alpaca_trade_api.rest import APIError

api_key = 'PK3Y5N2FQHN84K1BWSJ7'
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
for i in range(200):
    try:
        print(api.get_last_quote(active_assets[i].symbol))
    except APIError:
        print(active_assets[i])

trade_conn = ap.stream2.StreamConn(api_key, api_secret, base_trade)
data_conn = ap.stream2.StreamConn(api_key, api_secret,
                                  base_trade)  # will use this when we have live acc, not for paper trading


@trade_conn.on(r'^account_updates$')
async def on_account_updates(conn, channel, account):
    balance = account['cash']  # maybe make this cash_withdrawable?


@trade_conn.on(r'^trade_updates$')
async def on_trade_updates(conn, channel, trade):
    trades.append(trade)  # maybe remove
    if 'partial_fill' in trade.event:
        trades.append([trade.order['updated_at'], trade.order['symbol'], trade.order['side'],
                       trade['price'], trade.order['filled_qty'], trade.order['filled_avg_price']])
        with open('past_trades.csv', 'w') as f:
            json.dump(trades, f, indent=4)
    if 'fill' in trade.event:
        partial_trades.append([trade.order['updated_at'], trade.order['symbol'], trade.order['side'],
                               trade.order['filled_qty'], trade.order['filled_avg_price']])
        with open('partial_trades.csv', 'w') as f:
            json.dump(partial_trades, f, indent=4)
    # if 'done_for_the_day' in trade.event:
    # maybe set something true here
    if 'new' in trade.event:
        requested_trades.append([trade.order['updated_at'], trade.order['symbol'], trade.order['side'],
                                 trade['price']])
        with open('new_trades.csv', 'w') as f:
            json.dump(requested_trades, f, indent=4)


def ws_start():
    trade_conn.run(['account_updates', 'trade_updates'])


# pass in asset with buy or sell direction
def submit_order(asset, direction):
    api.submit_order(symbol=asset['symbol'], qty=1, side=direction, type='market',
                     time_in_force='day')  # change market buy later on
    # add stuff for stop limits, limits, etc once non market order


def check_open():
    clock = api.get_clock()
    close = clock.next_close
    return clock.next_close > clock.timestamp


def actively_trading():
    clock = api.get_clock()
    #
    #
    #
    pass


# makes asset list for pruned stocks list
def parse_stocks():
    # stock_list = whatever we pass in from algo
    # asset = api.get_asset(stock_list[i])
    # asset_list[i] = asset
    # return asset_list
    pass


# starts trader and cancels all current orders to avoid any monkey business
def start_trader():
    api.cancel_all_orders()
    balance = api.get_account()['cash']
    ws_thread = threading.Thread(target=ws_start, daemon=True)  # low prio thread? maybe no daemon
    ws_thread.start()
    sleep(10)  # buffer for initialize

    # trading next
    while (check_open() == True):
        assets = parse_stocks()
        # maybe add some sleeps
        while (actively_trading() == True):
            for i in range(len(assets)):
                submit_order(assets[i])
                assets.remove(assets[i])  # this will be inefficient
