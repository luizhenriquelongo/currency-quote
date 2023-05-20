import concurrent.futures
from typing import (
    List,
)

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.http import (
    JsonResponse,
    QueryDict,
)

import utils
from currencies import schemas
from currencies.api.serializers import (
    CurrencySerializer,
    ExchangeRateSerializer,
    QueryParamsSerializer,
)
from currencies.db_repository import (
    RepositoryInterface,
)
from currencies.interfaces import APIInterface
from currencies.models import ExchangeRate


class GetRatesUseCase:
    def __init__(self, api: APIInterface, repository: RepositoryInterface):
        self.response = schemas.UseCaseResponse()
        self._query_args = schemas.QueryArgs()
        self._api = api
        self._repository = repository
        self._model_objects_to_save: List[ExchangeRate] = []

    def execute(self, request: WSGIRequest):
        self.parse_query_args(request.GET)

        dates_to_search = utils.get_dates_between(
            start_date=self._query_args.start_date,
            end_date=self._query_args.end_date,
        )
        if not dates_to_search:
            return JsonResponse(self.response.dict())

        db_results = self._repository.filter_rates_by_date_range(
            start_date=utils.isodate_to_datetime(self._query_args.start_date),
            end_date=utils.isodate_to_datetime(self._query_args.end_date),
        )

        serializer = ExchangeRateSerializer(db_results, many=True)
        self.append_results_to_response(serializer.to_schemas())

        available_dates = {result.date.isoformat() for result in db_results}
        missing_dates = [date for date in dates_to_search if date not in available_dates]

        if missing_dates:
            api_results = self.fetch_missing_dates_from_api(missing_dates)
            self.append_results_to_response(api_results)

        return self.process_response()

    def parse_query_args(self, query_args: QueryDict) -> None:
        query_params = QueryParamsSerializer(data=query_args)
        query_params.is_valid(raise_exception=True)

        self._query_args.start_date = query_params.data["start_date"]
        self._query_args.end_date = query_params.data["end_date"]
        self._query_args.append_currencies = query_params.data["currencies"]

    def get_results_from_api(self, dates_to_search: List[str]) -> List[schemas.GetRatesAPIResponseSchema]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            tasks = [executor.submit(self._api.get_rates, date) for date in dates_to_search]

            completed_tasks = concurrent.futures.as_completed(tasks)
            return [task.result() for task in completed_tasks if task is not None]

    def save_results_to_db(self):
        with transaction.atomic():
            ExchangeRate.objects.bulk_create(self._model_objects_to_save)

    def process_response(self) -> JsonResponse:
        if self._query_args.append_currencies:
            self.append_currencies_to_response()

        self.response.results = sorted(self.response.results, key=lambda obj: obj.date)
        return JsonResponse(self.response.dict(exclude_none=True))

    def fetch_missing_dates_from_api(self, missing_dates: List[str]) -> List[schemas.GetRatesAPIResponseSchema]:
        results = self.get_results_from_api(missing_dates)

        [self._model_objects_to_save.extend(result.to_db_model()) for result in results]
        self.save_results_to_db()

        return results

    def append_results_to_response(self, results: List[schemas.GetRatesAPIResponseSchema]):
        self.response.results.extend([result for result in results])

    def append_currencies_to_response(self):
        currencies = self._repository.get_currencies(settings.MAPPED_CURRENCIES)
        serializer = CurrencySerializer(currencies, many=True)
        self.response.currencies = schemas.CurrenciesSchema.parse_obj(
            {
                currency_data["code"]: schemas.CurrencySchema.parse_obj(currency_data)
                for currency_data in serializer.data
            }
        )
