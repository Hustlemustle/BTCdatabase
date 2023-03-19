import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode


class Binance():
    def __init__(self, api_key = None, api_secret = None, BASE_URL = None):
        self.BASE_URL = BASE_URL
        self.KEY = api_key
        self.SECRET = api_secret
        

    ''' ======  begin of functions, you don't need to touch ====== '''
    def hashing(self,query_string):
        return hmac.new(self.SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def get_timestamp(self):
        return int(time.time() * 1000)


    def dispatch_request(self,http_method):
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json;charset=utf-8',
            'X-MBX-APIKEY': self.KEY
        })
        return {
            'GET': session.get,
            'DELETE': session.delete,
            'PUT': session.put,
            'POST': session.post,
        }.get(http_method, 'GET')

    # used for sending request requires the signature
    def send_signed_request(self, http_method, url_path, payload={}):
        query_string = urlencode(payload, True)
        
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())

        url = self.BASE_URL + url_path + '?' + query_string + '&signature=' + self.hashing(query_string)
        # print("{} {}".format(http_method, url))
        params = {'url': url, 'params': {}}
        response = self.dispatch_request(http_method)(**params)
        return response.json()

    # used for sending public data request
    def send_public_request(self, url_path, payload={}):
        query_string = urlencode(payload, True)
        url = self.BASE_URL + url_path
        if query_string:
            url = url + '?' + query_string
        # print("{}".format(url))
        # response = dispatch_request('GET')(url=url)
        response = requests.get(url)
        return response.json()

    ''' ======  end of functions ====== '''
    
if __name__ == '__main__':
    
    # For public requests from Binance

    binance = Binance(BASE_URL = 'https://api.binance.com') # for Binance US
    # binance = Binance(BASE_URL = 'https://api.binance.com') # for Binance 
    # url_path = '/api/v3/klines'
    # payload = {
    #     'symbol': 'BTCUSDT',
    #     'interval': '1m'
    # }

    url_path = '/api/v3/ticker/price'

    payload = {}
    r = binance.send_public_request(url_path, payload=payload)

    from pandas import json_normalize
    print(json_normalize(r))

    # # from pandas import json_normalize
    # import pandas as pd
    # col = ['Open time','Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades',
    #        'Taker buy volume','Taker buy quote asset volume','Ignore']
    # print(pd.DataFrame(r, columns = col))
    """
    # output
             Open time            Open  ... Taker buy quote asset volume Ignore
    0    1628553600000  46266.87000000  ...            12900366.31669680      0
    1    1628640000000  45571.98000000  ...            12913585.93505232      0
    2    1628726400000  45514.26000000  ...            17928711.02609125      0
    3    1628812800000  44417.93000000  ...            13662275.65550609      0
    4    1628899200000  47808.98000000  ...            11666478.97093738      0
    ..             ...             ...  ...                          ...    ...
    495  1671321600000  16781.49000000  ...             5864401.44993415      0
    496  1671408000000  16741.57000000  ...            12000272.34997982      0
    497  1671494400000  16436.13000000  ...            19164362.31701696      0
    498  1671580800000  16898.67000000  ...             7353034.55469651      0
    499  1671667200000  16828.58000000  ...              382495.04011232      0
    """

    # # for signed requests from Binance
    # api_key = ''
    # api_secret = ''
    # binance = Binance(api_key=api_key,api_secret = api_secret,BASE_URL = 'https://api.binance.com')
    # url_path = '/api/v3/account'
    # payload = {
    # }
    # method = 'GET'
    # r = binance.send_signed_request(http_method = method, url_path = url_path, payload = payload)
    # print(r)
    


    
    
