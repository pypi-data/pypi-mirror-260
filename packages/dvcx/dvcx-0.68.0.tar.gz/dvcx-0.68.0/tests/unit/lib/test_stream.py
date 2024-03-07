import pytest

from dql.cache import DQLCache, UniqueId
from dql.lib.stream import FileStream


def test_uid_missing_location():
    name = "my_name"
    vtype = "vt1"

    stream = FileStream(name=name, vtype=vtype)
    assert stream.get_uid() == UniqueId("", "", name, "", 0, vtype, None)


def test_uid_location():
    name = "na_me"
    vtype = "some_random"
    loc = [{"e": 42}]

    stream = FileStream(name=name, vtype=vtype, location=loc)
    assert stream.get_uid() == UniqueId("", "", name, "", 0, vtype, loc)


def test_file_stem():
    s = FileStream(name=".file.jpg.txt")
    assert s.get_file_stem() == ".file.jpg"


def test_file_ext():
    s = FileStream(name=".file.jpg.txt")
    assert s.get_file_ext() == "txt"


@pytest.fixture
def cache(tmp_path):
    return DQLCache(str(tmp_path / "cache"), str(tmp_path / "tmp"))


def test_cache_get_path(cache):
    stream = FileStream(name="test.txt1", source="s3://mybkt")
    stream.set_cache(cache)

    uid = stream.get_uid()
    data = b"some data is heRe"
    cache.store_data(uid, data)

    path = stream.get_local_path()
    assert path is not None

    with open(path, mode="rb") as f:
        assert f.read() == data


def test_cache_get_path_without_cache(cache):
    stream = FileStream(name="test.txt1", source="s3://mybkt")
    with pytest.raises(RuntimeError):
        stream.get_local_path()
