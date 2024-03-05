from typing import Mapping

from typing_extensions import TypeGuard


def is_mapping(obj: object) -> TypeGuard[Mapping[str, object]]:
    return isinstance(obj, Mapping)
