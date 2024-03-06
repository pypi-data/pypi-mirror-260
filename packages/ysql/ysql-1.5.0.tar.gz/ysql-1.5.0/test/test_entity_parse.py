# -*- coding:utf-8 -*-
from dataclasses import dataclass

import pytest

from ysql.entity import _parse_attr_value, _parse_constraints, Entity, Constraint as cs, _Constraint


@Entity
@dataclass
class Student:
    attr_int: int
    attr_float: float
    attr_bool: bool
    attr_str: str

    attr_tuple: tuple
    attr_list = list
    attr_dict = dict
    attr_set = set

    attr_int_default: int = 1
    attr_float_default: float = 1.0
    attr_bool_default: bool = True
    attr_str_default: str = '1'

    attr_1cs: str = cs.not_null
    attr_2cs: str = cs.not_null, cs.unique
    attr_3cs: str = cs.not_null, cs.unique, cs.primary_key

    attr_str_and_cs: str = '1', cs.not_null, cs.datatype("varchar(200)")
    attr_int_and_cs: int = 1, cs.not_null
    attr_float_and_cs: float = 1.0, cs.not_null
    attr_bool_and_cs: bool = True, cs.not_null

    attr_str_and_2cs: str = '1', cs.not_null, cs.unique, cs.datatype("varchar(200)")
    attr_int_and_2cs: int = 1, cs.not_null, cs.unique
    attr_float_and_2cs: float = 1.0, cs.not_null, cs.unique
    attr_bool_and_2cs: bool = True, cs.not_null, cs.unique

    id: int = cs.auto_primary_key

    attr_tuple_c: tuple = cs.ignore
    attr_list_c: list = cs.ignore
    attr_dict_c: dict = cs.ignore
    attr_set_c: set = cs.ignore

    attr_tuple_c_and_v: tuple = cs.ignore, (1,)
    attr_tuple2_c_and_v: tuple = cs.ignore, 1, 2
    attr_list_c_and_v: list = cs.ignore, [1]
    attr_dict_c_and_v: dict = cs.ignore, {'1': 1}
    attr_set_c_and_v: set = cs.ignore, {1}


# ====================================================================================================================
def test_parse_1value():
    assert Student.attr_int_default == _parse_attr_value(Student.attr_int_default)
    assert Student.attr_float_default == _parse_attr_value(Student.attr_float_default)
    assert Student.attr_bool_default == _parse_attr_value(Student.attr_bool_default)
    assert Student.attr_str_default == _parse_attr_value(Student.attr_str_default)


def test_parse_1v_from_1c():
    assert Student.attr_int_default == _parse_attr_value(Student.attr_int_and_cs)
    assert Student.attr_float_default == _parse_attr_value(Student.attr_float_and_cs)
    assert Student.attr_bool_default == _parse_attr_value(Student.attr_bool_and_cs)
    assert Student.attr_str_default == _parse_attr_value(Student.attr_str_and_cs)


def test_parse_1v_from_2c():
    assert Student.attr_int_default == _parse_attr_value(Student.attr_int_and_2cs)
    assert Student.attr_float_default == _parse_attr_value(Student.attr_float_and_2cs)
    assert Student.attr_bool_default == _parse_attr_value(Student.attr_bool_and_2cs)
    assert Student.attr_str_default == _parse_attr_value(Student.attr_str_and_2cs)


def test_parse_1constraint():
    assert isinstance(Student.attr_1cs, _Constraint)
    assert _parse_constraints(Student.attr_1cs) == [cs.not_null]
    assert _parse_constraints(Student.id) == [cs.auto_primary_key]


def test_parse_2c():
    constraints = {cs.not_null, cs.unique}
    assert set(_parse_constraints(Student.attr_2cs)) == constraints


def test_parse_3c():
    constraints = {cs.not_null, cs.unique, cs.primary_key}
    assert set(_parse_constraints(Student.attr_3cs)) == constraints


def test_parse_value_from_c_no_default():
    assert _parse_attr_value(Student.attr_1cs) is None
    assert _parse_attr_value(Student.attr_2cs) is None
    assert _parse_attr_value(Student.attr_3cs) is None


def test_parse_1c_from_1v():
    assert _parse_constraints(Student.attr_str_and_cs) == [cs.not_null, cs.datatype("varchar(200)")]
    assert _parse_constraints(Student.attr_int_and_cs) == [cs.not_null]
    assert _parse_constraints(Student.attr_bool_and_cs) == [cs.not_null]
    assert _parse_constraints(Student.attr_float_and_cs) == [cs.not_null]


def test_parse_2c_from_1v():
    constraints = {cs.not_null, cs.unique}
    assert set(_parse_constraints(Student.attr_str_and_2cs)) == {cs.not_null, cs.unique, cs.datatype("varchar(200)")}
    assert set(_parse_constraints(Student.attr_int_and_2cs)) == constraints
    assert set(_parse_constraints(Student.attr_bool_and_2cs)) == constraints
    assert set(_parse_constraints(Student.attr_float_and_2cs)) == constraints


def test_parse_ignore_constraint():
    assert _parse_constraints(Student.attr_tuple_c) == [cs.ignore]
    assert _parse_constraints(Student.attr_list_c) == [cs.ignore]
    assert _parse_constraints(Student.attr_dict_c) == [cs.ignore]
    assert _parse_constraints(Student.attr_set_c) == [cs.ignore]


def test_parse_ignore_value():
    assert _parse_attr_value(Student.attr_tuple_c_and_v) == (1,)
    assert _parse_attr_value(Student.attr_tuple2_c_and_v) == (1, 2)
    assert _parse_attr_value(Student.attr_list_c_and_v) == [1]
    assert _parse_attr_value(Student.attr_dict_c_and_v) == {'1': 1}
    assert _parse_attr_value(Student.attr_set_c_and_v) == {1}


def test_parse_ignore_value_no_default():
    assert _parse_attr_value(Student.attr_tuple_c) is None
    assert _parse_attr_value(Student.attr_list_c) is None
    assert _parse_attr_value(Student.attr_dict_c) is None
    assert _parse_attr_value(Student.attr_set_c) is None


if __name__ == '__main__':
    pytest.main(["-vv", "--capture=no", __file__])
