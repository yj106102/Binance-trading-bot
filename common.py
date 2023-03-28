import json
import os
import ccxt


settings_path = "settings.json"


def get_binance():
    keys = get_binance_keys()
    return ccxt.binance(
        config={
            "apiKey": keys["API_KEY"],
            "secret": keys["API_SECRET"],
            "enableRateLimit": True,
            "options": {
                "defaultType": "future",
            },
        }
    )


def get_binance_keys():
    keys = get_project_settings(settings_path)["BINANCE_KEYS"]
    return keys


def get_project_settings(file_path):
    if os.path.exists(file_path):
        file = open(file_path, "r")
        project_settings = json.load(file)
        file.close()
        return project_settings
    else:
        return ImportError