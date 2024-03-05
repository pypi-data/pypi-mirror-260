import pydantic

PYDANTIC_V2 = pydantic.VERSION.startswith("2.")


def model_json(model: pydantic.BaseModel, *, indent: int | None = None) -> str:
    if PYDANTIC_V2:
        return model.model_dump_json(indent=indent)
    return model.json(indent=indent)  # type: ignore
