# -*- coding: utf-8 -*-
from twoandhalf_spider.flows.BaseFlowNode import BaseFlowNode
import jieba

host = "127.0.0.1"
user = "root"
passwd = "Root@1234"
db = "crawler_xiabb"


class SegmentFlowNode(BaseFlowNode):
    def __init__(self, host, user, passwd, db, src, dst):
        super(BaseFlowNode, self).__init__(host=host, user=user, passwd=passwd, db=db, src=src, dst=dst)
        self.content_index = src['content_index']

    def segment(self):
        records = self.read()
        ret = []
        for record in records:
            text = record[self.content_index]
            record[self.content_index] = jieba.cut(text)
            ret.append(record)
        return ret

    def action(self):
        records = self.segment()
        self.save(records)


if __name__ == "__main__":
    src = {
        "table": "crawler_xiabb.weibo_post",
        "fields": ["id", "body"],
        "content_index": 1,
        "preserve": ["id"]
    }

    dst = {
        "table": "crawler_xiabb.weibo_post_seg",
        "fields": ["id", "body"],
        "schema": {
            "id": "varchar()",
            "body": "text"
        }
    }

    segment = SegmentFlowNode(host=host, user=user,passwd=passwd,db=db, src=src, dst=dst)
    segment.action()