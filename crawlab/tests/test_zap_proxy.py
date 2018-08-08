from unittest.mock import MagicMock, patch

from crawlab.tests.crawlab_case import CrawLabCase
from crawlab.proxy import ZapProxy


class ZapProxyTest(CrawLabCase):
    def setUpTest(self):
        pass

    @patch('subprocess.Popen', MagicMock(return_value=True))
    def test_should_start_zap(self):
        self.zap_proxy = ZapProxy(host='test')
        self.assertIsNotNone(self.zap_proxy)