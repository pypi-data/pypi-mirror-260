# -*- coding:utf-8 -*-
from dataclasses import asdict, dataclass

import pytest

from test.test_env import MetaDatabaseTest
from ysql import Entity, Constraint as cs, Dao, Insert


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


@Dao(entity=Student, fetch_type=dataclass)
class DaoStudent:
    """不使用DaoFuncs类"""

    @Insert
    def insert(self, entity):
        pass

    def select_one_student(self, student_id: int):
        sql = "select * from student where student_id=?;"
        return self.execute(sql=sql, args=[student_id])

    def select_one_student_with_substitute(self, student_id: int):
        sql = "select * from __ where student_id=? limit 1;"
        return self.execute(sql=sql, args=[student_id])

    def select_one_student_with_limit(self, student_id: int):
        sql = "select * from student where student_id=? limit 1;"
        return self.execute(sql=sql, args=[student_id])

    def select_one_student_with_substitute_and_limit(self, student_id: int):
        sql = "select * from __ where student_id=? limit 1;"
        return self.execute(sql=sql, args=[student_id])

    def select_student_with_conditions(self, student_id: int, age: int):
        sql = "select * from student where student_id=? and age=? limit 1;"
        return self.execute(sql=sql, args=[student_id, age])


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
def test_execute_sql_without_dao_func(init_db: Database):
    """执行sql方法"""
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_one_student(student_id=select_id)
        assert isinstance(result, list)
        assert result
        assert asdict(result[0]) == asdict(students[select_id])


def test_execute_sql_with_substitute_without_dao_func(init_db: Database):
    """执行sql方法，使用替代符"""
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_one_student_with_substitute(student_id=select_id)
        assert asdict(result) == asdict(students[select_id])


def test_execute_sql_with_limit_without_dao_func(init_db: Database):
    """执行sql方法，使用limit"""
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_one_student_with_limit(student_id=select_id)
        assert asdict(result) == asdict(students[select_id])


def test_execute_sql_with_substitute_and_limit_without_dao_func(init_db: Database):
    """执行sql方法，使用替代符和limit"""
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_one_student_with_substitute_and_limit(student_id=select_id)
        assert asdict(result) == asdict(students[select_id])


def test_execute_sql_with_conditions_without_dao_func(init_db: Database):
    """执行sql方法，使用替代符和limit"""
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_student_with_conditions(student_id=select_id, age=select_id)
        assert asdict(result) == asdict(students[select_id])


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
