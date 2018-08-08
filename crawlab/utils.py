import logging
import re
import sys

import ipywidgets
from scrapydo.utils import highlight

from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonTracebackLexer, PythonLexer
from fabric.colors import blue, cyan, green, magenta, red

lexer = PythonLexer()
python_traceback_lexer = PythonTracebackLexer()
terminal_formatter = TerminalFormatter()
re_color_codes = re.compile(r'\033\[(\d;)?\d+m')


LEVELS = {
    'INFO': blue('INFO'),
    'DEBUG': blue('DEBUG'),
    'WARNING': red('WARN', bold=True),
    'CRITICAL': magenta('CRIT'),
    'ERROR': red('ERROR'),
}


class ScrapyFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self)

    def format(self, record):
        s = '%(levelname)s %(name)s %(message)s' % {
            'levelname': LEVELS[record.levelname],
            'name': cyan(record.name),
            'message': record.getMessage()
        }

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            try:
                exc_text = record.exc_text
            except UnicodeError:
                exc_text = record.exc_text.decode(sys.getfilesystemencoding())
            s += highlight(exc_text, python_traceback_lexer, terminal_formatter)

        return s


class OutputWidgetHandler(logging.Handler):

    def __init__(self):
        super(OutputWidgetHandler, self).__init__()
        self.out = ipywidgets.Output()

    def emit(self, record):
        formatted_record = self.format(record)
        new_output = {
            'name': 'stdout',
            'output_type': 'stream',
            'text': formatted_record+'\n'
        }
        self.out.outputs = self.out.outputs + (new_output, )

    def clear_logs(self):
        self.out.clear_output()


def create_handler():
    handler = OutputWidgetHandler()
    handler.setFormatter(ScrapyFormatter())
    logger = logging.getLogger('scrapy')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return handler


def highlight_html(code):
    return highlight(code, output_wrapper=str).replace('<body>\n<h2></h2>\n\n', '<body>')