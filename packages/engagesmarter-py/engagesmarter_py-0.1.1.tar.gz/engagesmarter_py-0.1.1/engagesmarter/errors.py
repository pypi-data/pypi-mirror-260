import httpx


class EngageSmarterError(Exception):
    pass


class EsApiResponseError(EngageSmarterError):
    HTTP_STATUS: int

    def __init__(self, **ctx):
        self.ctx = ctx

    def __str__(self):
        return (
            f"Engage Smarter API returned an error with http status: {self.HTTP_STATUS}. "
            f"Error details: {self.ctx!r}"
        )


class BadRequestApiError(EsApiResponseError):
    HTTP_STATUS = 400


class UnauthorizedApiError(EsApiResponseError):
    HTTP_STATUS = 401


class ForbiddenApiError(EsApiResponseError):
    HTTP_STATUS = 403


class NotFoundApiError(EsApiResponseError):
    HTTP_STATUS = 404


class MethodNotAllowedApiError(EsApiResponseError):
    HTTP_STATUS = 405


class AlreadyExistsApiError(EsApiResponseError):
    HTTP_STATUS = 409


class UnprocessableEntityApiError(EsApiResponseError):
    HTTP_STATUS = 422


class GenericApiError(EsApiResponseError):
    HTTP_STATUS = 500


class HttpResponseError(EsApiResponseError):
    """Used to handle http errors other than those defined by the Engage Smarter API."""

    def __init__(self, response: httpx.Response):
        self.status_code = response.status_code
        self.detail = response.content
        self.HTTP_STATUS = self.status_code

    def __str__(self):
        return (
            "Received an HTTP error from server\n"
            + f"Response status: {self.status_code}\n"
            + f"Response content: {self.detail}\n"
        )
