# -*- coding: utf-8 -*-
import MySQLdb
import sys

class MysqlHelper(object):
    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.cursor = None
        self.connection = None

    def connect(self):
        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset='utf8mb4', init_command='SET NAMES UTF8')
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection and self.cursor:
            self.cursor.close()

    def escape_string(self, string):
        return MySQLdb.escape_string(string)

    def batch_insert(self, sqls):
        for sql in sqls:
            #print sql
            try:
                self.cursor.execute(sql)
            except Exception, e:
                print >>sys.stderr, e
                sys.exit(1)
        # commit
        try:
            self.connection.commit()
        except Exception, e:
            print >> sys.stderr, e

    def create_temp_table(self, table, schema):
        sql = """
        CREATE TABLE IF NOT EXISTS %s (%s) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """ % (table, ",".join([k+" "+v for (k, v) in schema]))
        print >> sys.stderr, sql
        self.cursor.execute(sql)

    def select(self, table, fields):
        sql = """
        SELECT %s FROM %s
        LIMIT 1000
        """ % (",".join(fields), table)
        print >> sys.stderr, sql
        self.cursor.execute(sql)
        for record in self.cursor:
            yield record
        self.cursor.close()
