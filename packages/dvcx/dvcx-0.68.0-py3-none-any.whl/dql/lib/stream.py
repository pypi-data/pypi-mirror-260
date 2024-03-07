from datetime import datetime
from pathlib import Path
from random import getrandbits
from typing import Optional

from pydantic import Field

from dql.cache import UniqueId
from dql.lib.feature import StreamFeature


class FileStream(StreamFeature):
    source: str = Field(default="")
    parent: str = Field(default="")
    name: str
    version: str = Field(default="")
    etag: str = Field(default="")
    size: int = Field(default=0)
    vtype: str = Field(default="")
    location: Optional[list[dict]] = Field(default=None)

    _unique_id_keys = ["source", "parent", "name", "etag", "size", "vtype", "location"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._stream = None
        self._cache = None

    def open(self):
        return self._stream

    def set_cache(self, cache):
        self._cache = cache

    def get_uid(self):
        dump = self.model_dump()
        return UniqueId(*(dump[k] for k in self._unique_id_keys))

    def get_local_path(self) -> Optional[str]:
        """Get path to a file in a local cache.
        Return None if file is not cached. Throws an exception if cache is not setup."""
        if self._cache is None:
            raise RuntimeError(
                "cannot resolve local file path because cache is not setup"
            )
        return self._cache.get_path(self.get_uid())

    def get_file_suffix(self):
        return Path(self.name).suffix

    def get_file_ext(self):
        return Path(self.name).suffix.strip(".")

    def get_file_stem(self):
        return Path(self.name).stem


class FileInfo(StreamFeature):
    source: str = Field(default="")
    parent: str = Field(default="")
    name: str
    size: int = Field(default=0)
    location: Optional[dict] = Field(default=None)
    vtype: str = Field(default="")
    dir_type: int = Field(default=0)
    owner_name: str = Field(default="")
    owner_id: str = Field(default="")
    is_latest: bool = Field(default=True)
    last_modified: datetime = Field(default=datetime.min)
    version: str = Field(default="")
    etag: str = Field(default="")
    checksum: str = Field(default="")
    anno: Optional[dict] = Field(default=None)
    random: int = Field(default_factory=lambda: getrandbits(63))
