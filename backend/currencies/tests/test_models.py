import pytest
from _decimal import Decimal
from django.core.exceptions import ValidationError

from currencies.models import (
    Currency,
    ExchangeRate,
)


@pytest.fixture
def usd_currency():
    return Currency.objects.create(name="US Dollar", code="USD", symbol="$")


@pytest.mark.django_db
class TestRateQuoteModel:
    def test_clean_method(self, usd_currency):
        brl_currency = Currency.objects.create(name="Brazilian Real", code="BRL", symbol="R$")

        quote = ExchangeRate(date="2023-05-15", base_currency=usd_currency, currency=brl_currency, rate=Decimal("5.2"))
        quote.full_clean()
        quote.save()

        assert ExchangeRate.objects.filter(pk=quote.pk).exists()

    def test_if_clean_method_raises_exception(self, usd_currency):
        with pytest.raises(ValidationError):
            quote = ExchangeRate(
                date="2023-05-15", base_currency=usd_currency, currency=usd_currency, rate=Decimal("0.5")
            )
            quote.full_clean()
            quote.save()

        assert len(ExchangeRate.objects.all()) == 0
