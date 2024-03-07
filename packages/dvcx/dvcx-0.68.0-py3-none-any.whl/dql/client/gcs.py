from base64 import b64decode
from datetime import datetime
from typing import Any

from dateutil.parser import isoparse
from gcsfs import GCSFileSystem

from dql.node import Entry

from .fsspec import DELIMITER, Client

# Patch gcsfs for consistency with s3fs
GCSFileSystem.set_session = GCSFileSystem._set_session


class GCSClient(Client):
    FS_CLASS = GCSFileSystem
    PREFIX = "gcs://"
    protocol = "gcs"

    @staticmethod
    def parse_timestamp(timestamp: str) -> datetime:
        """
        Parse timestamp string returned by GCSFileSystem.

        This ensures that the passed timestamp is timezone aware.
        """
        dt = isoparse(timestamp)
        assert dt.tzinfo is not None
        return dt

    def convert_info(self, v: dict[str, Any], parent: str) -> Entry:
        name = v.get("name", "").split(DELIMITER)[-1]
        if "generation" in v:
            gen = f"#{v['generation']}"
            if name.endswith(gen):
                name = name[: -len(gen)]
        return Entry.from_file(
            parent=parent,
            name=name,
            checksum=b64decode(v.get("md5Hash", "")).hex(),
            etag=v.get("etag", ""),
            version=v.get("generation", ""),
            is_latest=not v.get("timeDeleted"),
            last_modified=self.parse_timestamp(v["updated"]),
            size=v.get("size", ""),
        )
