from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
import json
import os
import ccxt


settings_path = "settings.json"
def get_binance():
    keys = get_binance_keys()
    return ccxt.binance(config = {
        'apiKey': keys['API_KEY'],
        'secret': keys['API_SECRET'],
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        }
    })

def get_binance_keys():
    keys = get_project_settings(settings_path)['BINANCE_KEYS']
    return keys
def get_project_settings(importFilepath):
    # Test the filepath to sure it exists
    if os.path.exists(importFilepath):
        # Open the file
        f = open(importFilepath, "r")
        # Get the information from file
        project_settings = json.load(f)
        # Close the file
        f.close()
        # Return project settings to program
        return project_settings
    else:
        return ImportError

# def get_symbols(): 
#     # config_logging(logging, logging.DEBUG)
#     um_futures_client = get_futures()
#     symbols = []
#     for symbol in um_futures_client.exchange_info()['symbols']:
#         symbols.append(symbol['symbol'])
#     return symbols
    
 

    # print(um_futures_client.account())
    