from json import JSONDecodeError

import httpx

from .errors import (
    AlreadyExistsApiError,
    BadRequestApiError,
    ForbiddenApiError,
    GenericApiError,
    HttpResponseError,
    MethodNotAllowedApiError,
    NotFoundApiError,
    UnauthorizedApiError,
    UnprocessableEntityApiError,
)


def handle_response_error(response: httpx.Response, parse_response: bool = True):
    try:
        response_content = response.json() if parse_response else {}
    except JSONDecodeError:
        response_content = {"detail": response.text}

    error_detail = response_content.get("detail")
    if not isinstance(error_detail, dict):  # normalize detail if not data structure
        error_detail = {"response": error_detail}

    error_args = error_detail if error_detail else response_content

    if response.status_code == BadRequestApiError.HTTP_STATUS:
        error_type = BadRequestApiError
    elif response.status_code == UnauthorizedApiError.HTTP_STATUS:
        error_type = UnauthorizedApiError
    elif response.status_code == AlreadyExistsApiError.HTTP_STATUS:
        error_type = AlreadyExistsApiError
    elif response.status_code == ForbiddenApiError.HTTP_STATUS:
        error_type = ForbiddenApiError
    elif response.status_code == NotFoundApiError.HTTP_STATUS:
        error_type = NotFoundApiError
    elif response.status_code == UnprocessableEntityApiError.HTTP_STATUS:
        error_type = UnprocessableEntityApiError
    elif response.status_code == MethodNotAllowedApiError.HTTP_STATUS:
        error_type = MethodNotAllowedApiError
    elif response.status_code == GenericApiError.HTTP_STATUS:
        error_type = GenericApiError
    else:
        raise HttpResponseError(response=response)
    raise error_type(**error_args)
