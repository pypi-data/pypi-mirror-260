# -*- coding:utf-8 -*-
import os
import shutil
import sqlite3
from dataclasses import dataclass
from typing import Optional

import pymysql
import pytest
from pytest import fixture

from test.test_env import MetaDatabaseTest
from ysql import Entity, Constraint as cs, Dao, DaoFunc, Insert
from ysql.dao import Conflict, Sql, DB_TYPE_SQLITE, DB_TYPE_MYSQL


@Entity(check_type=True)
@dataclass
class Student:
    name: str = cs.unique, cs.datatype("varchar(200)")
    age: int = None
    id: int = cs.auto_primary_key


@Dao(Student, fetch_type=Student)
class DaoStudent(DaoFunc):

    @Insert(conflict=Conflict.error)
    def insert_error(self):
        pass

    @Insert(conflict=Conflict.ignore)
    def insert_ignore(self):
        pass

    @Insert(conflict=Conflict.replace)
    def insert_replace(self):
        pass

    @Sql("select * from __ where name=? limit 1;")
    def get_student_by_name(self, name) -> Optional[Student]:
        pass


class Database(MetaDatabaseTest):
    dao_student = DaoStudent()


# ====================================================================================================================
@fixture(scope="function")
def init_db(request):
    db = Database()
    db_dir = "db_folder"
    # 从request对象中获取当前测试文件的路径
    test_file_name = request.module.__file__
    # 提取文件名（不含扩展名）
    file_name = os.path.splitext(os.path.basename(test_file_name))[0]
    db_path = f"{db_dir}/{file_name}.db"
    if db.db_type == "sqlite":
        if os.path.exists(db_path):
            os.remove(db_path)
        db.connect(db_path)
    elif db.db_type == "mysql":
        db.connect()
    db.create_tables()
    yield db
    db.disconnect()
    if db.db_type == "sqlite":
        if os.path.exists(db_path):
            os.remove(db_path)
            if not os.listdir(db_dir):
                # 文件夹为空，执行删除操作
                shutil.rmtree(db_dir)


students = [Student(name='张三', age=10),
            Student(name='张三', age=11),
            Student(name='李四', age=12)]


# ====================================================================================================================
def test_insert_default(init_db: Database):
    db = init_db
    if db.db_type == DB_TYPE_SQLITE:
        with pytest.raises(sqlite3.IntegrityError) as exc_info:
            for student in students:
                db.dao_student.insert(student)
        assert "UNIQUE constraint failed" in str(exc_info.value)
    elif db.db_type == DB_TYPE_MYSQL:
        with pytest.raises(pymysql.err.IntegrityError) as exc_info:
            for student in students:
                db.dao_student.insert(student)
        assert "Duplicate entry" in str(exc_info.value)
        assert "for key 'student.name'" in str(exc_info.value)
    db.rollback()


def test_insert_error(init_db: Database):
    db = init_db
    if db.db_type == DB_TYPE_SQLITE:
        with pytest.raises(sqlite3.IntegrityError) as exc_info:
            for student in students:
                db.dao_student.insert_error(student)
        assert "UNIQUE constraint failed" in str(exc_info.value)
    elif db.db_type == DB_TYPE_MYSQL:
        with pytest.raises(pymysql.err.IntegrityError) as exc_info:
            for student in students:
                db.dao_student.insert_error(student)
        assert "Duplicate entry" in str(exc_info.value)
        assert "for key 'student.name'" in str(exc_info.value)
    db.rollback()


def test_insert_ignore(init_db: Database):
    db = init_db
    for student in students:
        db.dao_student.insert_ignore(student)
    db.commit()

    select_student = students[0]
    student_conflict = db.dao_student.get_student_by_name(name=select_student.name)
    assert student_conflict.age == select_student.age


def test_insert_replace(init_db: Database):
    db = init_db
    for student in students:
        db.dao_student.insert_replace(student)
    db.commit()

    select_student = students[0]
    student_conflict = db.dao_student.get_student_by_name(name=select_student.name)
    assert student_conflict.age == students[1].age


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
