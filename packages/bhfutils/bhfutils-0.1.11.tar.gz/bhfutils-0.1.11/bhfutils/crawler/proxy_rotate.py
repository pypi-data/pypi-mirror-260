class ProxyRotateMiddleware(object):
    '''
    Ensures the proxy from the response is passed
    when response status code is 429.
    
    Usage: 

    settings.py ->

    ...
    PROXIES = ['http://127.0.0.1:8080']

    ...

    DOWNLOADER_MIDDLEWARES = {
        ...
        'bhfutils.crawler.proxy_rotate.ProxyRotateMiddleware': 800
    }
    '''
    def __init__(self, settings):
        self.proxies = settings.get('PROXIES')
        self.proxy_queue = self.get_proxy()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def get_proxy(self):
        while self.proxies:
            for proxy in self.proxies:
                yield proxy
        raise LookupError('Proxies not found. Set PROXIES in settings! Use format [http://user:password@ip:port] for proxies.')

    def process_response(self, request, response, spider):
        if response.status in [302, 407, 429]:
            request.meta['proxy'] = next(self.proxy_queue)
            request.dont_filter = True
            return request
        else:
            return response
