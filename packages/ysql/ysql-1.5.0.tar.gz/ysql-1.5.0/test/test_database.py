# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from test.test_env import MetaDatabaseTest
from ysql import Entity, Constraint as cs, Dao, DaoFunc


@Entity
@dataclass
class Student_Comment:
    name: str = cs.comment('学生姓名')
    contact_info: float = cs.comment('联系方式')
    time: str = cs.comment('时间')
    abstract: str = cs.comment('摘要')
    student_id: int = cs.auto_primary_key, cs.comment('学生id')


@Dao(Student_Comment)
class DaoStudent(DaoFunc):
    pass


class Database(MetaDatabaseTest):
    dao_student = DaoStudent()


@pytest.fixture(scope="session")
def database_class():
    return Database


# ====================================================================================================================
def test_create_tables(init_db):
    """建库"""
    db = init_db
    db.create_tables()


def test_create_with_comment(init_db):
    """注释功能"""
    db = init_db
    db.dao_student.create_table()


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
