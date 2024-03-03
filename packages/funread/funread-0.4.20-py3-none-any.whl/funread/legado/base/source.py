import json
from datetime import datetime

from fundb.sqlalchemy import Base
from fundb.sqlalchemy import BaseTable, create_engine_sqlite
from funsecret import get_md5_str
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import mapped_column


class ReadODSSourceData(Base):
    __tablename__ = "read_ods_source"

    uuid = mapped_column(String(100), comment="源md5", primary_key=True, default="")
    url_uuid = mapped_column(String(100), comment="id", default=1)
    status = mapped_column(Integer, comment="status", default=2)
    # 创建时间
    gmt_create = mapped_column(DateTime(timezone=True), server_default=func.now())
    # 修改时间：当md5不一致时更新
    gmt_modified = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # 更新时间，当重新拉取校验时更新
    gmt_updated = mapped_column(DateTime(timezone=True), server_default=func.now())
    # 下游处理时间，下游拉数据时更新
    gmt_solved = mapped_column(DateTime(timezone=True), server_default=func.now())
    source = mapped_column(String(100000), comment="源", default="")


class ReadODSSourceDataManage(BaseTable):
    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        engine = create_engine_sqlite(url)
        super(ReadODSSourceDataManage, self).__init__(table=ReadODSSourceData, engine=engine, *args, **kwargs)

    def row_upsert(self, source, url_uuid):
        source = json.dumps(source)
        data = {
            "uuid": get_md5_str(source),
            "url_uuid": url_uuid,
            "source": source,
        }
        self.upsert(data)

    def row_solved(self, uuid, status=2) -> bool:
        data = {"uuid": uuid, "gmt_solved": datetime.now(), "status": status}
        self.upsert(data)
        return True
