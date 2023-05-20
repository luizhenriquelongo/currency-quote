import abc
from datetime import date
from typing import List

from currencies.models import (
    Currency,
    ExchangeRate,
)
from currencies.schemas import (
    CurrencySchema,
    GetRatesAPIResponseSchema,
)


class APIInterface(abc.ABC):
    @abc.abstractmethod
    def get_rates(
        self,
        rates_date: str = date.today().isoformat(),
        *,
        base_currency: str = "USD",
    ) -> GetRatesAPIResponseSchema | None:
        ...

    @abc.abstractmethod
    def get_currencies(self) -> List[CurrencySchema] | None:
        ...


class RepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def filter_rates_by_date_range(self, start_date: date, end_date: date) -> List[ExchangeRate]:
        ...

    @abc.abstractmethod
    def get_currencies(self, currencies: List[str]) -> List[Currency]:
        ...
