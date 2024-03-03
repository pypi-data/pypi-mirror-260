import json
from datetime import datetime

from fundrive import GithubDrive
from funsecret import read_secret
from tqdm import tqdm

read_secret(cate1="funread", cate2="legado", cate3="sqlite", cate4="path", value="/home/bingtao/workspace/hubs/funread-dat/db/")

from funread.legado.base import url_manage
from funread.legado.load.url import load_data1, load_yck_ceo
from funread.legado.base import progress_manage
from funread.legado.base import source_manage


def run1():
    url_manage.snapshot_download()
    load_data1()
    load_yck_ceo(book_size=2000)
    url_manage.snapshot_upload()


def run2():
    source_manage.snapshot_download()
    source_manage.progress(url_manage)
    source_manage.snapshot_upload()


def run3():
    progress_manage.snapshot_download()
    progress_manage.progress(source_manage)
    progress_manage.snapshot_upload()


def run4():
    # progress_manage.snapshot_download()
    data = progress_manage.select_all()["source"].to_list()
    data = [json.loads(item) for item in data]
    print(len(data))
    drive = GithubDrive()
    drive.login(repo_str="farfarfun/funread-cache")
    dir_path = f"funread/legado/book/snapshot/{datetime.now().strftime('%Y%m%d')}"
    step = 1000
    for i in tqdm(range(0, len(data), step)):
        drive.upload_file(content=data[i : i + 1000], git_path=f"{dir_path}/progress-{i / step + 1}.json")


url_manage.snapshot_download()
source_manage.snapshot_download()
progress_manage.snapshot_download()
# run1()
# run2()
# run3()
# run4()
