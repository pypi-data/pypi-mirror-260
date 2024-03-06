# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from test.test_env import MetaDatabaseTest
from ysql import Entity, Constraint as cs, Dao, DaoFunc, Sql


@Entity(check_type=True)
@dataclass
class Student:
    name: str
    age: int
    phone: int = cs.not_null
    weight: float = 50.0, cs.not_null
    height: float = cs.not_null, cs.unique
    address: str = 'hit', cs.not_null, cs.unique, cs.datatype("varchar(200)")
    student_id: int = cs.primary_key
    if_aged: bool = False


@Dao(Student, fetch_type=Student)
class DaoStudent(DaoFunc):

    @Sql("select if_aged from __ limit 1;", fetch_type=bool)
    def select_bool(self):
        pass

    @Sql("select if_aged from __ limit 1;")
    def select_bool_no_return_bool(self):
        pass


class Database(MetaDatabaseTest):
    dao_student = DaoStudent()


@pytest.fixture(scope="session")
def database_class():
    return Database


# ====================================================================================================================
def generate_students(start, end):
    return [
        Student(name=f'李华{i}', age=i, phone=123456789,
                weight=50.0, height=100.0 + i, address=f'hit{i}',
                student_id=i)
        for i in range(start, end)
    ]


def insert_data(db: Database, num=100):
    students = generate_students(0, num)
    db.dao_student.insert(students)
    db.commit()
    return students


# ====================================================================================================================
def test_bool(init_db: Database):
    db = init_db
    insert_data(db, 1000)
    result1 = db.dao_student.select_bool()
    result2 = db.dao_student.select_bool_no_return_bool()
    assert type(result1) == bool
    assert type(result2.if_aged) == int


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
