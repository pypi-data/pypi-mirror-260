# -*- coding:utf-8 -*-
import os
import shutil
from dataclasses import dataclass

import pytest

from test.test_env import MetaDatabaseTest
from ysql.dao import Dao, Sql, DaoFunc
from ysql.entity import Entity, Constraint as cs


@Entity(check_type=True)
@dataclass
class Student:
    name: str
    age: int
    id: int = cs.auto_primary_key


@Dao(entity=Student)
class DaoStudent(DaoFunc):

    @Sql("delete from student where id=?;")
    def delete_student_by_id(self, student_id):
        pass


@Entity(check_type=True)
@dataclass
class Score:
    score: float
    student_id: int = cs.primary_key, cs.foreign_key(parent_entity=Student,
                                                     parent_field='id',
                                                     delete_link=cs.cascade)


@Dao(entity=Score)
class DaoScore(DaoFunc):

    @Sql("select * from __ where student_id=?;")
    def get_score_by_student_id(self, student_id):
        pass


class Database(MetaDatabaseTest):
    dao_score = DaoScore()
    dao_student = DaoStudent()


# ====================================================================================================================
@pytest.fixture(scope="module")
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
        db.execute("PRAGMA foreign_keys = ON;")
    elif db.db_type == "mysql":
        db.connect()
    db.dao_student.create_table()
    db.dao_score.create_table()
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
def test_insert_data(init_db: Database):
    db = init_db
    db.dao_student.insert(students)


def test_foreign_key_delete_cascade(init_db: Database):
    """外键"""
    db = init_db
    select_id = 1
    score = Score(150.0, student_id=select_id)
    db.dao_score.insert(score)
    db.dao_student.delete_student_by_id(student_id=select_id)
    db.commit()
    result = db.dao_score.get_score_by_student_id(select_id)
    assert len(result) == 0


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
