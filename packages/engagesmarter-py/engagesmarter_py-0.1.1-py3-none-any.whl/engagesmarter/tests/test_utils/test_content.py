import pytest
from pydantic import BaseModel

from client.engagesmarter.utils.content import prepare_content


class TestModel(BaseModel):
    test_int: int
    test_str: str


test_model1 = TestModel(
    test_int=1,
    test_str="test1",
)
test_dict1 = {
    "test_int": 1,
    "test_str": "test1",
}
test_json1 = '{"test_int":1,"test_str":"test1"}'

test_model2 = TestModel(
    test_int=2,
    test_str="test2",
)
test_dict2 = {
    "test_int": 2,
    "test_str": "test2",
}
test_json2 = '{"test_int":2,"test_str":"test2"}'

test_models = [test_model1, test_model2]
test_dicts = [test_dict1, test_dict2]
test_jsons = "[" + test_json1 + "," + test_json2 + "]"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (test_json1, test_json1),
        (test_model1, test_json1),
        (test_model2, test_json2),
        (test_models, test_jsons),
        (test_dict1, test_json1),
        (test_dict2, test_json2),
        (test_dicts, test_jsons),
    ],
)
def test_prepare_content(test_input, expected):
    content = prepare_content(test_input)
    assert content == expected
