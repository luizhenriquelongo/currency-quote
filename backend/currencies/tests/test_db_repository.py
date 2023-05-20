import datetime
from typing import Dict

import pytest
from _decimal import Decimal

from currencies.db_repository import DBRepository
from currencies.models import (
    Currency,
    ExchangeRate,
)


@pytest.fixture
def mock_exchange_rate_model(mocker):
    def create_mock_exchange_rate(date):
        exchange_rate = mocker.Mock(spec=ExchangeRate)
        exchange_rate.date = date
        return exchange_rate

    return create_mock_exchange_rate


@pytest.fixture
def mock_currency_model(mocker):
    def create_mock_currency(code):
        currency = mocker.Mock(spec=Currency)
        currency.code = code
        return currency

    return create_mock_currency


@pytest.fixture
def db_repository():
    return DBRepository()


@pytest.fixture
def currencies() -> Dict[str, Currency]:
    usd_currency = Currency.objects.create(name="US Dollar", code="USD", symbol="$")
    brl_currency = Currency.objects.create(name="Brazilian Real", code="BRL", symbol="R$")
    eur_currency = Currency.objects.create(name="Euro", code="EUR", symbol="€")
    return {
        usd_currency.code: usd_currency,
        brl_currency.code: brl_currency,
        eur_currency.code: eur_currency,
    }


@pytest.mark.django_db
def test_filter_rates_by_date_range(db_repository, currencies):
    exchange_rate1 = ExchangeRate.objects.create(
        date=datetime.date(2023, 1, 10), base_currency=currencies["USD"], currency=currencies["USD"], rate=Decimal(1)
    )
    exchange_rate2 = ExchangeRate.objects.create(
        date=datetime.date(2023, 1, 10),
        base_currency=currencies["USD"],
        currency=currencies["BRL"],
        rate=Decimal("5.2"),
    )
    exchange_rate3 = ExchangeRate.objects.create(
        date=datetime.date(2023, 1, 15), base_currency=currencies["USD"], currency=currencies["USD"], rate=Decimal(1)
    )
    exchange_rate4 = ExchangeRate.objects.create(
        date=datetime.date(2023, 2, 1), base_currency=currencies["USD"], currency=currencies["USD"], rate=Decimal(1)
    )

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 1, 31)

    result = db_repository.filter_rates_by_date_range(start_date, end_date)

    assert len(result) == 3
    assert exchange_rate1 in result
    assert exchange_rate2 in result
    assert exchange_rate3 in result
    assert exchange_rate4 not in result


@pytest.mark.django_db
def test_get_currencies(db_repository, currencies):
    result = db_repository.get_currencies(["USD", "EUR"])

    assert len(result) == 2
    assert currencies["USD"] in result
    assert currencies["EUR"] in result
    assert currencies["BRL"] not in result


@pytest.mark.django_db
def test_get_currencies_for_an_unavailable_currency(db_repository, currencies):
    result = db_repository.get_currencies(["USD", "EUR", "JPY"])

    assert len(result) == 2
    assert currencies["USD"] in result
    assert currencies["EUR"] in result
    assert currencies["BRL"] not in result
