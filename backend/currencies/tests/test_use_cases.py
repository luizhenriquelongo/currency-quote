import datetime
import json
from collections import Counter

import pytest
import pytest_mock
from django.http import (
    JsonResponse,
    QueryDict,
)
from django.test import RequestFactory
from rest_framework import exceptions

from currencies import schemas
from currencies.db_repository import RepositoryInterface
from currencies.interfaces import APIInterface
from currencies.models import (
    Currency,
    ExchangeRate,
)
from currencies.use_cases import GetRatesUseCase


@pytest.fixture
def mock_api_interface(mocker):
    return mocker.Mock(spec=APIInterface)


@pytest.fixture
def mock_repository_interface(mocker):
    return mocker.Mock(spec=RepositoryInterface)


@pytest.fixture
def mock_parse_query_args(get_rates_use_case, mocker):
    def modify_query_args(_):
        get_rates_use_case._query_args.start_date = "2023-01-10"
        get_rates_use_case._query_args.end_date = "2023-01-15"

    mock = mocker.patch("currencies.use_cases.GetRatesUseCase.parse_query_args")
    mock.side_effect = modify_query_args
    return mock


@pytest.fixture
def get_rates_use_case(mock_api_interface, mock_repository_interface):
    return GetRatesUseCase(mock_api_interface, mock_repository_interface)


@pytest.fixture
def request_factory():
    return RequestFactory()


def create_exchange_rate(date):
    exchange_rate = ExchangeRate(date=date)
    return exchange_rate


def test_execute_with_no_dates_to_search(get_rates_use_case, mock_repository_interface, mock_api_interface):
    request = RequestFactory().get("/rates/")
    with pytest.raises(exceptions.ValidationError) as error:
        get_rates_use_case.execute(request)
        assert error.value.status_code == 400

    mock_repository_interface.filter_rates_by_date_range.assert_not_called()
    mock_api_interface.get_rates.assert_not_called()


def test_execute_with_not_business_days_dates_to_search(
    get_rates_use_case, mock_repository_interface, mock_api_interface, mock_parse_query_args, mocker
):
    mock_get_dates_between = mocker.patch("utils.get_dates_between")
    mock_get_dates_between.return_value = []

    request = RequestFactory().get("/rates/")
    request.GET = QueryDict("start_date=2023-01-14&end_date=2023-01-15&currencies=1")
    raw_response = get_rates_use_case.execute(request)

    assert isinstance(raw_response, JsonResponse)
    assert raw_response.status_code == 200
    response = json.loads(raw_response.content)

    assert len(response["results"]) == 0
    mock_parse_query_args.assert_called_once_with(request.GET)
    mock_get_dates_between.assert_called_once_with(start_date="2023-01-10", end_date="2023-01-15")
    mock_repository_interface.filter_rates_by_date_range.assert_not_called()
    mock_api_interface.get_rates.assert_not_called()


@pytest.mark.django_db
def test_execute_with_dates_to_search(get_rates_use_case, mock_repository_interface, mocker, mock_parse_query_args):
    mock_repository_interface.filter_rates_by_date_range.return_value = [
        create_exchange_rate(datetime.date(2023, 1, 10)),
        create_exchange_rate(datetime.date(2023, 1, 15)),
    ]

    mock_to_schemas = mocker.patch("currencies.api.serializers.ExchangeRateListSerializer.to_schemas")
    mock_to_schemas.return_value = [
        schemas.GetRatesAPIResponseSchema.parse_obj(
            {
                "date": "2023-01-10",
                "base": "USD",
                "rates": {
                    "EUR": "0.9267840593141800",
                    "USD": "1.0000000000000000",
                    "BRL": "4.3874884151992600",
                    "JPY": "112.0111214087120000",
                },
            },
        ),
        schemas.GetRatesAPIResponseSchema.parse_obj(
            {
                "date": "2023-01-11",
                "base": "USD",
                "rates": {
                    "EUR": "0.9267840593141800",
                    "USD": "1.0000000000000000",
                    "BRL": "4.3874884151992600",
                    "JPY": "112.0111214087120000",
                },
            },
        ),
    ]

    mock_fetch_missing_dates_from_api = mocker.patch(
        "currencies.use_cases.GetRatesUseCase.fetch_missing_dates_from_api"
    )
    mock_fetch_missing_dates_from_api.return_value = []

    request = RequestFactory().get("/rates/")
    request.GET = QueryDict("start_date=2023-01-01&end_date=2023-01-07&currencies=1")
    raw_response = get_rates_use_case.execute(request)

    assert isinstance(raw_response, JsonResponse)
    assert raw_response.status_code == 200

    response = json.loads(raw_response.content)

    assert len(response["results"]) == 2
    mock_parse_query_args.assert_called_once_with(request.GET)
    mock_repository_interface.filter_rates_by_date_range.assert_called_once_with(
        start_date=datetime.datetime(2023, 1, 10, 0, 0), end_date=datetime.datetime(2023, 1, 15, 0, 0)
    )
    mock_to_schemas.assert_called_once()
    mock_fetch_missing_dates_from_api.assert_called_once_with(["2023-01-11", "2023-01-12", "2023-01-13"])


