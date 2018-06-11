from websocket import create_connection
import simplejson as json

ws = create_connection("wss://api.tiingo.com/crypto")

subscribe = {
 'eventName':'subscribe',
 'authorization':'993e1b0a543e60b88848094cb90521871a02711e',
 'eventData': {
               'tickers': ['btcusd']
               }
 }

ws.send(json.dumps(subscribe))



while(True):
    json_data = json.loads(ws.recv())
    if json_data['messageType']=='A':
        fx_data=json_data['data']
        print(fx_data)
        price = fx_data[-1]

        #print(fx_data[1], fx_data[-1])






