# -*- coding:utf-8 -*-
from dataclasses import asdict, dataclass

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


@Dao(entity=Student, fetch_type=dataclass)
class DaoStudent(DaoFunc):
    @Sql("select * from student where student_id=?;", fetch_type=Student)
    def select_student_by_id(self, student_id):
        pass

    @Sql("delete from student where student_id=?;")
    def delete_student_by_id(self, student_id):
        pass

    @Sql("select * from __ where student_id=?;", fetch_one=True, fetch_type=Student)
    def select_student_by_id_use_fetch_one(self):
        pass

    @Sql("select * from student where student_id=? limit 1;", fetch_type=Student)
    def select_student_by_id_limit1(self, student_id):
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
def test_fetchone(init_db: Database):
    """查询单记录"""
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result1 = db.dao_student.select_student_by_id(select_id)
        result2 = db.dao_student.select_student_by_id_limit1(select_id)
        assert isinstance(result1, list)
        assert asdict(result1[0]) == asdict(result2)


def test_fetchone_no_record(init_db: Database):
    """查询不存在的单记录"""
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        db.dao_student.delete_student_by_id(student_id=select_id)
        result1 = db.dao_student.select_student_by_id(select_id)
        result2 = db.dao_student.select_student_by_id_limit1(select_id)
        assert not result1
        assert result2 is None


def test_sql_fetch_one(init_db: Database):
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result1 = db.dao_student.select_student_by_id(select_id)
        result2 = db.dao_student.select_student_by_id_use_fetch_one(select_id)
        assert type(result1) == list
        assert type(result2) == Student
        assert result1[0] == result2


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
