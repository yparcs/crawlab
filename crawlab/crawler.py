import scrapydo
from crawlab.proxy import ZapProxy
from crawlab.utils import create_handler


class Crawler:
    def __init__(self, ):
        self.proxy = ZapProxy()
        self.log_handlers = {}
        scrapydo.setup()

    def get_proxy(self):
        return self.proxy.get_url()

    def get_handler(self, key):
        return self.log_handlers.get(key, create_handler())

    def get_messages(self, url):
        return self.proxy.get_messages(url)

    def configure_proxy(self, request):
        if not self.proxy.started:
            started = self.proxy.start_server()
            if not started:
                raise Exception('Proxy not started')
        self.proxy.delete_messages(request.url)

    def fetch(self, request):
        if request.meta.get('proxy') == self.get_proxy():
            self.configure_proxy(request)

        callback = None
        if request.callback:
            callback = request.callback
            request.callback = None

        if not self.log_handlers.get(request.url):
            self.log_handlers[request.url] = create_handler()
        self.log_handlers[request.url].clear_logs()

        response = scrapydo.fetch(request)

        if callback:
            callback(response)

        return response
