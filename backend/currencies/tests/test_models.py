import pytest
from _decimal import Decimal
from django.core.exceptions import ValidationError

from currencies.models import (
    Currency,
    RateQuote,
)


@pytest.fixture
def usd_currency():
    return Currency.objects.create(name="US Dollar", representation="USD", symbol="$")


@pytest.mark.django_db
class TestRateQuoteModel:
    def test_clean_method(self, usd_currency):
        brl_currency = Currency.objects.create(name="Brazilian Real", representation="BRL", symbol="R$")

        quote = RateQuote(
            date="2023-05-15", base_currency=usd_currency, rate_currency=brl_currency, rate_value=Decimal("5.2")
        )
        quote.full_clean()
        quote.save()

        assert RateQuote.objects.filter(pk=quote.pk).exists()

    def test_if_clean_method_raises_exception(self, usd_currency):
        with pytest.raises(ValidationError):
            quote = RateQuote(
                date="2023-05-15", base_currency=usd_currency, rate_currency=usd_currency, rate_value=Decimal("0.5")
            )
            quote.full_clean()
            quote.save()

        assert len(RateQuote.objects.all()) == 0
