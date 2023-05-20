from typing import (
    Dict,
    List,
)

from _decimal import Decimal
from django.conf import settings
from pydantic import (
    BaseModel,
    create_model,
)

import utils
from currencies.models import (
    Currency,
    ExchangeRate,
)


class CurrencySchema(BaseModel):
    name: str
    code: str
    symbol: str


RatesSchema = create_model("RatesSchema", **{field: (Decimal, ...) for field in settings.MAPPED_CURRENCIES})


class GetRatesAPIResponseSchema(BaseModel):
    date: str
    base: str
    rates: RatesSchema

    def to_db_model(self) -> List[ExchangeRate]:
        # Fetching the queryset to avoid multiple requests since querysets are lazy.
        currencies_list = list(Currency.objects.all())
        currencies_searchable_by_code: Dict[str, Currency] = {currency.code: currency for currency in currencies_list}
        base_currency = currencies_searchable_by_code.get(self.base)

        objects = [
            ExchangeRate(
                date=utils.isodate_to_datetime(self.date).date(),
                base_currency=base_currency,
                currency=currencies_searchable_by_code.get(currency_code),
                rate=getattr(self.rates, currency_code),
            )
            for currency_code in settings.MAPPED_CURRENCIES
        ]

        return objects


class RateResponse(BaseModel):
    currency: CurrencySchema
    rate: Decimal


RatesSchemaResponse = create_model(
    "RateSchemaResponse", **{field: (RateResponse, ...) for field in settings.MAPPED_CURRENCIES}
)


class GetRatesListFromDbAPIResponse(BaseModel):
    date: str
    base: CurrencySchema
    rates: RatesSchemaResponse


class QueryArgs(BaseModel):
    start_date: str | None
    end_date: str | None
    append_currencies: bool = False


CurrenciesSchema = create_model(
    "CurrenciesSchema", **{field: (CurrencySchema, ...) for field in settings.MAPPED_CURRENCIES}
)


class UseCaseResponse(BaseModel):
    results: List[GetRatesAPIResponseSchema] = []
    currencies: CurrenciesSchema | None