def test_parse_query_args(get_rates_use_case, mocker):
    query_dict = QueryDict("start_date=2023-01-01&end_date=2023-01-05&currencies=1")
    mocker.patch.object(get_rates_use_case, "_query_args", mocker.Mock())

    get_rates_use_case.parse_query_args(query_dict)

    assert get_rates_use_case._query_args.start_date == "2023-01-01"
    assert get_rates_use_case._query_args.end_date == "2023-01-05"
    assert get_rates_use_case._query_args.append_currencies is True


def test_get_results_from_api(get_rates_use_case, mocker):
    dates_to_search = ["2023-01-01", "2023-01-02", "2023-01-03"]
    mock_api_interface = mocker.patch.object(get_rates_use_case, "_api")
    mock_api_interface.get_rates.side_effect = [1.23, 1.34, 1.45]

    results = get_rates_use_case.get_results_from_api(dates_to_search)

    assert len(results) == 3
    assert Counter(results) == Counter([1.23, 1.34, 1.45])
    assert mock_api_interface.get_rates.call_count == 3


@pytest.mark.django_db
def test_save_results_to_db(get_rates_use_case, mocker):
    mock_objects_bulk_create = mocker.patch.object(ExchangeRate.objects, "bulk_create")

    exchange_rates = [
        create_exchange_rate(datetime.date(2023, 1, 1)),
        create_exchange_rate(datetime.date(2023, 1, 2)),
    ]
    get_rates_use_case._model_objects_to_save = exchange_rates

    get_rates_use_case.save_results_to_db()

    mock_objects_bulk_create.assert_called_once_with(exchange_rates)


def test_process_response_when_appending_currencies(get_rates_use_case, mocker):
    get_rates_use_case.response.currencies = None
    get_rates_use_case._query_args.append_currencies = True

    mock_append_currencies = mocker.patch("currencies.use_cases.GetRatesUseCase.append_currencies_to_response")

    currencies = {
        "USD": {"name": "US Dollar", "code": "USD", "symbol": "$"},
        "BRL": {"name": "Brazilian Real", "code": "BRL", "symbol": "$"},
        "EUR": {"name": "Euro", "code": "EUR", "symbol": "$"},
        "JPY": {"name": "Japanese Yene", "code": "JPY", "symbol": "$"},
    }

    def append_currencies():
        get_rates_use_case.response.currencies = schemas.CurrenciesSchema.parse_obj(currencies)

    mock_append_currencies.side_effect = append_currencies

    raw_response = get_rates_use_case.process_response()

    assert isinstance(raw_response, JsonResponse)
    assert raw_response.status_code == 200

    response = json.loads(raw_response.content)

    assert response["currencies"] == currencies
    mock_append_currencies.assert_called_once()


def test_fetch_missing_dates_from_api(get_rates_use_case, mocker: pytest_mock.MockerFixture):
    missing_dates = ["2023-01-02", "2023-01-03"]

    mock_get_results_from_api = mocker.patch.object(get_rates_use_case, "get_results_from_api")

    schema1 = mocker.MagicMock(spec=schemas.GetRatesAPIResponseSchema)
    model1 = mocker.MagicMock(spec=ExchangeRate)
    schema1.to_db_model.return_value = [model1]
    mock_get_results_from_api.return_value = [schema1]

    mock_save_results_to_db = mocker.patch("currencies.use_cases.GetRatesUseCase.save_results_to_db")

    results = get_rates_use_case.fetch_missing_dates_from_api(missing_dates)

    assert results == [schema1]
    assert model1 in get_rates_use_case._model_objects_to_save
    mock_get_results_from_api.assert_called_once_with(missing_dates)
    mock_save_results_to_db.assert_called_once()


def test_append_results_to_response(get_rates_use_case, mocker):
    results = [
        {"date": "2023-01-02", "rate": 1.34},
        {"date": "2023-01-03", "rate": 1.45},
    ]
    get_rates_use_case.response.results = []

    get_rates_use_case.append_results_to_response(results)

    assert len(get_rates_use_case.response.results) == 2
    assert get_rates_use_case.response.results == results


def test_append_currencies_to_response(get_rates_use_case, mocker: pytest_mock.MockerFixture):
    currencies = [
        {"name": "US Dollar", "code": "USD", "symbol": "$"},
        {"name": "Brazilian Real", "code": "BRL", "symbol": "$"},
        {"name": "Euro", "code": "EUR", "symbol": "$"},
        {"name": "Japanese Yene", "code": "JPY", "symbol": "$"},
    ]
    mock_repository = mocker.patch.object(get_rates_use_case, "_repository")
    mock_repository.get_currencies = mocker.Mock()
    mock_repository.get_currencies.return_value = [Currency(**currency) for currency in currencies]

    get_rates_use_case.append_currencies_to_response()

    assert get_rates_use_case.response.currencies.dict() == {
        "USD": {"name": "US Dollar", "code": "USD", "symbol": "$"},
        "BRL": {"name": "Brazilian Real", "code": "BRL", "symbol": "$"},
        "EUR": {"name": "Euro", "code": "EUR", "symbol": "$"},
        "JPY": {"name": "Japanese Yene", "code": "JPY", "symbol": "$"},
    }
    mock_repository.get_currencies.assert_called_once()
