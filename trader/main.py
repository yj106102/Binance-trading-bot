import time
import pandas as pd
import pickle
import common
from tradinghelper.models import Record
from enum import Enum
from threading import Event
import threading
class Trade(Enum):
    BUY = 1
    SELL = 2
    NONE = 3
event = Event()
binance = common.get_binance()
TRADING_BALANCE_RATIO = 0.2
position_info = {'amount':{}, 'prev_price':{}} # amount는 현재 포지션이 롱이면 +, 숏이면 -, 없으면 0, prev_price는 트레이딩 시작 시 가격

def check_trade_condition(type,symbol,params):
    # 트레이딩 시작 조건 만족 확인
    if type == 'RSI':
        threshold = params['open_rsi_threshold']
        if get_rsi(symbol) < threshold:
            return Trade.BUY
        elif get_rsi(symbol) > 100-threshold:
            return Trade.SELL
        else:
            return Trade.NONE
    else:
        return Trade.NONE
def check_close_condition(type,symbol, params):
    # 트레이딩 종료 조건 만족 확인
    global position_info
    amount = position_info['amount']
    if type == 'RSI':
        threshold = params['close_rsi_threshold']
        if symbol in amount:
            if amount[symbol] > 0:
                if get_rsi(symbol) > threshold:
                    return True
                else:
                    return False
            elif amount[symbol] < 0:
                if get_rsi(symbol) < 100 - threshold:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
    else:
        return False

def rsi_calc(ohlc: pd.DataFrame, period: int = 14):
    #rsi 계산
    ohlc = ohlc[4].astype(float)
    delta = ohlc.diff()
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0

    _gain = gains.ewm(com=(period-1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period-1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100-(100/(1+RS)), name="RSI")

def get_rsi( symbol,itv='3m'):
    ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe=itv, limit=200)
    df = pd.DataFrame(ohlcv)
    rsi = rsi_calc(df,14).iloc[-1]
    return rsi
def get_price(symbol):
    # 현재 가격 계산
    last_price = binance.fetch_ticker (symbol)['last']

    return last_price

def get_trade_amount():
    # 얼마나 트레이딩 할지 계산
    fetched_balance = binance.fetch_balance(params={'type':'future'})
    balance = float(fetched_balance['USDT']['total'])
    return (balance * TRADING_BALANCE_RATIO)
def commit_trade(symbol, whether_to_trade):
    # 트레이딩 실행
    global position_info
    price = get_price(symbol)
    position_info['prev_price'][symbol] = price
    amount = get_trade_amount() / get_price(symbol)
    
    if whether_to_trade == Trade.BUY:
         print(f"Buying {symbol} for {amount} USDT")
         position_info['amount'][symbol] = amount
         binance.create_market_order(symbol, 'buy', amount)
    elif whether_to_trade == Trade.SELL:
         print(f"Selling {symbol} for {amount} USDT")
         position_info['amount'][symbol] = -amount
         binance.create_market_order(symbol, 'sell', amount)

def commit_close(type,symbol):
    #트레이딩 종료
    global position_info
    amount = position_info['amount']
    if amount[symbol] < 0:
        print(f"Closing {symbol} short position")
        amount[symbol] = 0
        binance.create_market_order(symbol, 'buy', abs(amount), params={"reduceOnly": True})
        
    elif amount[symbol] > 0:
        print(f"Closing {symbol} long position")
        amount[symbol] = 0
        binance.create_market_order(symbol, 'sell', abs(amount), params={"reduceOnly": True})
def get_event():
    return event

def record_result(type, symbol, params):
    # 결과를 데이터베이스에 저장
    global position_info
    print(position_info['prev_price'][symbol],get_price(symbol))
    benefit = position_info['amount'][symbol] * (position_info['prev_price'][symbol]-get_price(symbol))
    print('benefit: {}'.format(benefit))
    if type == 'RSI':
        Record.objects.create(strategy_type=type,symbol=symbol,benefit=benefit
                                 ,params=params)

def start_trade(symbols, params):
    global position_info
    new_params = params['params']
    type = params['type']
    amount = position_info['amount']
    if type != 'RSI':
        print('잘못된 거래 타입입니다.')
    
    
    for symbol in symbols:
        amount[symbol] = 0

    

    balance = binance.fetch_balance(params={'type':'future'})
    time.sleep(0.1)
    total_money = float(balance['USDT']['total'])
    while(True):
        print('Trading bot is running...')
        if event.is_set():
            # 종료 신호
            for symbol in symbols:
                commit_close(type,symbol)
            print('--------Trading bot stopped--------')
            event.clear()
            return
        for symbol in symbols:
            if amount[symbol] != 0:
                whether_to_close = check_close_condition(type,symbol,new_params)
                print(whether_to_close)
                if whether_to_close:
                    record_result(type,symbol,new_params)
                    commit_close(type,symbol)

            else:
                whether_to_trade = check_trade_condition(type,symbol,new_params)
                
                commit_trade(symbol,whether_to_trade)

        time.sleep(0.05)
    
