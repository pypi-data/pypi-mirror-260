import os

import pytest
from pydantic import Field

from dql.lib.feature import Feature
from dql.lib.feature_udf import (
    FeatureAggregator,
    FeatureBatchMapper,
    FeatureGenerator,
    FeatureMapper,
)
from dql.lib.stream import FileStream
from dql.query import Stream
from dql.sql.types import Int


class TestInput(Feature):
    name: str
    parent: str = Field(default="")
    size: int = Field(default=0)


class TestOutput(Feature):
    full_path: str
    size_squared: int = Field(default=0)


class MyAgg(FeatureAggregator):
    def __init__(self):
        super().__init__([TestInput], [TestOutput])

    def process(self, args):
        row = args[0]
        input = row[0]
        output = TestOutput(
            full_path=os.path.join(input.parent, input.name), size_squared=input.size**2
        )
        yield (output,)


def test_feature_udf():
    name = "file.txt"
    path = "dir1/dir2"
    size = 16
    params = ((name, path, size),)

    agg = MyAgg()
    res = list(agg(params))
    assert 1 == len(res)

    full_path, size_squared = res[0]
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2


class MyAggStream(FeatureAggregator):
    def __init__(self):
        super().__init__([FileStream], [TestOutput])

    def process(self, args):
        output = TestOutput(full_path="xx", size_squared=5)
        yield (output,)


def test_feature_udf_with_stream():
    stream = FileStream(name="tmp.jpg")
    args = ([Stream()] + list(stream.flatten()),)

    agg = MyAggStream()
    res = list(agg(args))
    assert 1 == len(res)


def test_feature_udf_with_single_input_and_output():
    class MyAgg(FeatureAggregator):
        def __init__(self):
            super().__init__(TestInput, TestOutput)

        def process(self, args):
            input = args[0]
            output = TestOutput(
                full_path=os.path.join(input.parent, input.name),
                size_squared=input.size**2,
            )
            yield output

    name = "f1.txt"
    path = "dd3"
    size = 343
    params = ((name, path, size),)

    agg = MyAgg()
    res = list(agg(params))
    assert 1 == len(res)

    full_path, size_squared = res[0]
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2


def test_incompatible_params_types():
    with pytest.raises(ValueError):

        class MyAggParamInstance(FeatureAggregator):
            def __init__(self):
                super().__init__(
                    (
                        ("size", Int),
                        ("test", Int),
                    ),
                    TestOutput,
                )

        MyAggParamInstance()

    with pytest.raises(ValueError):

        class MyAggParamType(FeatureAggregator):
            def __init__(self):
                super().__init__([Int, Int], TestOutput)

        MyAggParamType()

    with pytest.raises(ValueError):

        class MyAggOutputInstance(FeatureAggregator):
            def __init__(self):
                super().__init__([Int], TestOutput)

        MyAggOutputInstance()


def test_output_length_missmatch_with_params():
    class MyAggWrongLength(FeatureAggregator):
        def __init__(self):
            super().__init__(TestInput, [TestOutput, TestOutput])

        def process(self, args):
            input = args[0]
            output = TestOutput(
                full_path=os.path.join(input.parent, input.name),
                size_squared=input.size**2,
            )
            yield output, output, output

    with pytest.raises(RuntimeError):
        params = (("file", "dir", 12345),)
        agg = MyAggWrongLength()
        agg(params)


def test_output_type_missmatch_with_params_types():
    class MyAggWrongOutputType(FeatureAggregator):
        def __init__(self):
            super().__init__(TestInput, TestOutput)

        def process(self, args):
            yield 536

    with pytest.raises(RuntimeError):
        params = (("file", "dir", 12345),)
        agg = MyAggWrongOutputType()
        agg(params)


def test_mapper():
    class MyMap(FeatureMapper):
        def __init__(self):
            super().__init__(TestInput, TestOutput)

        def process(self, test_input):
            output = TestOutput(
                full_path=os.path.join(test_input.parent, test_input.name),
                size_squared=test_input.size**2,
            )
            return output

    name = "img001.jpg"
    path = "data/dogs"
    size = 56743
    params = ((name, path, size),)

    agg = MyMap()
    res = agg(params)

    full_path, size_squared = res
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2


def test_batch_mapper():
    class MyBatchMap(FeatureBatchMapper):
        def __init__(self):
            super().__init__(TestInput, TestOutput, 2)

        def process(self, test_inputs):
            for test_input in test_inputs:
                output = TestOutput(
                    full_path=os.path.join(test_input.parent, test_input.name),
                    size_squared=test_input.size**2,
                )
                yield output

    name = "img001.jpg"
    path = "data/dogs"
    size = 56743
    params = ((name, path, size), ("1_" + name, "1_" + path, size * 2))

    agg = MyBatchMap()
    res = agg(params)

    assert 2 == len(res)

    full_path, size_squared = res[0]
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2

    full_path, size_squared = res[1]
    assert full_path == os.path.join("1_" + path, "1_" + name)
    assert size_squared == (size * 2) ** 2


def test_generator():
    class MyGen(FeatureGenerator):
        def __init__(self):
            super().__init__(TestInput, TestOutput)

        def process(self, test_inputs):
            for test_input in test_inputs:
                yield TestOutput(
                    full_path=os.path.join(test_input.parent, test_input.name) + "_1",
                    size_squared=test_input.size**2,
                )

                yield TestOutput(
                    full_path=os.path.join(test_input.parent, test_input.name) + "_2",
                    size_squared=test_input.size**3,
                )

    name = "img742.jpg"
    path = "d1/cats"
    size = 384
    params = ((name, path, size),)

    agg = MyGen()
    res = agg(params)

    assert 2 == len(res)

    full_path, size_squared = res[0]
    assert full_path == os.path.join(path, name) + "_1"
    assert size_squared == size**2

    full_path, size_squared = res[1]
    assert full_path == os.path.join(path, name) + "_2"
    assert size_squared == size**3
