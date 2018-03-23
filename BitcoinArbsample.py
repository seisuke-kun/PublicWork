import ccxt
import time
#print(ccxt.exchanges) #取れる取引所を取得

exchange_list = ['bitflyer', 'coincheck', 'quoinex', 'zaif']#比較したい取引所のリスト


#表示するだけ
while True:
    ask_exchange = ''
    ask_price = 99999999
    bid_exchange = ''
    bid_price = 0

    for exchange_id in exchange_list:
        exchange = eval('ccxt.' + exchange_id + '()')
        orderbook = exchange.fetch_order_book ('BTC/JPY')
        bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
        ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
        if ask < ask_price:
            ask_exchange = exchange_id
            ask_price = ask
        if bid > bid_price:
            bid_exchange = exchange_id
            bid_price = bid

    if bid_price > ask_price:#裁定可能なら
        print (ask_exchange, 'で', ask_price, '円で買って')
        print (bid_exchange, 'で', bid_price, '円で売れば')
        print (bid_price - ask_price, '円の利益！')

'''
#取引するなら
exchanges = {
    "bitflyer": {
        "apiKey": "",
        "secret": ""
    },
    "quoinex": {
        "apiKey": "",
        "secret": ""
    },
    "zaif": {
        "apiKey": "",
        "secret": ""
    }
}

while True:
    amount = 0.001
    ask_exchange = ''
    ask_price = 99999999
    bid_exchange = ''
    bid_price = 0

    # 各取引所のaskとbidを取得
    for exchange_id in exchanges:
        exchange = eval('ccxt.' + exchange_id + '()')
        orderbook = exchange.fetch_order_book('BTC/JPY')
        bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
        ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
        if ask < ask_price:
            ask_exchange = exchange_id
            ask_price = ask
        if bid > bid_price:
            bid_exchange = exchange_id
            bid_price = bid

    # 裁定取引を行う
    if bid_price > ask_price:#裁定可能なら
        #買い
        exchange = eval('ccxt.' + ask_exchange + '()')
        exchange.apiKey = exchanges[ask_exchange]["apiKey"]
        exchange.secret = exchanges[ask_exchange]["secret"]
        exchange.create_limit_buy_order ('BTC/JPY', 0.001, int(ask_price/10)*10)

        #売り
        exchange = eval('ccxt.' + bid_exchange + '()')
        exchange.apiKey = exchanges[bid_exchange]["apiKey"]
        exchange.secret = exchanges[bid_exchange]["secret"]
        exchange.create_limit_sell_order ('BTC/JPY', 0.001, int(bid_price*10)/10)

        print(ask_exchange, 'で', ask_price, '円で', amount, '買って')
        print(bid_exchange, 'で', bid_price, '円で', amount, '売ったので')
        print((bid_price - ask_price)*amount, '円の利益！')
        time.sleep(10)'''
