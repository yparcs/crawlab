import html

from IPython.display import display
import ipywidgets
from ipywidgets import Layout, HTML
from traitlets import Unicode, Dict
from bs4 import BeautifulSoup

from crawlab.utils import highlight_html


@ipywidgets.register
class NetworkWidget(ipywidgets.VBox):
    
    def __init__(self, messages):
        messages_widgets = []
        for message in messages:
            messages_widgets += [self._network_box(message['request']), self._network_box(message['response'])]
        super(NetworkWidget, self).__init__(messages_widgets)

    @staticmethod
    def _box(box_widgets):
        return ipywidgets.VBox(box_widgets, layout=Layout(
            border='1px solid gray', padding='3px', margin='3px'))

    def _network_box(self, message):
        return self._box([
            self._title(message['title']),
            self._title_text_box('Header', message['header']),
            self._title_text_box('Body', message['body']),
        ])

    @staticmethod
    def _title(title):
        return ipywidgets.HTML(value='<b>' + title + '</b>')

    def _title_text_box(self, title, text):
        text_box_widgets = [self._title(title)]
        if text:
            text_box_widgets.append(self._box([ipywidgets.HTML(value=text)]))
        return self._box(text_box_widgets)


@ipywidgets.register
class BrowserWidget(ipywidgets.DOMWidget):
    _view_name = Unicode('BrowserView').tag(sync=True)
    _view_module = Unicode('crawlab').tag(sync=True)
    
    srcdoc = Unicode('srcdoc').tag(sync=True)
    
    def __init__(self, srcdoc='', **kwargs):
        self.srcdoc = srcdoc
        
        super(BrowserWidget, self).__init__(**kwargs)


@ipywidgets.register
class ResponseWidget(ipywidgets.Tab):
    def __init__(self, response, messages, log_handler):
        children = [
            ('Browser', BrowserWidget(srcdoc=html.escape(response.text))),
            ('Code', ipywidgets.HTML(highlight_html(response.text))),
            ('Logs', log_handler.out),
            ('Network', NetworkWidget(messages=messages))
        ]

        super(ResponseWidget, self).__init__([widget for name, widget in children], layout={'height': '300px'})

        for i, widget in enumerate(children):
            self.set_title(i, widget[0])


@ipywidgets.register
class SelectorResultWidget(ipywidgets.VBox):
    def __init__(self, selector):
        self.title = 'Result'
        results = []
        for data_str in selector.extract():
            code_widget = ipywidgets.HTML(highlight_html(data_str))
            box = ipywidgets.VBox([code_widget], layout=Layout(border='1px solid gray', padding='3px', margin='3px'))
            results.append(box)
        super(SelectorResultWidget, self).__init__(results)


@ipywidgets.register
class SelectorWidget(ipywidgets.Tab):

    def __init__(self, selector):
        children = [
            ('Result', SelectorResultWidget(selector)),
            ('Code', ipywidgets.HTML(self._format_code(selector)))
        ]

        super(SelectorWidget, self).__init__([widget for name, widget in children])

        for i, widget in enumerate(children):
            self.set_title(i, widget[0])

    def _format_code(self, selector):
        if len(selector) > 0:
            start_mark = '{mark}'
            end_mark = '{/mark}'

            marked_code = ''.join(selector[0].xpath('/*').extract())
            for tag in selector.extract():
                marked_code = marked_code.replace(tag, start_mark + tag + end_mark)

            highlighted_code = highlight_html(marked_code)
            prettify_html = BeautifulSoup(highlighted_code, 'html.parser').prettify()

            return prettify_html\
                .replace(start_mark, '<mark style="background-color: yellow;">').replace(end_mark, '</mark>')

        return 'Not found'


class JsonWidget(ipywidgets.DOMWidget):
    _view_name = Unicode('JsonView').tag(sync=True)
    _view_module = Unicode('crawlab').tag(sync=True)
    
    data = Dict({}).tag(sync=True)
    
    def __init__(self, data, **kwargs):
        self.data = dict(data)
        css = """
            .mark-water{
                color:#bbb;
            }
            .node-content-wrapper{
                font-family: 'Quicksand', sans-serif;
                background-color:#fff;
            }
            .node-content-wrapper ul{
                border-left:1px dotted #ccc;
                list-style:none;
                padding-left:25px;
                margin:0px;
            }
            .node-content-wrapper ul li{
                list-style:none;
                border-bottom:0;
                padding-bottom:0
            }
            .node-hgl-path{
                background-color:#fefbdf;
            }
            .node-bracket{
                font-weight:bold;
                display:inline-block;
                cursor:pointer;
            }
            .node-bracket:hover{
                color:#999;
            }
            .leaft-container{
                width:100%;
                max-width:300px;
                height:100%;
            }
            .title{ color:#ccc;}
            .string{ color:#080;}
            .number{ color:#ccaa00;}
            .boolean{ color:#1979d3;}
            .date{ color:#aa6655;}
            .null{ color:#ff5050;}
        """
        display(HTML('<style>' + css + '</style>'))

        super(JsonWidget, self).__init__(**kwargs)

