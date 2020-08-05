import alpaca_trade_api as tradeapi
import threading
from time import sleep
import json
import logging

api_key = 'PK3Y5N2FQHN84K1BWSJ7'
api_secret = '/LhQfCCcu1n5E6eNLVXHVOA3FQhIuaj8JfmjtMYB'
base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

account = api.get_account()
print(account)
