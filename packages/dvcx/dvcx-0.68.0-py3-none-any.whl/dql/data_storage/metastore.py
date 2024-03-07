import hashlib
import json
import logging
import posixpath
from abc import ABC, abstractmethod
from collections.abc import Iterator, Sequence
from datetime import datetime, timezone
from functools import reduce
from itertools import groupby
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
)

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Table,
    Text,
    UniqueConstraint,
    select,
)
from sqlalchemy.sql import func

from dql.dataset import DatasetDependency, DatasetRecord, DatasetVersion
from dql.dataset import Status as DatasetStatus
from dql.error import DatasetNotFoundError, StorageNotFoundError
from dql.sql.types import SQLType
from dql.storage import Status as StorageStatus
from dql.storage import Storage, StorageURI
from dql.utils import is_expired

if TYPE_CHECKING:
    import sqlalchemy as sa
    from sqlalchemy.schema import SchemaItem

    from dql.data_storage import AbstractIDGenerator, schema
    from dql.data_storage.db_engine import DatabaseEngine


logger = logging.getLogger("dql")


class AbstractMetastore(ABC):
    """
    Abstract Metastore class, to be implemented by any Database Adapters
    for a specific database system. This manages the storing, searching, and
    retrieval of indexed metadata, and has shared logic for all database
    systems currently in use.
    """

    #
    # Constants, Initialization, and Tables
    #

    PARTIALS_TABLE_NAME_PREFIX = "prt_"
    STORAGE_TABLE = "buckets"
    DATASET_TABLE = "datasets"
    DATASET_VERSION_TABLE = "datasets_versions"
    DATASET_DEPENDENCY_TABLE = "datasets_dependencies"

    id_generator: "AbstractIDGenerator"
    schema: "schema.Schema"
    db: "DatabaseEngine"

    storage_class = Storage
    dataset_class = DatasetRecord
    dependency_class = DatasetDependency

    def __init__(
        self,
        id_generator: "AbstractIDGenerator",
        uri: StorageURI = StorageURI(""),
        partial_id: Optional[int] = None,
    ):
        self.id_generator = id_generator
        self.uri = uri
        self.partial_id: Optional[int] = partial_id
        self._storages: Optional[Table] = None
        self._partials: Optional[Table] = None
        self._datasets: Optional[Table] = None
        self._datasets_versions: Optional[Table] = None
        self._datasets_dependencies: Optional[Table] = None
        self.dataset_fields = [
            c.name
            for c in self.datasets_columns()
            if c.name  # type: ignore[attr-defined]
        ]
        self.dataset_version_fields = [
            c.name
            for c in self.datasets_versions_columns()
            if c.name  # type: ignore[attr-defined]
        ]

    def cleanup_for_tests(self):  # noqa: B027
        """Cleanup for tests. Override in subclasses."""

    @classmethod
    def buckets_columns(cls) -> list["SchemaItem"]:
        """Buckets (storages) table columns."""
        return [
            Column("id", Integer, primary_key=True, nullable=False),
            Column("uri", Text, nullable=False),
            Column("timestamp", DateTime(timezone=True)),
            Column("expires", DateTime(timezone=True)),
            Column("started_inserting_at", DateTime(timezone=True)),
            Column("last_inserted_at", DateTime(timezone=True)),
            Column("status", Integer, nullable=False),
            Column("error_message", Text, nullable=False, default=""),
            Column("error_stack", Text, nullable=False, default=""),
        ]

    @classmethod
    def datasets_columns(cls) -> list["SchemaItem"]:
        """Datasets table columns."""
        return [
            Column("id", Integer, primary_key=True),
            Column("name", Text, nullable=False),
            Column("description", Text),
            Column("labels", JSON, nullable=True),
            Column("shadow", Boolean, nullable=False),
            Column("status", Integer, nullable=False),
            Column("created_at", DateTime(timezone=True)),
            Column("finished_at", DateTime(timezone=True)),
            Column("error_message", Text, nullable=False, default=""),
            Column("error_stack", Text, nullable=False, default=""),
            Column("script_output", Text, nullable=False, default=""),
            Column("job_id", Text, nullable=True),
            Column("sources", Text, nullable=False, default=""),
            Column("query_script", Text, nullable=False, default=""),
            Column("custom_column_types", JSON, nullable=True),
        ]

    @classmethod
    def datasets_versions_columns(cls) -> list["SchemaItem"]:
        """Datasets versions table columns."""
        return [
            Column("id", Integer, primary_key=True),
            Column(
                "dataset_id",
                Integer,
                ForeignKey(f"{cls.DATASET_TABLE}.id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column("version", Integer, nullable=False),
            # adding default for now until we fully remove shadow datasets
            Column("status", Integer, nullable=False, default=DatasetStatus.COMPLETE),
            Column("created_at", DateTime(timezone=True)),
            Column("finished_at", DateTime(timezone=True)),
            Column("error_message", Text, nullable=False, default=""),
            Column("error_stack", Text, nullable=False, default=""),
            Column("script_output", Text, nullable=False, default=""),
            Column("job_id", Text, nullable=True),
            Column("sources", Text, nullable=False, default=""),
            Column("query_script", Text, nullable=False, default=""),
            Column("custom_column_types", JSON, nullable=True),
            UniqueConstraint("dataset_id", "version"),
        ]

    @classmethod
    def datasets_dependencies_columns(cls) -> list["SchemaItem"]:
        """Datasets dependencies table columns."""
        return [
            Column("id", Integer, primary_key=True),
            # TODO remove when https://github.com/iterative/dql/issues/959 is done
            Column(
                "source_dataset_id",
                Integer,
                ForeignKey(f"{cls.DATASET_TABLE}.id"),
                nullable=False,
            ),
            Column(
                "source_dataset_version_id",
                Integer,
                ForeignKey(f"{cls.DATASET_VERSION_TABLE}.id"),
                nullable=True,
            ),
            # TODO remove when https://github.com/iterative/dql/issues/959 is done
            Column(
                "dataset_id",
                Integer,
                ForeignKey(f"{cls.DATASET_TABLE}.id"),
                nullable=True,
            ),
            Column(
                "dataset_version_id",
                Integer,
                ForeignKey(f"{cls.DATASET_VERSION_TABLE}.id"),
                nullable=True,
            ),
            # TODO remove when https://github.com/iterative/dql/issues/1121 is done
            # If we unify datasets and bucket listing then both bucket fields won't
            # be needed
            Column(
                "bucket_id",
                Integer,
                ForeignKey(f"{cls.STORAGE_TABLE}.id"),
                nullable=True,
            ),
            Column("bucket_version", Text, nullable=True),
        ]

    @classmethod
    def storage_partial_columns(cls) -> list["SchemaItem"]:
        """Storage partial table columns."""
        return [
            Column("path_str", Text, nullable=False),
            # This is generated before insert and is not the SQLite rowid,
            # so it is not the primary key.
            Column("partial_id", Integer, nullable=False, index=True),
            Column("timestamp", DateTime(timezone=True)),
            Column("expires", DateTime(timezone=True)),
        ]

    def get_storage_partial_table(self, name: str) -> Table:
        table = self.db.metadata.tables.get(name)
        if table is None:
            table = Table(
                name,
                self.db.metadata,
                *self.storage_partial_columns(),
            )
        return table

    @abstractmethod
    def clone(
        self, uri: StorageURI = StorageURI(""), partial_id: Optional[int] = None
    ) -> "AbstractMetastore":
        """Clones Metastore implementation for some Storage input"""

    @abstractmethod
    def clone_params(self) -> tuple[Callable[..., Any], list[Any], dict[str, Any]]:
        """
        Returns the class, args, and kwargs needed to instantiate a cloned copy of this
        AbstractMetastore implementation, for use in separate processes or machines.
        """

    def close(self) -> None:
        """Closes any active database connections."""
        self.db.close()

    @abstractmethod
    def init_db(self, uri: StorageURI, partial_id: int) -> None:
        """Initializes database tables for metastore"""

    #
    # Query Tables
    #

    def partials_table(self, uri: StorageURI):
        return self.get_storage_partial_table(self.partials_table_name(uri))

    @property
    def storages(self) -> Table:
        if self._storages is None:
            self._storages = Table(
                self.STORAGE_TABLE, self.db.metadata, *self.buckets_columns()
            )
        return self._storages

    @property
    def partials(self) -> Table:
        assert (
            self.current_partials_table_name
        ), "Partials can only be used if uri/current_partials_table_name is set"
        if self._partials is None:
            self._partials = self.get_storage_partial_table(
                self.current_partials_table_name
            )
        return self._partials

    @property
    def datasets(self) -> Table:
        if self._datasets is None:
            self._datasets = Table(
                self.DATASET_TABLE, self.db.metadata, *self.datasets_columns()
            )
        return self._datasets

    @property
    def datasets_versions(self) -> Table:
        if self._datasets_versions is None:
            self._datasets_versions = Table(
                self.DATASET_VERSION_TABLE,
                self.db.metadata,
                *self.datasets_versions_columns(),
            )
        return self._datasets_versions

    @property
    def datasets_dependencies(self) -> Table:
        if self._datasets_dependencies is None:
            self._datasets_dependencies = Table(
                self.DATASET_DEPENDENCY_TABLE,
                self.db.metadata,
                *self.datasets_dependencies_columns(),
            )
        return self._datasets_dependencies

    #
    # Query Starters (These can be overridden by subclasses)
    #

    @abstractmethod
    def storages_insert(self):
        ...

    def storages_select(self, *columns):
        storages = self.storages
        if not columns:
            return storages.select()
        return select(*columns).select_from(storages)

    def storages_update(self):
        return self.storages.update()

    def storages_delete(self):
        return self.storages.delete()

    @abstractmethod
    def partials_insert(self):
        ...

    def partials_select(self, *columns):
        partials = self.partials
        if not columns:
            return partials.select()
        return select(*columns).select_from(partials)

    def partials_update(self):
        return self.partials.update()

    @abstractmethod
    def datasets_insert(self):
        ...

    def datasets_select(self, *columns):
        datasets = self.datasets
        if not columns:
            return datasets.select()
        return select(*columns).select_from(datasets)

    def datasets_update(self):
        return self.datasets.update()

    def datasets_delete(self):
        return self.datasets.delete()

    @abstractmethod
    def datasets_versions_insert(self):
        ...

    def datasets_versions_select(self, *columns):
        datasets_versions = self.datasets_versions
        if not columns:
            return datasets_versions.select()
        return select(*columns).select_from(datasets_versions)

    def datasets_versions_update(self):
        return self.datasets_versions.update()

    def datasets_versions_delete(self):
        return self.datasets_versions.delete()

    @abstractmethod
    def datasets_dependencies_insert(self):
        ...

    def datasets_dependencies_select(self, *columns):
        datasets_dependencies = self.datasets_dependencies
        if not columns:
            return datasets_dependencies.select()
        return select(*columns).select_from(datasets_dependencies)

    def datasets_dependencies_update(self):
        return self.datasets_dependencies.update()

    def datasets_dependencies_delete(self):
        return self.datasets_dependencies.delete()

    #
    # Table Name Internal Functions
    #

    def partials_table_name(self, uri: StorageURI) -> str:
        sha = hashlib.sha256(uri.encode("utf-8")).hexdigest()[:12]
        return f"{self.PARTIALS_TABLE_NAME_PREFIX}_{sha}"

    @property
    def current_partials_table_name(self) -> Optional[str]:
        if not self.uri:
            return None
        return self.partials_table_name(self.uri)

    #
    # Storages
    #

    def create_storage_if_not_registered(self, uri: StorageURI, conn=None) -> None:
        """Saves new storage if it doesn't exist in database."""
        self.db.execute(
            self.storages_insert()
            .values(
                uri=uri,
                status=StorageStatus.CREATED,
                error_message="",
                error_stack="",
            )
            .on_conflict_do_nothing(),
            conn=conn,
        )

    def register_storage_for_indexing(
        self,
        uri: StorageURI,
        force_update: bool = True,
        prefix: str = "",
    ) -> tuple[Storage, bool, bool, Optional[int]]:
        """
        Prepares storage for indexing operation.
        This method should be called before index operation is started
        It returns:
            - storage, prepared for indexing
            - boolean saying if indexing is needed
            - boolean saying if indexing is currently pending (running)
            - boolean saying if this storage is newly created
        """
        # This ensures that all calls to the DB are in a single transaction
        # and commit is automatically called once this function returns
        with self.db.transaction() as conn:
            # Create storage if it doesn't exist
            self.create_storage_if_not_registered(uri, conn=conn)
            storage = self.get_storage(uri, conn=conn)

            if storage.status == StorageStatus.PENDING:
                return storage, False, True, None

            if storage.is_expired or storage.status == StorageStatus.STALE:
                storage = self.mark_storage_pending(storage, conn=conn)
                return storage, True, False, None

            if (
                storage.status in (StorageStatus.PARTIAL, StorageStatus.COMPLETE)
                and not force_update
            ):
                partial_id = self.get_valid_partial_id(uri, prefix, raise_exc=False)
                if partial_id is not None:
                    return storage, False, False, partial_id
                return storage, True, False, None

            storage = self.mark_storage_pending(storage, conn=conn)
            return storage, True, False, None

    def find_stale_storages(self):
        """
        Finds all pending storages for which the last inserted node has happened
        before STALE_HOURS_LIMIT hours, and marks it as STALE
        """
        s = self.storages
        with self.db.transaction() as conn:
            pending_storages = map(
                self.storage_class._make,
                self.db.execute(
                    self.storages_select().where(s.c.status == StorageStatus.PENDING),
                    conn=conn,
                ),
            )
            for storage in pending_storages:
                if storage.is_stale:
                    print(f"Marking storage {storage.uri} as stale")
                    self._mark_storage_stale(storage.id, conn=conn)

    def mark_storage_indexed(
        self,
        uri: StorageURI,
        status: int,
        ttl: int,
        end_time: Optional[datetime] = None,
        prefix: str = "",
        partial_id: int = 0,
        error_message: str = "",
        error_stack: str = "",
    ) -> None:
        """
        Marks storage as indexed.
        This method should be called when index operation is finished
        """
        if status == StorageStatus.PARTIAL and not prefix:
            raise AssertionError("Partial indexing requires a prefix")

        if end_time is None:
            end_time = datetime.now(timezone.utc)
        expires = Storage.get_expiration_time(end_time, ttl)

        s = self.storages
        with self.db.transaction() as conn:
            self.db.execute(
                self.storages_update()
                .where(s.c.uri == uri)
                .values(  # type: ignore [attr-defined]
                    timestamp=end_time,
                    expires=expires,
                    status=status,
                    last_inserted_at=end_time,
                    error_message=error_message,
                    error_stack=error_stack,
                ),
                conn=conn,
            )

            if not self.current_partials_table_name:
                # This only occurs in tests
                return

            if status in (StorageStatus.PARTIAL, StorageStatus.COMPLETE):
                dir_prefix = posixpath.join(prefix, "")
                self.db.execute(
                    self.partials_insert().values(
                        path_str=dir_prefix,
                        timestamp=end_time,
                        expires=expires,
                        partial_id=partial_id,
                    ),
                    conn=conn,
                )

    @abstractmethod
    def mark_storage_not_indexed(self, uri: StorageURI) -> None:
        """
        Mark storage as not indexed.
        This method should be called when storage index is deleted.
        """

    def update_last_inserted_at(self, uri: Optional[StorageURI] = None) -> None:
        """Updates last inserted datetime in bucket with current time"""
        uri = uri or self.uri
        updates = {"last_inserted_at": datetime.now(timezone.utc)}
        s = self.storages
        self.db.execute(
            self.storages_update().where(s.c.uri == uri).values(**updates)  # type: ignore [attr-defined]
        )

    def get_all_storage_uris(self) -> Iterator[StorageURI]:
        s = self.storages
        yield from (r[0] for r in self.db.execute(self.storages_select(s.c.uri)))

    def get_storage(self, uri: StorageURI, conn=None) -> Storage:
        """
        Gets storage representation from database.
        E.g. if s3 is used as storage this would be s3 bucket data
        """
        s = self.storages
        result = next(
            self.db.execute(self.storages_select().where(s.c.uri == uri), conn=conn),
            None,
        )
        if not result:
            raise StorageNotFoundError(f"Storage {uri} not found.")

        return self.storage_class._make(result)

    def list_storages(self) -> list[Storage]:
        result = self.db.execute(self.storages_select())
        if not result:
            return []

        return [self.storage_class._make(r) for r in result]

    def mark_storage_pending(self, storage: Storage, conn=None) -> Storage:
        # Update status to pending and dates
        updates = {
            "status": StorageStatus.PENDING,
            "timestamp": None,
            "expires": None,
            "last_inserted_at": None,
            "started_inserting_at": datetime.now(timezone.utc),
        }
        storage = storage._replace(**updates)  # type: ignore [arg-type]
        s = self.storages
        self.db.execute(
            self.storages_update().where(s.c.uri == storage.uri).values(**updates),  # type: ignore [attr-defined]
            conn=conn,
        )
        return storage

    def _mark_storage_stale(self, storage_id: int, conn=None) -> None:
        # Update status to pending and dates
        updates = {"status": StorageStatus.STALE, "timestamp": None, "expires": None}
        s = self.storages
        self.db.execute(
            self.storages.update().where(s.c.id == storage_id).values(**updates),  # type: ignore [attr-defined]
            conn=conn,
        )

    #
    # Partial Indexes
    #

    def init_partial_id(self, uri: StorageURI):
        if not uri:
            raise ValueError("uri for get_next_partial_id() cannot be empty")
        self.id_generator.init_id(f"partials:{uri}")

    def get_next_partial_id(self, uri: StorageURI) -> int:
        if not uri:
            raise ValueError("uri for get_next_partial_id() cannot be empty")
        return self.id_generator.get_next_id(f"partials:{uri}")

    def get_valid_partial_id(
        self, uri: StorageURI, prefix: str, raise_exc: bool = True
    ) -> Optional[int]:
        # This SQL statement finds all entries that are
        # prefixes of the given prefix, matching this or parent directories
        # that are indexed.
        dir_prefix = posixpath.join(prefix, "")
        p = self.partials_table(uri)
        expire_values = self.db.execute(
            select(p.c.expires, p.c.partial_id)
            .select_from(p)
            .where(
                p.c.path_str == func.substr(dir_prefix, 1, func.length(p.c.path_str))
            )
            .order_by(p.c.expires.desc())
        )
        for expires, partial_id in expire_values:
            if not is_expired(expires):
                return partial_id
        if raise_exc:
            raise RuntimeError(f"Unable to get valid partial_id: {uri=}, {prefix=}")
        return None

    def get_last_partial_id(self, uri: StorageURI) -> Optional[int]:
        p = self.partials_table(uri)
        if not self.db.has_table(p.name):
            raise StorageNotFoundError(f"Storage {uri} partials are not found.")
        last_partial = self.db.execute(
            select(p.c.partial_id)
            .select_from(p)
            .order_by(p.c.timestamp.desc())
            .limit(1)
        )
        for (partial_id,) in last_partial:
            return partial_id
        return None

    #
    # Datasets
    #

    def create_dataset(
        self,
        name: str,
        shadow: bool = True,
        status: int = DatasetStatus.CREATED,
        sources: Optional[list[str]] = None,
        query_script: str = "",
        custom_columns: Sequence["sa.Column"] = (),
        ignore_if_exists: bool = False,
        **kwargs,  # TODO registered = True / False
    ) -> "DatasetRecord":
        """Creates new dataset."""
        custom_column_types = json.dumps(
            {
                c.name: c.type.to_dict()
                for c in self.schema.dataset_row_cls.default_columns()
                + list(custom_columns)
                if isinstance(c.type, SQLType)
            }
        )

        # TODO abstract this method and add registered = True based on kwargs
        query = self.datasets_insert().values(
            name=name,
            shadow=shadow,
            status=status,
            created_at=datetime.now(timezone.utc),
            error_message="",
            error_stack="",
            script_output="",
            sources="\n".join(sources) if sources else "",
            query_script=query_script,
            custom_column_types=custom_column_types,
        )
        if ignore_if_exists:
            query = query.on_conflict_do_nothing(index_elements=["name"])
        self.db.execute(query)

        dataset = self.get_dataset(name)
        assert dataset.shadow == shadow

        return dataset

    def create_dataset_version(
        self,
        dataset: DatasetRecord,
        version: int,
        status: int = DatasetStatus.CREATED,
        sources: str = "",
        query_script: str = "",
        error_message: str = "",
        error_stack: str = "",
        script_output: str = "",
        created_at: Optional[datetime] = None,
        finished_at: Optional[datetime] = None,
        custom_column_types: Optional[dict[str, Any]] = None,
        ignore_if_exists: bool = False,
        conn=None,
    ) -> "DatasetRecord":
        """Creates new dataset version."""
        if status in [DatasetStatus.COMPLETE, DatasetStatus.FAILED]:
            finished_at = finished_at or datetime.now(timezone.utc)
        else:
            finished_at = None

        query = self.datasets_versions_insert().values(
            dataset_id=dataset.id,
            version=version,
            status=status,  # for now until we remove shadow datasets
            created_at=created_at or datetime.now(timezone.utc),
            finished_at=finished_at,
            error_message=error_message,
            error_stack=error_stack,
            script_output=script_output,
            sources=sources,
            query_script=query_script,
            custom_column_types=json.dumps(custom_column_types or {}),
        )
        if ignore_if_exists:
            query = query.on_conflict_do_nothing(
                index_elements=["dataset_id", "version"]
            )
        self.db.execute(query, conn=conn)

        return self.get_dataset(dataset.name, conn=conn)

    def remove_dataset(self, dataset: "DatasetRecord") -> None:
        """Removes dataset."""
        d = self.datasets
        with self.db.transaction():
            self.remove_dataset_dependencies(dataset)
            self.remove_dataset_dependants(dataset)
            self.db.execute(self.datasets_delete().where(d.c.id == dataset.id))

    def update_dataset(
        self, dataset: DatasetRecord, conn=None, **kwargs
    ) -> DatasetRecord:
        """Updates dataset fields."""
        values = {}
        dataset_values = {}
        for field, value in kwargs.items():
            if field in self.dataset_fields[1:]:
                if field in ["labels", "custom_column_types"]:
                    values[field] = json.dumps(value) if value else None
                else:
                    values[field] = value
                if field == "custom_column_types":
                    dataset_values[field] = DatasetRecord.parse_custom_column_types(
                        value
                    )
                else:
                    dataset_values[field] = value

        if not values:
            # Nothing to update
            return dataset

        d = self.datasets
        self.db.execute(
            self.datasets_update().where(d.c.name == dataset.name).values(values),
            conn=conn,
        )  # type: ignore [attr-defined]

        dataset.update(**dataset_values)
        return dataset

    def update_dataset_version(
        self, dataset_version: DatasetVersion, conn=None, **kwargs
    ) -> DatasetVersion:
        """Updates dataset fields."""
        values = {}
        for field, value in kwargs.items():
            if field in self.dataset_version_fields[1:]:
                if field == "custom_column_types":
                    dataset_version.update(
                        **{field: DatasetRecord.parse_custom_column_types(value)}
                    )
                    values[field] = json.dumps(value) if value else None
                else:
                    values[field] = value
                    dataset_version.update(**{field: value})

        if not values:
            # Nothing to update
            return dataset_version

        dv = self.datasets_versions
        self.db.execute(
            self.datasets_versions_update()
            .where(dv.c.id == dataset_version.id)
            .values(values),
            conn=conn,
        )  # type: ignore [attr-defined]

        return dataset_version

    def _parse_dataset(self, rows) -> Optional[DatasetRecord]:
        versions = []
        for r in rows:
            versions.append(self.dataset_class.parse(*r))
        if not versions:
            return None
        return reduce(lambda ds, version: ds.merge_versions(version), versions)

    def remove_dataset_version(
        self, dataset: DatasetRecord, version: int
    ) -> DatasetRecord:
        """
        Deletes one single dataset version.
        If it was last version, it removes dataset completely
        """
        if not dataset.has_version(version):
            raise DatasetNotFoundError(
                f"Dataset {dataset.name} version {version} not found."
            )

        self.remove_dataset_dependencies(dataset, version)
        self.remove_dataset_dependants(dataset, version)

        d = self.datasets
        dv = self.datasets_versions
        self.db.execute(
            self.datasets_versions_delete().where(
                (dv.c.dataset_id == dataset.id) & (dv.c.version == version)
            )
        )

        if dataset.versions and len(dataset.versions) == 1:
            # had only one version, fully deleting dataset
            self.db.execute(self.datasets_delete().where(d.c.id == dataset.id))

        dataset.remove_version(version)

        return dataset

    def list_datasets(
        self, shadow_only: Optional[bool] = None
    ) -> Iterator["DatasetRecord"]:
        """Lists all datasets (or shadow datasets only)"""
        d = self.datasets
        dv = self.datasets_versions
        query = self.datasets_select(
            *(getattr(d.c, f) for f in self.dataset_fields),
            *(getattr(dv.c, f) for f in self.dataset_version_fields),
        )
        j = d.join(dv, d.c.id == dv.c.dataset_id, isouter=True)

        if shadow_only is not None:
            query = query.where(  # type: ignore [attr-defined]
                d.c.shadow == bool(shadow_only)
            ).order_by("dataset_id")

        query = query.select_from(j)
        rows = self.db.execute(query)

        for _, g in groupby(rows, lambda r: r[0]):
            dataset = self._parse_dataset(list(g))
            if dataset:
                dataset.sort_versions()
                yield dataset

    def get_dataset(self, name: str, conn=None) -> DatasetRecord:
        """Gets a single dataset by name"""
        d = self.datasets
        dv = self.datasets_versions
        query = self.datasets_select(
            *(getattr(d.c, f) for f in self.dataset_fields),
            *(getattr(dv.c, f) for f in self.dataset_version_fields),
        ).where(d.c.name == name)  # type: ignore [attr-defined]
        j = d.join(dv, d.c.id == dv.c.dataset_id, isouter=True)
        query = query.select_from(j)
        ds = self._parse_dataset(self.db.execute(query, conn=conn))
        if not ds:
            raise DatasetNotFoundError(f"Dataset {name} not found.")
        return ds

    def update_dataset_status(
        self,
        dataset: DatasetRecord,
        status: int,
        version: Optional[int] = None,
        conn=None,
        error_message="",
        error_stack="",
        script_output="",
    ) -> DatasetRecord:
        """
        Updates dataset status and appropriate fields related to status
        It also updates version if specified.
        """
        update_data: dict[str, Any] = {"status": status}
        if status in [DatasetStatus.COMPLETE, DatasetStatus.FAILED]:
            # if in final state, updating finished_at datetime
            update_data["finished_at"] = datetime.now(timezone.utc)
            if script_output:
                update_data["script_output"] = script_output

        if status == DatasetStatus.FAILED:
            update_data["error_message"] = error_message
            update_data["error_stack"] = error_stack

        self.update_dataset(dataset, conn=conn, **update_data)

        if version:
            dataset_version = dataset.get_version(version)
            self.update_dataset_version(dataset_version, conn=conn, **update_data)

        return dataset

    #
    # Dataset dependencies
    #

    def insert_dataset_dependency(self, data: dict[str, Any]) -> None:
        """Method for inserting dependencies"""
        self.db.execute(self.datasets_dependencies_insert().values(**data))

    def add_dependency(
        self,
        dependency: DatasetDependency,
        source_dataset_name: str,
        source_dataset_version: Optional[int] = None,
    ) -> None:
        if dependency.is_dataset:
            self.add_dataset_dependency(
                source_dataset_name,
                dependency.name,
                source_dataset_version,
                int(dependency.version) if dependency.version else None,
            )
        else:
            self.add_storage_dependency(
                source_dataset_name,
                StorageURI(dependency.name),
                dependency.version,
                source_dataset_version,
            )

    def add_storage_dependency(
        self,
        source_dataset_name: str,
        storage_uri: StorageURI,
        storage_timestamp_str: Optional[str] = None,
        source_dataset_version: Optional[int] = None,
    ) -> None:
        source_dataset = self.get_dataset(source_dataset_name)
        storage = self.get_storage(storage_uri)

        self.insert_dataset_dependency(
            {
                "source_dataset_id": source_dataset.id,
                "source_dataset_version_id": (
                    source_dataset.get_version(source_dataset_version).id
                    if source_dataset_version
                    else None
                ),
                "bucket_id": storage.id,
                "bucket_version": storage_timestamp_str,
            }
        )

    def add_dataset_dependency(
        self,
        source_dataset_name: str,
        dataset_name: str,
        source_dataset_version: Optional[int] = None,
        dataset_version: Optional[int] = None,
    ):
        source_dataset = self.get_dataset(source_dataset_name)
        dataset = self.get_dataset(dataset_name)

        self.insert_dataset_dependency(
            {
                "source_dataset_id": source_dataset.id,
                "source_dataset_version_id": (
                    source_dataset.get_version(source_dataset_version).id
                    if source_dataset_version
                    else None
                ),
                "dataset_id": dataset.id,
                "dataset_version_id": (
                    dataset.get_version(dataset_version).id if dataset_version else None
                ),
            }
        )

    def update_dataset_dependency_source(
        self,
        source_dataset: DatasetRecord,
        source_dataset_version: Optional[int] = None,
        new_source_dataset: Optional[DatasetRecord] = None,
        new_source_dataset_version: Optional[int] = None,
    ):
        dd = self.datasets_dependencies

        if not new_source_dataset:
            new_source_dataset = source_dataset

        q = self.datasets_dependencies_update().where(
            dd.c.source_dataset_id == source_dataset.id
        )
        if source_dataset_version:
            q = q.where(
                dd.c.source_dataset_version_id
                == source_dataset.get_version(source_dataset_version).id
            )

        data = {"source_dataset_id": new_source_dataset.id}
        if new_source_dataset_version:
            data["source_dataset_version_id"] = new_source_dataset.get_version(
                new_source_dataset_version
            ).id

        q = q.values(**data)
        self.db.execute(q)

    @abstractmethod
    def dataset_dependencies_select_columns(self) -> list["SchemaItem"]:
        """
        Returns a list of columns to select in a query for fetching dataset dependencies
        """

    def get_direct_dataset_dependencies(
        self, dataset: DatasetRecord, version: Optional[int] = None
    ) -> list[Optional[DatasetDependency]]:
        d = self.datasets
        dd = self.datasets_dependencies
        dv = self.datasets_versions
        s = self.storages

        select_cols = self.dataset_dependencies_select_columns()

        query = (
            self.datasets_dependencies_select(*select_cols)
            .where(dd.c.source_dataset_id == dataset.id)
            .select_from(
                dd.join(d, dd.c.dataset_id == d.c.id, isouter=True)
                .join(s, dd.c.bucket_id == s.c.id, isouter=True)
                .join(dv, dd.c.dataset_version_id == dv.c.id, isouter=True)
            )
        )
        if version:
            dataset_version = dataset.get_version(version)
            query = query.where(dd.c.source_dataset_version_id == dataset_version.id)

        return [self.dependency_class.parse(*r) for r in self.db.execute(query)]

    def remove_dataset_dependencies(
        self, dataset: DatasetRecord, version: Optional[int] = None
    ):
        """
        When we remove dataset, we need to clean up it's dependencies as well
        """
        dd = self.datasets_dependencies

        q = self.datasets_dependencies_delete().where(
            dd.c.source_dataset_id == dataset.id
        )

        if version:
            q = q.where(
                dd.c.source_dataset_version_id == dataset.get_version(version).id
            )

        self.db.execute(q)

    def remove_dataset_dependants(
        self, dataset: DatasetRecord, version: Optional[int] = None
    ):
        """
        When we remove dataset, we need to clear it's references in other dataset
        dependencies
        """
        dd = self.datasets_dependencies

        q = self.datasets_dependencies_update().where(dd.c.dataset_id == dataset.id)
        if version:
            q = q.where(dd.c.dataset_version_id == dataset.get_version(version).id)

        q = q.values(dataset_id=None, dataset_version_id=None)

        self.db.execute(q)
