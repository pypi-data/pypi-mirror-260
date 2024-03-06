# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from test.test_env import MetaDatabaseTest
from ysql import Entity, Constraint as cs, Dao, DaoFunc


@Entity
@dataclass
class Student:
    name: str
    age: int
    phone: int = cs.not_null
    weight: float = 50.0, cs.not_null
    height: float = cs.not_null, cs.unique
    address: str = 'hit', cs.not_null, cs.unique, cs.datatype("varchar(200)")
    student_id: int = cs.auto_primary_key
    if_aged: bool = False


@Dao(Student)
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


def test_create(init_db):
    db = init_db
    db.dao_student.create_table()


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
