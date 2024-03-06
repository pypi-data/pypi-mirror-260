import os

import pymysql

from ysql import SqliteDatabase, MetaDatabase


class MysqlDatabase(MetaDatabase):
    def __init__(self):
        super().__init__()
        self.update_db_type("mysql")

    def connect(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123456')
        self.update_connection(connection)
        # 删除数据库（如果存在）
        self.cursor.execute("DROP DATABASE IF EXISTS test_database")
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS test_database")
        # 选择使用新创建的数据库
        self.cursor.execute("USE test_database")


if os.getenv('DB_IMPL') == 'sqlite':
    MetaDatabaseTest = SqliteDatabase
elif os.getenv('DB_IMPL') == 'mysql':
    MetaDatabaseTest = MysqlDatabase
