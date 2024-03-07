from collections.abc import Sequence
from typing import Union

from dql.catalog import get_catalog
from dql.lib.feature import Feature, FeatureClass, FeatureClassSeq
from dql.lib.udf import Aggregator, BatchMapper, Generator, Mapper
from dql.query import Stream


class FeatureConvertor:
    @property
    def udf_params_list(self):
        return self._udf_params_list

    @property
    def udf_output_spec(self):
        return self._udf_output_spec

    @property
    def is_single_input(self):
        return self._is_single_input

    @property
    def is_single_output(self):
        return self._is_single_output

    @property
    def has_stream(self):
        return self._has_stream

    @property
    def cache(self):
        return self._cache

    def __init__(
        self,
        inputs: Union[FeatureClass, FeatureClassSeq] = (),
        outputs: Union[FeatureClass, FeatureClassSeq] = (),
        is_input_batched: bool = True,
    ):
        self._is_input_batched = is_input_batched

        self._inputs, self._is_single_input = self._convert_to_sequence(inputs)
        self._outputs, self._is_single_output = self._convert_to_sequence(outputs)

        self._validate_schema("params", self._inputs)
        self._validate_schema("output", self._outputs)

        self._has_stream = any(
            f.is_stream  # type: ignore[attr-defined]
            for f in self._inputs
        )
        self._cache = get_catalog().cache

        udf_params_spec = Feature.features_to_udf_spec(self._inputs)
        stream_prm = [Stream()] if self._has_stream else []
        self._udf_params_list = stream_prm + list(udf_params_spec.keys())

        self._udf_output_spec = Feature.features_to_udf_spec(self._outputs)  # type: ignore[attr-defined]

    @staticmethod
    def _convert_to_sequence(
        arg: Union[FeatureClass, FeatureClassSeq],
    ) -> tuple[FeatureClassSeq, bool]:
        if not isinstance(arg, Sequence):
            return [arg], True
        else:
            return arg, False

    def deserialize_objs(self, params, args):
        streams = []
        if self._has_stream:
            for row in args:
                streams.append(row.pop(0))

        obj_rows = [self._params_to_objects(params, arg) for arg in args]
        for row, stream in zip(obj_rows, streams):
            for feature in row:
                if feature.is_stream:
                    feature.set_stream(stream)
                    feature.set_cache(self._cache)

        return obj_rows

    def _params_to_objects(self, params, args):
        new_params = params if not self._has_stream else params[1:]
        return [cls.unflatten(dict(zip(new_params, args))) for cls in self._inputs]

    def _validate_schema(self, context: str, features: FeatureClassSeq):
        for type_ in features:
            if not isinstance(type_, type):
                raise ValueError(
                    f"{self.__class__.__name__} does not accept instances as"
                    f" {context}. A class must be provided"
                )
            if not issubclass(type_, Feature):
                raise ValueError(
                    f"{self.__class__.__name__} does not accept {context} "
                    f"of type {type_}. It must be subclass of Feature"
                )

    def validate_output_obj(self, result_objs, *args, **kwargs):
        for row in result_objs:
            if len(row) != len(self._outputs):
                raise RuntimeError(
                    f"Output of {self.__class__.__name__} must have "
                    f"{len(self._outputs)} objects while {len(row)} "
                    f"were provided"
                )

            for num, (o, type_) in enumerate(zip(row, self._outputs)):
                if not isinstance(o, type_):
                    raise RuntimeError(
                        f"Expected the output at index {num} of "
                        f"{self.__class__.__name__} to be '{type_.__name__}' "
                        f", but found it to be of type '{type(o).__name__}'"
                    )

    def process_rows(self, udf, rows):
        obj_rows = self.deserialize_objs(udf.params, rows)
        if self.is_single_input:
            obj_rows = [objs[0] for objs in obj_rows]

        if not self._is_input_batched:
            assert len(obj_rows) == 1, (
                f"{udf.__class__.__name__} takes "
                f"{len(obj_rows)} rows while it's not batched"
            )
            obj_rows = obj_rows[0]

        returned_value = udf.process(obj_rows)
        if self._is_input_batched:
            result_objs = list(returned_value)
        else:
            result_objs = [returned_value]

        if self.is_single_output:
            result_objs = [[x] for x in result_objs]

        self.validate_output_obj(result_objs)

        res = [Feature.flatten_list(objs) for objs in result_objs]

        if not self._is_input_batched:
            assert len(res) == 1, (
                f"{udf.__class__.__name__} returns {len(obj_rows)} "
                f"rows while it's not batched"
            )
            return res[0]
        return res


class FeatureAggregator(Aggregator):
    def __init__(
        self,
        inputs: Union[FeatureClass, FeatureClassSeq] = (),
        outputs: Union[FeatureClass, FeatureClassSeq] = (),
        batch=1,
    ):
        self._fc = FeatureConvertor(inputs, outputs)
        super().__init__(self._fc.udf_params_list, self._fc.udf_output_spec, batch)

    def __call__(self, args):
        return self._fc.process_rows(self, args)


class FeatureMapper(Mapper):
    def __init__(
        self,
        inputs: Union[FeatureClass, FeatureClassSeq] = (),
        outputs: Union[FeatureClass, FeatureClassSeq] = (),
        batch=1,
    ):
        self._fc = FeatureConvertor(inputs, outputs, is_input_batched=False)
        super().__init__(self._fc.udf_params_list, self._fc.udf_output_spec, batch)

    def __call__(self, args):
        return self._fc.process_rows(self, args)


class FeatureBatchMapper(BatchMapper):
    def __init__(
        self,
        inputs: Union[FeatureClass, FeatureClassSeq] = (),
        outputs: Union[FeatureClass, FeatureClassSeq] = (),
        batch=1,
    ):
        self._fc = FeatureConvertor(inputs, outputs)
        super().__init__(self._fc.udf_params_list, self._fc.udf_output_spec, batch)

    def __call__(self, args):
        return self._fc.process_rows(self, args)


class FeatureGenerator(Generator):
    def __init__(
        self,
        inputs: Union[FeatureClass, FeatureClassSeq] = (),
        outputs: Union[FeatureClass, FeatureClassSeq] = (),
        batch=1,
    ):
        self._fc = FeatureConvertor(inputs, outputs)
        super().__init__(self._fc.udf_params_list, self._fc.udf_output_spec, batch)

    def __call__(self, args):
        return self._fc.process_rows(self, args)
