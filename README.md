crawlab
===============================

An interactive toolkit for web crawler

Installation
------------

To install use pip:

    $ pip install crawlab
    $ jupyter nbextension enable --py --sys-prefix crawlab


For a development installation (requires npm),

    $ git clone https://github.com/fabiocariati/crawlab.git
    $ cd crawlab
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix crawlab
    $ jupyter nbextension enable --py --sys-prefix crawlab
