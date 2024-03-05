import pydantic

from client.engagesmarter.utils.pydantic import model_json


def test_model_json():
    class TestModelClass(pydantic.BaseModel):
        a: int
        b: str

    test_model_instance = TestModelClass(a=1, b="test")

    assert model_json(test_model_instance) == '{"a":1,"b":"test"}'
