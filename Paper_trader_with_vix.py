import alpaca_trade_api as ap
import threading
from time import sleep
import json
import logging

from alpaca_trade_api.rest import APIError

api_key = 'PKK2CKO4NF9TC01H8X6S'
api_secret = 'CHZ4f7visuyRvkuOHdeHO9PTWStpWPsCu//uxTWx'
base_url = 'https://paper-api.alpaca.markets'
l = []
api = ap.REST(api_key, api_secret, base_url, api_version='v2')
assets = api.list_assets(status="active")
for i in range(len(assets)):
    try:
        l.append(assets[i].symbol)
    except APIError:
        print("poop")
account = api.get_account()
print(l)
