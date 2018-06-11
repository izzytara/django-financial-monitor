from websocket import create_connection
import simplejson as json

API_KEY = '993e1b0a543e60b88848094cb90521871a02711e'


class BitCoinApi:

    def subscribe(self, ticker):
        subscribe = {
            'eventName': 'subscribe',
            'authorization': API_KEY,
            'eventData': {
                'tickers': [ticker]
            }
        }
        return subscribe

    def unsubscribe(self, ticker):
        subscribe = {
            'eventName': 'unsubscribe',
            'authorization': API_KEY,
            'eventData': {
                'subscriptionId': 75,
                'tickers': [ticker]
            }
        }
        return subscribe

    def websocket(self, subscribe):
        ws = create_connection("wss://api.tiingo.com/crypto")
        ws.send(json.dumps(subscribe))
        return ws

    def wrapper(self):
        b = BitCoinApi()
        s = b.subscribe('btcusd')
        ws = b.websocket(s)
        return ws

"""
b = BitCoinApi()
ws = b.wrapper()
while True:
    r= json.loads(ws.recv())
    if r['messageType'] =='A':
        data = r['data']
        print(data)
"""










