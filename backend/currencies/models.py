from _decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, null=False, blank=False, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    symbol = models.CharField(max_length=3, null=False, blank=False)


class ExchangeRate(models.Model):
    date = models.DateField(null=False, blank=False)
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="base_rates")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="exchange_rates")
    rate = models.DecimalField(decimal_places=16, max_digits=20)

    class Meta:
        unique_together = (
            "date",
            "base_currency",
            "currency",
        )

    def clean(self):
        super().clean()
        if self.base_currency == self.currency and self.rate != Decimal(1):
            raise ValidationError(f"Comparison between equal currencies should be 1, not {self.rate}.")
