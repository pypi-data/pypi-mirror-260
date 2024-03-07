from collections.abc import Sequence

from dql.catalog import get_catalog
from dql.lib.facet import Facet
from dql.lib.udf import Aggregator
from dql.query import Stream


class FacetAggregator(Aggregator):
    def __init__(
        self,
        inputs: Sequence[type[Facet]] = (),
        outputs: Sequence[type[Facet]] = (),
        batch=1,
    ):
        self._inputs = inputs
        self._outputs = outputs
        self._has_stream = any(f.is_stream for f in self._inputs)
        self._cache = get_catalog().cache

        self._output_dict = dict(Facet.flatten_schema_list(self._outputs))
        super().__init__(self._input_classes_to_params(), self._output_dict, batch)

    def _input_classes_to_params(self):
        schemas = Facet.flatten_schema_list(self._inputs)
        stream_prm = [Stream()] if self._has_stream else []
        params = stream_prm + list(dict(schemas).keys())
        return params

    def __call__(self, args):
        obj_rows = self._deserialize_objs(args)
        result_objs = list(self.process(obj_rows))
        return [Facet.flatten_list(objs) for objs in result_objs]

    def _deserialize_objs(self, args):
        streams = []
        if self._has_stream:
            for row in args:
                streams.append(row.pop(0))

        obj_rows = [self._params_to_objects(arg) for arg in args]
        for row, stream in zip(obj_rows, streams):
            for facet in row:
                if facet.is_stream:
                    facet.set_stream(stream)
                    facet.set_cache(self._cache)

        return obj_rows

    def _params_to_objects(self, args):
        params = self.params if not self._has_stream else self.params[1:]
        return [cls.unflatten(dict(zip(params, args))) for cls in self._inputs]
