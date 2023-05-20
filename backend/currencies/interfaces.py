import abc
from datetime import date
from typing import List

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
