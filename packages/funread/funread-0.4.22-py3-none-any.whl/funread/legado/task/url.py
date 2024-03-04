import os

from fundrive import LanZouSnapshot
from funread.legado.base import url_manage
from funread.legado.base.url import DataType
from funtask import Task


class ReadODSUrlDataTask(Task):
    def __init__(self, *args, **kwargs):
        super(ReadODSUrlDataTask, self).__init__(*args, **kwargs)
        self.url = url_manage.url
        self.url_manage = url_manage
        self.snapshot = LanZouSnapshot(fid="8822098", url="https://bingtao.lanzoub.com/b01lj2vxi", pwd="4jn0")

    def example(self, *args, **kwargs):
        self.snapshot_download()
        self.add_book_source("https://bitbucket.org/xiu2/yuedu/raw/master/shuyuan")
        self.snapshot_upload()

    def snapshot_download(self):
        self.snapshot.download(os.path.dirname(self.url))

    def snapshot_upload(self):
        self.snapshot.update(self.url)

    def add_book_source(self, url, cate1='default', *args, **kwargs):
        self.url_manage.add_source(url, cate1, type=DataType.BOOK, *args, **kwargs)

    def add_rss_source(self, url, cate1='default', *args, **kwargs):
        self.url_manage.add_source(url, cate1, type=DataType.RSS, *args, **kwargs)
   