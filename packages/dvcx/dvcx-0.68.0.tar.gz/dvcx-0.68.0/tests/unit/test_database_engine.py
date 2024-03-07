from sqlalchemy import Column, Integer, Table


def test_table(sqlite_db):
    table = Table(
        "test_table", sqlite_db.metadata, Column("id", Integer, primary_key=True)
    )
    assert not sqlite_db.has_table("test_table")
    assert not sqlite_db.has_table("test_table_2")

    table.create(sqlite_db.engine)
    assert sqlite_db.has_table("test_table")
    assert not sqlite_db.has_table("test_table_2")

    sqlite_db.rename_table("test_table", "test_table_2")
    assert sqlite_db.has_table("test_table_2")
    assert not sqlite_db.has_table("test_table")

    sqlite_db.drop_table(Table("test_table_2", sqlite_db.metadata))
    assert not sqlite_db.has_table("test_table")
    assert not sqlite_db.has_table("test_table_2")


def test_table_in_transaction(sqlite_db):
    table = Table(
        "test_table", sqlite_db.metadata, Column("id", Integer, primary_key=True)
    )
    assert not sqlite_db.has_table("test_table")
    assert not sqlite_db.has_table("test_table_2")

    with sqlite_db.transaction():
        table.create(sqlite_db.engine)
        assert sqlite_db.has_table("test_table")
        assert not sqlite_db.has_table("test_table_2")

        sqlite_db.rename_table("test_table", "test_table_2")
        assert sqlite_db.has_table("test_table_2")
        assert not sqlite_db.has_table("test_table")

        sqlite_db.drop_table(Table("test_table_2", sqlite_db.metadata))
        assert not sqlite_db.has_table("test_table")
        assert not sqlite_db.has_table("test_table_2")
