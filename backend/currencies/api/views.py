from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)
from rest_framework.decorators import (
    api_view,
)

from currencies import (
    use_cases,
)
from currencies.api.serializers import (
    QueryParamsSerializer,
)
from currencies.db_repository import DBRepository
from currencies.docs import (
    definitions,
    examples,
)
from currencies.vat_comply_api import VATComplyAPI


@extend_schema(
    methods=["GET"],
    summary="List rates by date",
    description="Returns a list of rates quoted between two dates",
    parameters=[QueryParamsSerializer],
    auth=[],
    tags=["Rates"],
    responses={
        200: OpenApiResponse(
            response=definitions.Response200Schema,
            description="Returns a list of exchange rates for the dates and return currencies descriptions if currency "
            "flag is on.",
            examples=[
                examples.CurrenciesFlagOn,
                examples.CurrenciesFlagOff,
            ],
        ),
        400: OpenApiResponse(
            response={
                "properties": {
                    "field_name": {
                        "items": {"type": "string", "description": "error description"},
                        "title": "ErrorsArray",
                        "type": "array",
                    },
                },
                "title": "ErrorResponse",
                "type": "object",
            },
            description="Bad Requests",
            examples=[OpenApiExample(name="Bad Request", value={"currencies": ["Must be a valid boolean."]})],
        ),
    },
)
@api_view(["GET"])
def get_rates(request: WSGIRequest) -> JsonResponse:
    api = VATComplyAPI()
    repository = DBRepository()
    use_case = use_cases.GetRatesUseCase(api, repository)
    response = use_case.execute(request)
    return response
