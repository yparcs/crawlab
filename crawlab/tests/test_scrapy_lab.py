from IPython.display import display
from scrapy.selector import SelectorList
from scrapy.item import Item
from crawlab import configure_display
from crawlab.tests.crawlab_case import CrawLabCase
from scrapy.http.response.html import HtmlResponse
from scrapy.http.response.text import TextResponse
from scrapy.http.response.xml import XmlResponse


class CrawLabTest(CrawLabCase):

    def test_displays(self):
        configure_display()

        self.assertTrue(hasattr(HtmlResponse, '_ipython_display_'))
        self.assertTrue(hasattr(TextResponse, '_ipython_display_'))
        self.assertTrue(hasattr(XmlResponse, '_ipython_display_'))
        self.assertTrue(hasattr(SelectorList, '_ipython_display_'))
        self.assertTrue(hasattr(Item, '_ipython_display_'))

    def test_display_response_without_return(self):
        response = HtmlResponse(body=b'<html>test</html>', url='http://some.url', status=200)
        resp = display(response)
        self.assertIsNone(resp)

    def test_display_selector_without_return(self):
        selector = HtmlResponse(body=b'<html>test</html>', url='http://some.url', status=200).xpath('//html')
        resp = display(selector)
        self.assertIsNone(resp)
