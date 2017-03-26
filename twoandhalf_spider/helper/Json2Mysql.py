# -*- coding: utf-8 -*-
from MysqlHelper import MysqlHelper


class Json2Mysql(MysqlHelper):

    def __init__(self, host, user, passwd, db):
        super(MysqlHelper, self).__init__(host, user, passwd, db)

    def update_many(self, records):
        sqls = []
        self.connect()
        for (table, ukeys, record) in records:
            k_list, v_list, u_list = [], [], []
            for k, v in record.items():
                k = k.encode('utf-8')
                k_list.append(k)
                if type(v) is str:
                    v = '\''+self.escape_string(v)+'\''
                elif type(v) is unicode:
                    v = '\'' + self.escape_string(v.encode('utf-8'))+'\''
                else:
                    v = str(v)
                v_list.append(v)
                if k not in ukeys:
                    u_list.append("%s=%s" % (k, v))
            fields = ",".join(k_list)
            values = ",".join(v_list)
            updates = ",".join(u_list)
            if updates:
                sqls.append("INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" % (table, fields, values, updates))
            else:
                sqls.append(
                    "INSERT INTO %s (%s) VALUES (%s)" % (table, fields, values))
        self.batch_insert(sqls)
        self.disconnect()


if __name__ == "__main__":
    pass