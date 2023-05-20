import abc
import datetime
from typing import List

from currencies.models import (
    Currency,
    ExchangeRate,
)


class RepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def filter_rates_by_date_range(self, start_date: datetime.date, end_date: datetime.date) -> List[ExchangeRate]:
        ...

    @abc.abstractmethod
    def get_currencies(self, currencies: List[str]) -> List[Currency]:
        ...


class DBRepository(RepositoryInterface):
    def filter_rates_by_date_range(self, start_date: datetime.date, end_date: datetime.date) -> List[ExchangeRate]:
        queryset = ExchangeRate.objects.filter(
            date__gte=start_date,
            date__lte=end_date,
        )
        return list(queryset)

    def get_currencies(self, currencies: List[str]) -> List[Currency]:
        queryset = Currency.objects.filter(code__in=currencies)
        return list(queryset)
