import json
import os
import re

from fundrive import LanZouSnapshot
from funread.legado.base import progress_manage, source_manage
from funtask import Task
from tqdm import tqdm


def retain_zh_ch_dig(text):
    return re.sub("[^\u4e00-\u9fa5a-zA-Z0-9\[\]]+", "", text)


class Progress:
    def __init__(self, data):
        self.data = data
        self.source = json.loads(data["source"])
        self.source["bookSourceComment"] = ""
        self.source["bookSourceUrl"] = self.source["bookSourceUrl"].rstrip("/|#")
        if "httpUserAgent" in self.source.keys():
            self.source["header"] = self.source.pop("httpUserAgent")

        for key in ["bookSourceGroup", "bookSourceName"]:
            self.source[key] = retain_zh_ch_dig(self.source.get(key, ""))

    def run(self):
        self.format_book_info()
        self.format_content()
        self.format_search()
        self.format_explore()
        self.format_toc()
        self.data["source"] = json.dumps(self.source)
        return self.data

    def __format_base(self, group, map):
        book_info = self.source.get(group, {})

        for key, name in map.items():
            if key not in self.source:
                continue
            value = self.source.pop(key)
            if value:
                book_info[name] = value
        if len(book_info) > 0:
            self.source[group] = book_info

    def format_book_info(self):
        map = {
            "ruleBookAuthor": "author",
            "ruleBookContent": "content",
            "ruleBookContentReplace": "contentReplace",
            "ruleBookInfoInit": "init",
            "ruleBookKind": "kind",
            "ruleBookLastChapter": "lastChapter",
            "ruleBookName": "name",
            "ruleBookUrlPattern": "urlPattern",
            "ruleBookWordCount": "wordCount",
        }
        self.__format_base("ruleBookInfo", map)

    def format_content(self):
        map = {
            "ruleContentUrl": "url",
            "ruleContentUrlNext": "urlNext",
            "ruleBookContentReplaceRegex": "replaceRegex",
            "ruleBookContentSourceRegex": "sourceRegex",
            "ruleBookContentWebJs": "webJs",
        }
        self.__format_base("ruleContent", map)

    def format_search(self):
        map = {
            "ruleSearchUrl": "url",
            "ruleSearchName": "name",
            "ruleSearchAuthor": "author",
            "ruleSearchList": "bookList",
            "ruleSearchCoverUrl": "coverUrl",
            "ruleSearchIntroduce": "intro",
            "ruleSearchKind": "kind",
            "ruleSearchLastChapter": "lastChapter",
            "ruleSearchNoteUrl": "noteUrl",
            "ruleSearchWordCount": "wordCount",
        }
        self.__format_base("ruleSearch", map)

    def format_explore(self):
        map = {
            "ruleFindUrl": "url",
            "ruleFindName": "name",
            "ruleFindAuthor": "author",
            "ruleFindList": "bookList",
            "ruleFindCoverUrl": "coverUrl",
            "ruleFindIntroduce": "intro",
            "ruleFindKind": "kind",
            "ruleFindLastChapter": "lastChapter",
            "ruleFindNoteUrl": "noteUrl",
        }
        self.__format_base("ruleExplore", map)

    def format_toc(self):
        map = {
            "ruleChapterList": "chapterList",
            "ruleChapterName": "chapterName",
            "ruleChapterUpdateTime": "updateTime",
            "ruleChapterUrl": "chapterUrl",
            "ruleChapterUrlNext": "nextTocUrl",
        }
        self.__format_base("ruleToc", map)


class ReadODSProgressDataTask(Task):
    def __init__(self, *args, **kwargs):
        super(ReadODSProgressDataTask, self).__init__(*args, **kwargs)
        self.url = progress_manage.url
        self.source_manage = source_manage
        self.progress_manage = progress_manage
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
        df = self.source_manage.select_all()
        # df = df[df["status"] == 2]
        df = df.sort_values("gmt_solved").reset_index(drop=True)

        def solve(row):
            try:
                self.progress_manage.upsert(Progress(data=dict(row)).run())
            except Exception as e:
                # print(e)
                # source_manage.row_solved(row["uuid"], status=1)
                pass

        tqdm.pandas(desc="source progress")
        df.progress_apply(lambda row: solve(row), axis=1)
