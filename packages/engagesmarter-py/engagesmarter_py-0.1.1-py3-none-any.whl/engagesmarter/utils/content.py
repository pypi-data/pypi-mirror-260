import json
from typing import Any

import pydantic

from .pydantic import model_json


def prepare_content(content: Any) -> str:
    SEPARATORS = (",", ":")
    if isinstance(content, str):
        pass

    elif isinstance(content, pydantic.BaseModel):
        content = model_json(content)

    elif isinstance(content, list):
        updated_content = []
        for c in content:
            if isinstance(c, pydantic.BaseModel):
                updated_content.append(json.loads(model_json(c)))
            else:
                updated_content.append(c)
        content = json.dumps(updated_content, separators=SEPARATORS)

    else:
        content = json.dumps(content, separators=SEPARATORS)

    return content
