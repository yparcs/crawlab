import subprocess
import os
import html
from time import sleep
import logging

from zapv2 import ZAPv2

from crawlab.settings import ZAP_PATH

logger = logging.getLogger('Proxy')


class ZapProxy:
    def __init__(self, host='127.0.0.1', port='8080'):
        self.host = host
        self.port = port
        self.client = ZAPv2(apikey=None, proxies={'http': self.get_url()})
        self.started = False

    def get_url(self):
        return 'http://{}:{}'.format(self.host, self.port)

    def start_server(self):
        self.started = self.is_running()
        if not self.started:
            cmd = [ZAP_PATH, '-config api.disablekey=true', '-daemon', '-host', self.host, '-port', self.port]
            try:
                resp = subprocess.Popen(cmd, stdout=open(os.devnull, 'w'))
                self.started = self._wait_for_server()
                if not self.started:
                    logger.error('Proxy not started, process :' + str(resp))
            except FileNotFoundError:
                logger.error('ZAP proxy not found')
        return self.started

    def get_messages(self, site_url=None):
        messages = []
        if self.started:
            messages = self.client.core.messages(baseurl=site_url)
        return [self._format_message(message) for message in messages]

    def delete_messages(self, site_url):
        return self.client.core.delete_site_node(site_url)

    def is_running(self):
        try:
            self.client.urlopen(self.get_url())
        except Exception as e:
            logger.debug(e)
            return False
        return True

    def _format_message(self, message):
        return {
            'request': {
                'title': 'Request',
                'header': message['requestHeader'],
                'body': html.escape(message['requestBody'])
            },
            'response': {
                'title': 'Response',
                'header': message['responseHeader'],
                'body': html.escape(message['responseBody'])
            }
        }

    def _wait_for_server(self, max_seconds=20):
        logger.info('starting proxy server..')
        for i in range(max_seconds):
            if self.is_running():
                logger.info('started!')
                return True
            sleep(1)
        return False
