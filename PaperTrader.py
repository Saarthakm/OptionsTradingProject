import alpaca_trade_api as ap
import threading
from time import sleep
import json
import logging

from alpaca_trade_api.rest import APIError

api_key = 'PK3Y5N2FQHN84K1BWSJ7'
api_secret = '/LhQfCCcu1n5E6eNLVXHVOA3FQhIuaj8JfmjtMYB'
base_trade = 'https://paper-api.alpaca.markets'
base_data = 'https://data.alpaca.markets/v1'

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
