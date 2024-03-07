from datetime import datetime
from decimal import Decimal
from typing import Optional

import pytest
from pydantic import Field, ValidationError

from dql.lib.feature import Feature, ShallowFeature
from dql.sql.types import JSON, Array, Binary, Boolean, DateTime, Int, String


class FileBasic(ShallowFeature):
    parent: str = Field(default="")
    name: str
    size: int = Field(default=0)


class FileInfo(FileBasic):
    location: dict = Field(default={})


class FileInfoEx(ShallowFeature):
    f_info: FileInfo
    type_id: int


def test_flatten_schema():
    schema = FileInfo.to_udf_spec()

    assert 4 == len(schema)
    assert [item[0] for item in schema] == ["parent", "name", "size", "location"]
    assert [item[1] for item in schema] == [String, String, Int, JSON]


def test_type_datatype():
    class Test1(Feature):
        d: datetime

    schema = Test1.to_udf_spec()
    assert schema[0][1] == DateTime


def test_type_optional_int():
    class Test1(Feature):
        d: Optional[int] = 23

    schema = Test1.to_udf_spec()
    assert schema[0][1] == Int


def test_type_bytes():
    class Test1(Feature):
        d: bytes

    schema = Test1.to_udf_spec()
    assert schema[0][1] == Binary


def test_type_array():
    class Test1(Feature):
        d: list

    schema = Test1.to_udf_spec()
    assert schema[0][1] == Array


def test_type_array_of_int():
    class Test1(Feature):
        d: list[int]

    schema = Test1.to_udf_spec()
    assert schema[0][1] == Array


def test_type_json():
    class Test1(Feature):
        d: dict

    schema = Test1.to_udf_spec()
    assert schema[0][1] == JSON


def test_type_bool():
    class Test1(Feature):
        d: bool

    schema = Test1.to_udf_spec()
    assert schema[0][1] == Boolean


def test_type_typed_json():
    class Test1(Feature):
        d: Optional[dict[str, int]]

    schema = Test1.to_udf_spec()
    assert schema[0][1] == JSON


def test_unknown_type():
    class Test1(Feature):
        d: Optional[Decimal]

    with pytest.raises(RuntimeError):
        Test1.to_udf_spec()


def test_flatten_nested_schema():
    schema = FileInfoEx.to_udf_spec()

    assert 5 == len(schema)
    assert [item[0] for item in schema] == [
        "parent",
        "name",
        "size",
        "location",
        "type_id",
    ]
    assert [item[1] for item in schema] == [String, String, Int, JSON, Int]


def test_flatten_schema_list():
    t1 = FileInfo(name="test1")
    t2 = FileInfo(name="t2", parent="pp1")
    res = Feature.features_to_udf_spec([t1, t2])
    assert len(t1.model_dump()) == len(res)


def test_flatten_basic():
    vals = FileBasic(parent="hello", name="world", size=123).flatten()
    assert vals == ("hello", "world", 123)


def test_flatten_with_json():
    t1 = FileInfo(parent="prt4", name="test1", size=42, location={"ee": "rr"})
    assert t1.flatten() == ("prt4", "test1", 42, {"ee": "rr"})


def test_flatten_with_empty_json():
    with pytest.raises(ValidationError):
        FileInfo(parent="prt4", name="test1", size=42, location=None)


def test_flatten_with_accepted_empty_json():
    class Test1(Feature):
        d: Optional[dict]

    assert Test1(d=None).flatten() == (None,)


def test_flatten_nested():
    t0 = FileInfo(parent="sfo", name="sf", size=567, location={"42": 999})
    t1 = FileInfoEx(f_info=t0, type_id=1849)

    assert t1.flatten() == ("sfo", "sf", 567, {"42": 999}, 1849)


def test_flatten_list():
    t1 = FileInfo(parent="p1", name="n4", size=3, location={"a": "b"})
    t2 = FileInfo(parent="p2", name="n5", size=2, location={"c": "d"})

    vals = t1.flatten_list([t1, t2])
    assert vals == ("p1", "n4", 3, {"a": "b"}, "p2", "n5", 2, {"c": "d"})


class MyNestedClass(Feature):
    type: int
    Name: str = Field(default="test1")


class MyTest(Feature):
    ThisIsName: str
    subClass: MyNestedClass  # noqa: N815


def test_naming_transform():
    assert [name for name, _ in MyTest.to_udf_spec()] == [
        "my_test__this_is_name",
        "my_test__sub_class__type",
        "my_test__sub_class__name",
    ]


def test_capital_letter_naming():
    class CAPLetterTEST(Feature):
        AAA_id: str

    vals = [name for name, _ in CAPLetterTEST.to_udf_spec()]
    assert vals == ["cap_letter_test__aaa_id"]


def test_delimiter_in_name():
    class MyClass(Feature):
        var__name: str

    with pytest.raises(RuntimeError):
        MyClass.to_udf_spec()

    with pytest.raises(RuntimeError):
        obj = MyClass(var__name="some stuff")
        dump = obj.model_dump()
        obj.unflatten(dump)


def test_delimiter_in_name_is_allowed_for_shallow_class():
    class MyClass(ShallowFeature):
        var__name: str

    MyClass.to_udf_spec()

    obj = MyClass(var__name="some stuff")
    dump = obj.model_dump()
    obj.unflatten(dump)


def test_custom_delimiter_in_name():
    class MyClass(Feature):
        delimiter = "EE"
        is_ieee_member: bool

    with pytest.raises(RuntimeError):
        MyClass.to_udf_spec()

    with pytest.raises(RuntimeError):
        obj = MyClass(is_ieee_member=True)
        obj.unflatten(obj.model_dump())


def test_naming_delimiter():
    class MyNestedClassNew(MyNestedClass):
        delimiter = "+++"

    class MyTestNew(MyTest):
        delimiter = "+++"

        ThisIsName: str
        subClass: MyNestedClassNew  # noqa: N815

    schema = MyTestNew.to_udf_spec()

    assert [name for name, _ in schema] == [
        "my_test_new+++this_is_name",
        "my_test_new+++sub_class+++type",
        "my_test_new+++sub_class+++name",
    ]


def test_deserialize_nested():
    class Child(Feature):
        type: int
        name: str = Field(default="test1")

    class Parent(Feature):
        name: str
        child: Child

    in_db_map = {
        "parent__name": "a1",
        "parent__child__type": 42,
        "parent__child__name": "a2",
    }

    p = Parent.unflatten(in_db_map)

    assert p.name == "a1"
    assert p.child.type == 42
    assert p.child.name == "a2"


def test_deserialize_shallow():
    class Child(ShallowFeature):
        type: int
        child_name: str = Field(default="test1")

    class Parent(ShallowFeature):
        name: str
        child: Child

    in_db_map = {
        "child_name": "a1",
        "type": 42,
        "name": "a2",
    }

    p = Parent.unflatten(in_db_map)

    assert p.name == "a2"
    assert p.child.type == 42
    assert p.child.child_name == "a1"


def test_deserialize_nested_with_name_normalization():
    class ChildClass(Feature):
        type: int
        name: str = Field(default="test1")

    class Parent(Feature):
        name: str
        childClass11: ChildClass  # noqa: N815

    in_db_map = {
        "parent__name": "name1",
        "parent__child_class11__type": 12,
        "parent__child_class11__name": "n2",
    }

    p = Parent.unflatten(in_db_map)

    assert p.name == "name1"
    assert p.childClass11.type == 12
    assert p.childClass11.name == "n2"
