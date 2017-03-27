# -*- coding: utf-8 -*-
from twoandhalf_spider.helper.Json2Mysql import Json2Mysql
import sys


class BaseFlowNode(object):
    def __init__(self, db_conf, src=None, dst=None):
        if src:
            self.src_data_managers = [(it['table']
                                       , it['fields']
                                       ,
                                       Json2Mysql(host=db_conf['host'], user=db_conf['user'], passwd=db_conf['passwd'],
                                                  db=db_conf['db'])) for it in src]
        else:
            self.src_data_managers = None
        if dst:
            self.dst_data_managers = [(it['table']
                                       , it['schema']
                                       ,
                                       Json2Mysql(host=db_conf['host'], user=db_conf['user'], passwd=db_conf['passwd'],
                                                  db=db_conf['db'])) for it in dst]
        else:
            self.dst_data_managers = None

    def read(self):
        for i, data_manager in enumerate(self.src_data_managers):
            (table, fields, connector) = data_manager
            connector.connect()
            for record in connector.select(table, fields):
                yield (i, dict(zip(fields, record)))
            connector.disconnect()

    def save(self, records):
        for i, data_manager in enumerate(self.dst_data_managers):
            (table, schema, connector) = data_manager
            connector.connect()
            connector.create_temp_table(table, schema)
            connector.update_many([(table, [], record) for record in records[i]])
            connector.disconnect()

    def action(self):
        pass



