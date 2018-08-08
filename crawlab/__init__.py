from crawlab.crawler import Crawler
from crawlab.magic_crawler import MagicCrawler

from scrapy.http.response.html import HtmlResponse
from scrapy.http.response.text import TextResponse
from scrapy.http.response.xml import XmlResponse
from scrapy.selector.unified import SelectorList
from scrapy.item import Item
from crawlab.utils import OutputWidgetHandler

from ._version import version_info, __version__

from .widgets import *

crawler = Crawler()


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'crawlab',
        'require': 'crawlab/extension'
    }]


def configure_display():
    for resp_class in [HtmlResponse, TextResponse, XmlResponse]:
        resp_class._ipython_display_ = \
            lambda r: display(ResponseWidget(r, crawler.get_messages(r.url), crawler.get_handler(r.url)))

    SelectorList._ipython_display_ = lambda s: display(SelectorWidget(s))
    Item._ipython_display_ = lambda i: display(JsonWidget(i))


def load_ipython_extension(ip):
    configure_display()
    mc = MagicCrawler(ip, crawler)
    ip.register_magics(mc)
