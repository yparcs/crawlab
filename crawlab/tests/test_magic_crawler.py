from unittest.mock import patch, MagicMock

from crawlab import Crawler
from crawlab.magic_crawler import MagicCrawler
from crawlab.tests.crawlab_case import CrawLabCase
import scrapy
from scrapy.http import HtmlResponse


class MockedResponse(HtmlResponse):
    def __init__(self):
        super(MockedResponse, self).__init__('http://test.url', body=b'<html>test<a>link</a></html>')


class MockedRequest:
    meta = {'proxy': ''}
    callback = None


class MockedIPython:
    class MockedEvents:
        def register(self, event, callback):
            return

    class MockedKernel:
        def do_execute(self, code, silent, store_history=False):
            return

    events = MockedEvents()
    kernel = MockedKernel()
    user_ns = {'request': MockedRequest(), 'response': MockedResponse()}


class CrawLabTest(CrawLabCase):
    def setUpTest(self):
        ip = MockedIPython()
        crawler = Crawler()
        self.magic_crawler = MagicCrawler(ip, crawler)

    @patch('scrapydo.fetch', MagicMock(return_value=True))
    def test_fetch(self):
        req = scrapy.Request('http://test.com')
        resp = self.magic_crawler.fetch(req)
        self.assertIsNotNone(resp)

    def test_xpath(self):
        resp = self.magic_crawler.xpath('//a')
        self.assertEquals('<a>link</a>', resp[0].extract())

    def test_css(self):
        resp = self.magic_crawler.css('a')
        self.assertEquals('<a>link</a>', resp[0].extract())

    def test_item(self):
        item = self.magic_crawler.item(test='item')
        self.assertEquals({'test': 'item'}, item)
