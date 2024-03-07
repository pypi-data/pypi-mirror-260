import inspect
import re
from collections.abc import Sequence
from datetime import datetime
from types import GenericAlias
from typing import ClassVar, Union, get_args, get_origin

from pydantic import BaseModel

from dql.query.udf import UDFOutputSpec
from dql.sql.types import JSON, Array, Binary, Boolean, DateTime, Float, Int, String

TYPE_TO_DVCX = {
    int: Int,
    str: String,
    float: Float,
    bool: Boolean,
    datetime: DateTime,
    bytes: Binary,
    list: Array,
    dict: JSON,
}


FeatureClass = type["Feature"]
FeatureClassSeq = Sequence[FeatureClass]


class Feature(BaseModel):
    """A base class for defining data classes that serve as inputs and outputs for
    DataFrame processing functions like `map()`, `generate()`, etc. Inherits from
    `pydantic`'s BaseModel, allowing for data validation and definition.
    """

    expand_name: ClassVar[bool] = True
    delimiter: ClassVar[str] = "__"
    is_stream: ClassVar[bool] = False

    @classmethod
    def prefix(cls) -> str:
        return cls.normalize(cls.__name__)

    @classmethod
    def normalize(cls, name: str) -> str:
        if cls.expand_name and cls.delimiter and cls.delimiter.lower() in name.lower():
            raise RuntimeError(
                f"variable '{name}' cannot be used because it contains {cls.delimiter}"
            )
        return Feature.to_snake_case(name)

    @staticmethod
    def to_snake_case(name: str) -> str:
        """Convert a CamelCase name to snake_case."""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    @staticmethod
    def _convert_type(typ):
        res = TYPE_TO_DVCX.get(typ, None)
        if res:
            return res

        orig = get_origin(typ)
        if orig == list:
            return Array
        if orig == dict:
            return JSON

        args = get_args(typ)
        if orig == Union and len(args) == 2 and (type(None) in args):
            return Feature._convert_type(args[0])

        raise RuntimeError(f"Cannot recognize type {typ}")

    @staticmethod
    def _iter_fields(fields):
        for name, f_info in fields.items():
            yield name, f_info.annotation, f_info.is_required()

    @classmethod
    def _flatten_full_schema(cls, fields, name_path):
        for name, anno, is_required in cls._iter_fields(fields):
            name = cls.normalize(name)

            # adding guard for GenericAlias, as `issubclass` on 3.11/3.12 accept
            # `types.GenericAlias` (eg: `list[int]`) as a first argument.
            # However, this behavior has been forbidden on 3.13 again.
            # See: https://github.com/python/cpython/issues/101162.
            if (
                inspect.isclass(anno)
                and not isinstance(anno, GenericAlias)
                and issubclass(anno, Feature)
            ):
                yield from cls._flatten_full_schema(
                    anno.model_fields, name_path + [name]
                )
            else:
                if cls.expand_name:
                    lst = [cls.prefix()] + name_path + [name]
                    name = cls.delimiter.join(lst)
                yield name, Feature._convert_type(anno), is_required

    @classmethod
    def to_udf_spec(cls):
        full_schema = cls._flatten_full_schema(cls.model_fields, [])
        return [(name, typ) for name, typ, is_required in full_schema]

    @staticmethod
    def features_to_udf_spec(fr_classes: FeatureClassSeq) -> UDFOutputSpec:
        return dict(
            item
            for b in fr_classes
            for item in b.to_udf_spec()  # type: ignore[attr-defined]
        )

    def _flatten_fields_values(self, fields, dump):
        for name, anno, _ in self._iter_fields(fields):
            value = dump[name]
            if inspect.isclass(anno) and issubclass(anno, Feature):
                yield from self._flatten_fields_values(anno.model_fields, value)
            else:
                yield value

    def flatten(self):
        return tuple(self._flatten_fields_values(self.model_fields, self.model_dump()))

    @staticmethod
    def flatten_list(objs):
        return tuple(val for obj in objs for val in obj.flatten())

    @classmethod
    def _unflatten(cls, dump, path):
        res = {}
        for name, anno, _ in Feature._iter_fields(cls.model_fields):
            name_norm = cls.normalize(name)
            if cls.expand_name:
                curr_path = path + cls.delimiter + name_norm
            else:
                curr_path = name_norm

            if inspect.isclass(anno) and issubclass(anno, Feature):
                val = anno._unflatten(dump, curr_path)
                res[name] = val
            else:
                res[name] = dump[curr_path]
        r = cls(**res)
        return r

    @classmethod
    def unflatten(cls, dump):
        return cls._unflatten(dump, cls.prefix())


class ShallowFeature(Feature):
    expand_name: ClassVar[bool] = False


class StreamFeature(ShallowFeature):
    is_stream = True

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self._stream = None

    def set_stream(self, stream):
        self._stream = stream

    def open(self):
        return self._stream
