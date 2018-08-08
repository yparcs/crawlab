import validators
import re

from IPython.core.magic import line_magic, magics_class, Magics

import scrapy
from crawlab.context_manager import ContextManager


@magics_class
class MagicCrawler(Magics):
    def __init__(self, shell, crawler):
        super(MagicCrawler, self).__init__(shell)

        self.cm = ContextManager(shell)
        self.crawler = crawler

    @line_magic
    def fetch(self, request):
        if type(request) is str:
            request = self._get_request_by_cmd(request)

        response = self.crawler.fetch(request)
        self.cm.set('response', response)

        return response

    @line_magic
    def xpath(self, code):
        return self._execute_selector_fn('xpath', code)

    @line_magic
    def css(self, code):
        return self._execute_selector_fn('css', code)

    @line_magic
    def item(self, code=None, **kwargs):
        if code and type(code) is str:
            kwargs = self.cm.execute_and_get('dict({})'.format(code))

        item_attrs = {k: scrapy.Field() for k in kwargs.keys()}
        item_cl = type('MagicItem', (scrapy.Item,), item_attrs)
        return item_cl(**kwargs)

    def _get_request_by_cmd(self, request):
        if validators.url(request):
            return scrapy.Request(request)
        return self.cm.execute_and_get(request)

    def _execute_selector_fn(self, selector_fn, code):
        commands = self._extract_commands(code)
        result = getattr(self.cm.get('response'), selector_fn)(commands.get('expr'))
        target = commands.get('target')
        if target:
            self.cm.set(target, result)
        return result

    @staticmethod
    def _extract_commands(code):
        match = re.match('(?P<expr>[^\s\>]*)(\s(?P<sep>\>)(\s*)(?P<target>.*))?', code)
        if not match:
            raise Exception('Wrong command')
        return match.groupdict()
