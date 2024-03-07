import os
from importlib import import_module
from typing import TYPE_CHECKING, Any, Optional

from dql.catalog import Catalog
from dql.data_storage.sqlite import SQLiteIDGenerator, SQLiteMetastore, SQLiteWarehouse
from dql.utils import get_envs_by_prefix

if TYPE_CHECKING:
    from dql.data_storage import AbstractIDGenerator


ID_GENERATOR_IMPORT_PATH = "DVCX_ID_GENERATOR"
ID_GENERATOR_ARG_PREFIX = "DVCX_ID_GENERATOR_ARG_"
METASTORE_IMPORT_PATH = "DVCX_METASTORE"
METASTORE_ARG_PREFIX = "DVCX_METASTORE_ARG_"
WAREHOUSE_IMPORT_PATH = "DVCX_WAREHOUSE"
WAREHOUSE_ARG_PREFIX = "DVCX_WAREHOUSE_ARG_"
DISTRIBUTED_ARG_PREFIX = "DVCX_DISTRIBUTED_ARG_"


def get_id_generator():
    id_generator_import_path = os.environ.get(ID_GENERATOR_IMPORT_PATH)
    id_generator_arg_envs = get_envs_by_prefix(ID_GENERATOR_ARG_PREFIX)
    # Convert env variable names to keyword argument names by lowercasing them
    id_generator_args = {k.lower(): v for k, v in id_generator_arg_envs.items()}

    if id_generator_import_path:
        # ID generator paths are specified as (for example):
        # dql.data_storage.SQLiteIDGenerator
        if "." not in id_generator_import_path:
            raise RuntimeError(
                f"Invalid {ID_GENERATOR_IMPORT_PATH} import path:"
                f"{id_generator_import_path}"
            )
        module_name, _, class_name = id_generator_import_path.rpartition(".")
        id_generator = import_module(module_name)
        id_generator_class = getattr(id_generator, class_name)
    else:
        id_generator_class = SQLiteIDGenerator
    return id_generator_class(**id_generator_args)


def get_metastore(id_generator: "AbstractIDGenerator"):
    metastore_import_path = os.environ.get(METASTORE_IMPORT_PATH)
    metastore_arg_envs = get_envs_by_prefix(METASTORE_ARG_PREFIX)
    # Convert env variable names to keyword argument names by lowercasing them
    metastore_args = {k.lower(): v for k, v in metastore_arg_envs.items()}

    if metastore_import_path:
        # Metastore paths are specified as (for example):
        # dql.data_storage.SQLiteMetastore
        if "." not in metastore_import_path:
            raise RuntimeError(
                f"Invalid {METASTORE_IMPORT_PATH} import path: {metastore_import_path}"
            )
        module_name, _, class_name = metastore_import_path.rpartition(".")
        metastore = import_module(module_name)
        metastore_class = getattr(metastore, class_name)
    else:
        metastore_class = SQLiteMetastore
    return metastore_class(id_generator, **metastore_args)


def get_warehouse(id_generator: "AbstractIDGenerator"):
    warehouse_import_path = os.environ.get(WAREHOUSE_IMPORT_PATH)
    warehouse_arg_envs = get_envs_by_prefix(WAREHOUSE_ARG_PREFIX)
    # Convert env variable names to keyword argument names by lowercasing them
    warehouse_args = {k.lower(): v for k, v in warehouse_arg_envs.items()}

    if warehouse_import_path:
        # Warehouse paths are specified as (for example):
        # dql.data_storage.SQLiteWarehouse
        if "." not in warehouse_import_path:
            raise RuntimeError(
                f"Invalid {WAREHOUSE_IMPORT_PATH} import path: {warehouse_import_path}"
            )
        module_name, _, class_name = warehouse_import_path.rpartition(".")
        warehouse = import_module(module_name)
        warehouse_class = getattr(warehouse, class_name)
    else:
        warehouse_class = SQLiteWarehouse
    return warehouse_class(id_generator, **warehouse_args)


def get_distributed_class(**kwargs):
    distributed_import_path = os.environ.get("DVCX_DISTRIBUTED")
    distributed_arg_envs = get_envs_by_prefix(DISTRIBUTED_ARG_PREFIX)
    # Convert env variable names to keyword argument names by lowercasing them
    distributed_args = {k.lower(): v for k, v in distributed_arg_envs.items()}

    if not distributed_import_path:
        raise RuntimeError(
            "DVCX_DISTRIBUTED import path is required for distributed UDF processing."
        )
    # Distributed class paths are specified as (for example):
    # module.classname
    if "." not in distributed_import_path:
        raise RuntimeError(
            f"Invalid DVCX_DISTRIBUTED import path: {distributed_import_path}"
        )
    module_name, _, class_name = distributed_import_path.rpartition(".")
    distributed = import_module(module_name)
    distributed_class = getattr(distributed, class_name)
    return distributed_class(**distributed_args | kwargs)


def get_catalog(client_config: Optional[dict[str, Any]] = None) -> Catalog:
    """
    Function that creates Catalog instance with appropriate metastore
    and warehouse classes. Metastore class can be provided with env variable
    DVCX_METASTORE and if not provided, default one is used. Warehouse class
    can be provided with env variable DVCX_WAREHOUSE and if not provided,

    If classes expects some kwargs, they can be provided via env variables
    by adding them with prefix (DVCX_METASTORE_ARG_ and DVCX_WAREHOUSE_ARG_)
    and name of variable after, e.g. if it accepts team_id as kwargs
    we can provide DVCX_METASTORE_ARG_TEAM_ID=12345 env variable.
    """
    id_generator = get_id_generator()
    return Catalog(
        id_generator=id_generator,
        metastore=get_metastore(id_generator),
        warehouse=get_warehouse(id_generator),
        client_config=client_config,
    )
