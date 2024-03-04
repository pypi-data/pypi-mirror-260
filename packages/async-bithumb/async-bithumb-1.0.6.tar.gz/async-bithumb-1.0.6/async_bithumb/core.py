from .errors import AioHttpRequestError, BithumbPrivateError, BithumbPublicError
import asyncio
import base64, urllib, hashlib, hmac, time
import aiohttp

async def handle_rate_limit(self):
    now = time.time()
    if now - self.last_reset > 1:
        self.last_reset = now
        self.rate = self.max_rate
    if self.rate <= 0:
        print(f'Hit Bithumb rate limit, sleeping for {self.last_reset + 1 - now:.2f} seconds..')
        await asyncio.sleep(self.last_reset + 1 - now)
        self.last_reset = time.time()
        self.rate = self.max_rate
    self.rate -= 1

class PublicApi:
    def __init__(self, rate=150):
        self.last_reset = time.time() - 60
        self.max_rate = rate
        self.rate = rate

    async def ticker(self, order_currency, payment_currency="KRW"):
        await handle_rate_limit(self)
        try:
            uri = "/public/ticker/{}_{}".format(order_currency, payment_currency)
            return await BithumbHttp().get(uri)
        except AioHttpRequestError as x:
            raise BithumbPublicError(f'{x.__class__.__name__}: {x}')


    async def transaction_history(self, order_currency, payment_currency="KRW", limit=20):
        await handle_rate_limit(self)
        try:
            uri = "/public/transaction_history/{}_{}?count={}".format(order_currency, payment_currency, limit)
            return await BithumbHttp().get(uri)
        except AioHttpRequestError as x:
            raise BithumbPublicError(f'{x.__class__.__name__}: {x}')


    async def orderbook(self, order_currency, payment_currency="KRW", limit=5):
        await handle_rate_limit(self)
        try:
            uri = "/public/orderbook/{}_{}?count={}".format(order_currency, payment_currency, limit)
            return await BithumbHttp().get(uri)
        except AioHttpRequestError as x:
            raise BithumbPublicError(f'{x.__class__.__name__}: {x}')


    async def btci(self):
        await handle_rate_limit(self)
        try:
            uri = "/public/btci"
            return await BithumbHttp().get(uri)
        except AioHttpRequestError as x:
            raise BithumbPublicError(f'{x.__class__.__name__}: {x}')


    async def candlestick(self, order_currency, payment_currency="KRW", chart_intervals="24h"):
        await handle_rate_limit(self)
        try:
            uri = "/public/candlestick/{}_{}/{}".format(order_currency, payment_currency, chart_intervals)
            return await BithumbHttp().get(uri)
        except AioHttpRequestError as x:
            raise BithumbPublicError(f'{x.__class__.__name__}: {x}')



class PrivateApi:
    def __init__(self, conkey, seckey, rate= 140):
        self.http = BithumbHttp(conkey, seckey)
        self.last_reset = time.time() - 60
        self.max_rate = rate
        self.rate = rate


    async def account(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/info/account', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


    async def balance(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/info/balance', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


    async def place(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/trade/place', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


    async def orders(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/info/orders', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


    async def order_detail(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/info/order_detail', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


    async def cancel(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/trade/cancel', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


    async def market_buy(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/trade/market_buy', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


    async def market_sell(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/trade/market_sell', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


    async def withdraw_coin(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/trade/btc_withdrawal', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


    async def withdraw_cash(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/trade/krw_withdrawal', **kwargs)
        except AioHttpRequestError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


    async def user_transactions(self, **kwargs):
        await handle_rate_limit(self)
        try:
            return await self.http.post('/info/user_transactions', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')



class AioHttpMethod:
    def __init__(self, base_url=""):
        self.base_url = base_url

    def update_headers(self, headers):
        self.headers = headers

    async def post(self, path, timeout=3, **kwargs):
        return await self._request('post', path, timeout, **kwargs)

    async def get(self, path, timeout=3, **kwargs):
        return await self._request('get', path, timeout, **kwargs)

    async def _request(self, method, path, timeout, **kwargs):
        uri = self.base_url + path
        async with aiohttp.ClientSession() as session:
            if hasattr(self, 'headers'):
                session.headers.update(self.headers)

            task = asyncio.create_task(getattr(session, method)(url=uri, data=kwargs))
            async with await asyncio.wait_for(task, timeout=timeout) as response:
                try:
                    resp = await response.json()
                except Exception as x:
                    session.close()
                    raise AioHttpRequestError(f'{x.__class__.__name__}: {x}')
                finally:
                    return resp




class BithumbHttp(AioHttpMethod):
    def __init__(self, conkey="", seckey=""):
        self.API_CONKEY = conkey.encode('utf-8')
        self.API_SECRET = seckey.encode('utf-8')
        super(BithumbHttp, self).__init__("https://api.bithumb.com")


    def _signature(self, path, nonce, **kwargs):
        query_string = path + chr(0) + urllib.parse.urlencode(kwargs) + \
                       chr(0) + nonce
        h = hmac.new(self.API_SECRET, query_string.encode('utf-8'),
                     hashlib.sha512)
        return base64.b64encode(h.hexdigest().encode('utf-8'))

    async def post(self, path, **kwargs):
        kwargs['endpoint'] = path
        nonce = str(int(time.time() * 1000))

        self.update_headers({
            'Api-Key': (self.API_CONKEY).decode('utf-8'),
            'Api-Sign': (self._signature(path, nonce, **kwargs)).decode('utf-8'),
            'Api-Nonce': nonce
        })
        return await super().post(path, **kwargs)

if __name__ == "__main__":
    print(PublicApi.ticker("BTC"))