# -*- coding: utf-8 -*-
import sys
import json
from Json2Mysql import Json2Mysql
import logging
from twoandhalf_spider.conf.mysql import host, user, passwd, db

batch_size = 1000
table_profile = "crawler_xiabb.weibo_profile"
table_post = "crawler_xiabb.weibo_post"


class WeiboJsonFile2Mysql(Json2Mysql):
    def __init__(self, host, user,passwd, db, batch_size):
        super(Json2Mysql, self).__init__(host, user, passwd, db)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.batch_size = batch_size

    def store(self, filename):
        with open(filename) as f:
            queue = []
            cnt = 0
            for line in f:
                json_obj = json.loads(line.strip())

                if 'nick_name' in json_obj:
                    if '_id' in json_obj:
                        json_obj['userid'] = json_obj['_id']
                        del json_obj['_id']
                    queue.append((table_profile, ['userid'], json_obj))
                    cnt += 1
                elif 'body' in json_obj:
                    if '_id' in json_obj:
                        json_obj['id'] = json_obj['_id']
                        del json_obj['_id']
                    queue.append((table_post, ['id'], json_obj))
                    cnt += 1
                if cnt % batch_size == 0:
                    self.update_many(queue)
                    self.logger.info("%d records inserted" % cnt)
                    queue = []
            if len(queue) > 0:
                self.update_many(queue)
            self.logger.info("finished(%d records)" % cnt)


if __name__ == "__main__":
    filename = sys.argv[1]
    wb_json_store = WeiboJsonFile2Mysql(host=host, user=user, passwd=passwd, db=db, batch_size=batch_size)
    wb_json_store.store(filename)
