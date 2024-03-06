# -*- coding:utf-8 -*-
from dataclasses import dataclass, asdict

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


@Dao(entity=Student, fetch_type=Student)
class DaoStudent(DaoFunc):
    @Sql("select * from student where student_id=?;", fetch_type=Student)
    def select_student_by_id(self, student_id):
        pass

    @Sql("select * from __;")
    def select_all_with_substitute(self):
        pass

    @Sql("update __ set name=? where student_id=?;")
    def update_name_by_id_with_substitute(self, name, student_id):
        pass

    @Sql("SELECT * FROM __ WHERE student_id = (SELECT MAX(student_id) FROM __);")
    def select_last_student_with_substitute(self):
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
def test_select_all_with_substitute(init_db):
    """使用表名替代符"""
    db = init_db
    students = insert_data(db)
    results = db.dao_student.select_all_with_substitute()
    for result in results:
        assert asdict(result) == asdict(students[result.student_id])


def test_update_name_with_substitute(init_db):
    """使用表名替代符更新"""
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        new_name = '好家伙'
        db.dao_student.update_name_by_id_with_substitute(name=new_name, student_id=select_id)
        db.commit()
        result = db.dao_student.select_student_by_id(select_id)
        assert result[0].name == new_name


def test_multiple_table_substitute(init_db: Database):
    """复杂sql中同时使用多个表名替代符"""
    db = init_db
    students = insert_data(db)
    result = db.dao_student.select_last_student_with_substitute()
    assert result
    assert result[0].student_id == students[-1].student_id


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
