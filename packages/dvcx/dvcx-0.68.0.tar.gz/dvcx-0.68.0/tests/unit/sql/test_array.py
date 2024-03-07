from typing import TYPE_CHECKING

from dql.sql import literal, select
from dql.sql.functions import array, string

if TYPE_CHECKING:
    from dql.data_storage import AbstractWarehouse


def test_length(warehouse: "AbstractWarehouse"):
    query = select(
        array.length(["abc", "def", "g", "hi"]),
        array.length([3.0, 5.0, 1.0, 6.0, 1.0]),
        array.length([[1, 2, 3], [4, 5, 6]]),
    )
    result = tuple(warehouse.db.execute(query))
    assert result == ((4, 5, 2),)


def test_length_on_split(warehouse: "AbstractWarehouse"):
    query = select(
        array.length(string.split(literal("abc/def/g/hi"), literal("/"))),
    )
    result = tuple(warehouse.db.execute(query))
    assert result == ((4,),)
