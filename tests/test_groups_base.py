# -*- coding: utf-8 -*-
import os
import io
import pandas as pd
import pytest
from eodhdc import exceptions
from eodhdc.base import BaseGroup

exceptions = [
    (("some/type", b'...'), "content", exceptions.UnsupportedContentType),
    (("application/json", b'{...}'), "content", exceptions.JSONDecodeError),
    (("text/html", ''.encode("utf-16")), "content", exceptions.BytesDecodeError),
    (("text/html", b'a,b'), "content:/xxx/xxx.csv", exceptions.FileIOError),
    (("text/html", b'a,b'), "pandas:/xxx/xxx.xxx", exceptions.UnsupportedExtension),
    (("text/html", b'a,b'), "pandas:/xxx/xxx.csv", exceptions.PandasRuntimeError)
]

results = [
    (("application/json", b'{"a":1,"b":2}'), "response", None, b'{"a":1,"b":2}'),
    (("text/html", b'a,b\n1,2'), "response:/tmp/result1.csv", None, b'a,b\n1,2'),
    (("application/json", b'{"a":1,"b":2}'), "content", None, {"a": 1, "b": 2}),
    (("text/html", b'a,b\n1,2'), "content:/tmp/result2.csv", None, "a,b\n1,2"),
    (("application/json", b'[{"a":1,"b":2}]'), "pandas", {
            "change:columns": {"b": "cb", "a": "ca"}, "change:reorder": True, "change:reindex": "cb"
        }, pd.read_json('[{"ca":1,"cb":2}]').set_index("cb")),
    (("text/html", b'a,b\n1,2'), "pandas:/tmp/result3.csv", {
            "change:columns": {"b": "cb", "a": "ca"}, "change:reorder": True, "change:reindex": "cb"
        }, pd.read_csv(io.StringIO("ca,cb\n1,2")).set_index("cb")),
    (("text/html", b'a,b\n1,2'), "pandas:/tmp/result3.json", None, pd.read_csv(io.StringIO("a,b\n1,2"))),
    (("text/html", b'a,b\n1,2'), "pandas:/tmp/result3.html", None, pd.read_csv(io.StringIO("a,b\n1,2")))
]


def client():
    """Client dummy function."""


@pytest.mark.groups
@pytest.mark.parametrize("response, output, exception", exceptions)
def test_base_exceptions(response, output, exception):
    """Test base prepare exceptions."""
    with pytest.raises(exception):
        group = BaseGroup(client)
        group.process(response, output)


@pytest.mark.groups
def test_base_prepare():
    """Test base prepare method."""
    source = {
        "self": "<...>", "symbol": "MCD.US", "period": "d", "order": "a", "start": None,
        "finish": None,  "fmt": "csv", "output": "pandas", "options": None
    }
    group = BaseGroup(client)
    result = group.prepare(source, ["symbol"])
    assert result == {"api_token": "demo", "period": "d", "order": "a", "fmt": "csv"}


@pytest.mark.groups
@pytest.mark.parametrize("response, output, writer, result", results)
def test_base_process(response, output, writer, result):
    """Test base process method."""
    group = BaseGroup(client)
    parts = output.split(":")
    if isinstance(result, pd.DataFrame):
        pd.testing.assert_frame_equal(group.process(response, output, writer), result)
    else:
        assert group.process(response, output) == result
    if "." in output:
        assert os.path.exists(parts[1])
        os.remove(parts[1])
