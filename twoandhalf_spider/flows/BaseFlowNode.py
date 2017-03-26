# -*- coding: utf-8 -*-
from twoandhalf_spider.helper.Json2Mysql import Json2Mysql
import sys

class BaseFlowNode(object):
    def __init__(self, host, user, passwd, db, src=None, dst=None):
        if src:
            self.src_table = src['table']
            self.src_fields = src['fields']
            self.src_data_manager = Json2Mysql(host=host, user=user, passwd=passwd, db=db)
        else:
            self.src_data_manager = None
        if dst:
            self.dst_table = dst['table']
            self.dst_schema = dst['schema']
            self.dst_data_manager = Json2Mysql(host=host, user=user, passwd=passwd, db=db)
        else:
            self.dst_data_manager = None

    def read(self):
        self.src_data_manager.connect()
        for record in self.src_data_manager.select(self.src_table, self.src_fields):
            yield dict(zip(self.src_fields, record))
        self.src_data_manager.disconnect()

    def save(self, records):
        self.dst_data_manager.connect()
        self.dst_data_manager.create_temp_table(self.dst_table, self.dst_schema)
        self.dst_data_manager.update_many([(self.dst_table, [], record) for record in records])
        self.dst_data_manager.disconnect()

    def action(self):
        pass



