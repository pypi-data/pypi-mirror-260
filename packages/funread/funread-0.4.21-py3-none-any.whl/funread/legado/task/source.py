import os

import requests
from fundrive import LanZouSnapshot
from funread.legado.base import source_manage, url_manage
from funtask import Task
from tqdm import tqdm


class ReadODSSourceDataTask(Task):
    def __init__(self, *args, **kwargs):
        super(ReadODSSourceDataTask, self).__init__(*args, **kwargs)
        self.url = source_manage.url
        self.url_manage = url_manage
        self.source_manage = source_manage
        self.snapshot = LanZouSnapshot(fid="8822120", url="https://bingtao.lanzoub.com/b01lj2wja", pwd="fn3k")

    def run(self, *args, **kwargs):
        self.snapshot_download()
        self.progress()
        self.snapshot_upload()

    def snapshot_download(self):
        self.snapshot.download(os.path.dirname(self.url))

    def snapshot_upload(self):
        self.snapshot.update(self.url)

    def progress(self):
        df = self.url_manage.select_all()
        # df = df[df["status"] == 2]
        df = df.sort_values("gmt_solved").reset_index(drop=True)

        def solve(row):
            try:
                response = requests.get(row["url"])
                for source in response.json():
                    self.source_manage.row_upsert(url_uuid=row["uuid"], source=source)
                self.url_manage.row_solved(row["uuid"])
            except Exception:
                self.url_manage.row_solved(row["uuid"], status=1)

        tqdm.pandas(desc="download source")
        df.progress_apply(lambda row: solve(row), axis=1)
