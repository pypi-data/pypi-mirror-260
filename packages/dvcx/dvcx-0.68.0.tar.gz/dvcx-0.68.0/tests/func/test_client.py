import asyncio

import pytest
from fsspec.asyn import sync

from dql.asyn import get_loop
from dql.client import Client

from ..data import ENTRIES


@pytest.fixture
def client(cloud_server):
    uri = cloud_server.src_uri
    return Client.get_implementation(uri).from_source(
        uri, cache=None, **cloud_server.client_config
    )


def normalize_entries(entries):
    return {(e.parent, e.name) for e in entries}


def match_entries(result, expected):
    assert len(result) == len(expected)
    assert normalize_entries(result) == normalize_entries(expected)


async def find(client, prefix):
    results = []
    try:
        async for entries in client.scandir(prefix):
            results.extend(entries)
    except BaseException as exc:
        print(f"find: {repr(exc)}")
        raise
    return results


def scandir(client, prefix):
    return sync(get_loop(), find, client, prefix)
    task = asyncio.run_coroutine_threadsafe(find(client, prefix), loop=get_loop())
    return task.result()


def test_scandir_error(client):
    with pytest.raises(FileNotFoundError):
        scandir(client, "bogus")


@pytest.mark.xfail
def test_scandir_not_dir(client):
    with pytest.raises(FileNotFoundError):
        scandir(client, "description")


def test_scandir_success(client):
    results = scandir(client, "")
    match_entries(results, ENTRIES)
