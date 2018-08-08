import os
import wget
import tarfile
import tempfile

from crawlab.settings import ZAP_VERSION

name = 'ZAP_{}_Core.tar.gz'.format(ZAP_VERSION)
url = 'https://github.com/zaproxy/zaproxy/releases/download/{}/{}'.format(ZAP_VERSION, name)

filename = wget.download(url, out=os.path.join(tempfile.gettempdir(), name))

tar = tarfile.open(filename)
tar.extractall()
tar.close()