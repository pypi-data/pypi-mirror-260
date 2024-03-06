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

    @Sql("select * from student;")
    def select_all(self):
        pass

    @Sql("select * from student where student_id=?;", fetch_type=Student)
    def select_student_by_id(self, student_id):
        pass

    @Sql("update student set name=? where student_id=?;")
    def update_name_by_id(self, name, student_id):
        pass

    @Sql("delete from student where student_id=?;")
    def delete_student_by_id(self, student_id):
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
def test_dao_create_table(init_db: Database):
    """创建表"""
    db = init_db
    db.dao_student.create_table()
    db.commit()


def test_insert(init_db):
    """插入数据"""
    db = init_db
    students = generate_students(0, 100)
    for student in students:
        record_id = db.dao_student.insert(entity=student)
        db.commit()

        result = db.dao_student.select_student_by_id(record_id)
        result = result[0]
        assert asdict(result) == asdict(students[result.student_id])


def test_select_all(init_db):
    """查询全部"""
    db = init_db
    students = insert_data(db)
    results = db.dao_student.select_all()
    for result in results:
        assert asdict(result) == asdict(students[result.student_id])


def test_select_student_by_id(init_db):
    """具体查询"""
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        result = db.dao_student.select_student_by_id(student_id=select_id)
        assert asdict(result[0]) == asdict(students[select_id])


def test_update_name(init_db):
    """更新"""
    db = init_db
    students = insert_data(db)
    for student in students:
        select_id = student.student_id
        new_name = '好家伙'
        db.dao_student.update_name_by_id(name=new_name, student_id=select_id)
        db.commit()
        result = db.dao_student.select_student_by_id(select_id)
        assert result[0].name == new_name


def test_insert_many(init_db: Database):
    """批量插入"""
    db = init_db
    start = 101
    end = 200
    students2 = generate_students(start=start, end=end)
    db.dao_student.insert(entity=students2)
    db.commit()

    for i in range(start, end):
        result = db.dao_student.select_student_by_id(i)
        result = result[0]
        assert asdict(result) == asdict(students2[i - start])


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
