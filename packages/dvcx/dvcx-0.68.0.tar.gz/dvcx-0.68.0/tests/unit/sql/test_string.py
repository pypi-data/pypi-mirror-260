from typing import TYPE_CHECKING

import pytest

from dql.sql import literal, select
from dql.sql.functions import string

if TYPE_CHECKING:
    from dql.data_storage import AbstractWarehouse


def test_length(warehouse: "AbstractWarehouse"):
    query = select(string.length(literal("abcdefg")))
    result = tuple(warehouse.db.execute(query))
    assert result == ((7,),)


@pytest.mark.parametrize(
    "args,expected",
    [
        ([literal("abc//def/g/hi"), literal("/")], ["abc", "", "def", "g", "hi"]),
        ([literal("abc//def/g/hi"), literal("/"), 2], ["abc", "", "def/g/hi"]),
    ],
)
def test_split(warehouse: "AbstractWarehouse", args, expected):
    query = select(string.split(*args))
    result = tuple(warehouse.dataset_rows_select(query))
    assert result == ((expected,),)
