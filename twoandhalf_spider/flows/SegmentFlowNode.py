# -*- coding: utf-8 -*-
from twoandhalf_spider.flows.BaseFlowNode import BaseFlowNode
from twoandhalf_spider.conf.mysql import host, user, passwd, db
import jieba


class SegmentFlowNode(BaseFlowNode):
    def __init__(self, host, user, passwd, db, src, dst):
        super(SegmentFlowNode, self).__init__(host=host, user=user, passwd=passwd, db=db, src=src, dst=dst)
        self.src_fields = src['fields']
        self.content_index = src['content_index']
        self.content_field = self.src_fields[self.content_index]

    def segment(self):
        for record in self.read():
            text = record[self.content_field]
            record[self.content_field] = " ".join(jieba.cut(text))
            yield record

    def action(self):
        records = self.segment()
        self.save(records)


if __name__ == "__main__":
    src = {
        "table": "weibo_post",
        "fields": ["id", "body"],
        "content_index": 1
    }

    dst = {
        "table": "weibo_post_seg",
        "fields": ["id", "body"],
        "schema": [
            ("id", "varchar(45)"),
            ("body", "text")
        ]
    }

    segment = SegmentFlowNode(host=host, user=user, passwd=passwd, db=db, src=src, dst=dst)
    segment.action()