import httpx
import pytest

from client.engagesmarter import errors
from client.engagesmarter.errors_handler import handle_response_error


@pytest.mark.parametrize(
    "status_code, expected_error",
    [
        (400, errors.BadRequestApiError),
        (401, errors.UnauthorizedApiError),
        (403, errors.ForbiddenApiError),
        (404, errors.NotFoundApiError),
        (405, errors.MethodNotAllowedApiError),
        (409, errors.AlreadyExistsApiError),
        (422, errors.UnprocessableEntityApiError),
        (500, errors.GenericApiError),
        (501, errors.HttpResponseError),
        (502, errors.HttpResponseError),
    ],
)
def test_handle_response_error(
    status_code: int, expected_error: errors.EsApiResponseError
):
    mock_response = httpx.Response(status_code=status_code)
    with pytest.raises(errors.EsApiResponseError):
        handle_response_error(mock_response)
    with pytest.raises(expected_error):
        handle_response_error(mock_response)
    with pytest.raises(expected_error):
        handle_response_error(mock_response, parse_response=False)
