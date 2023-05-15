from _decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=3, null=False, blank=False)
    symbol = models.CharField(max_length=3, null=False, blank=False)


class RateQuote(models.Model):
    date = models.DateField(null=False, blank=False)
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="base_currency")
    rate_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="rate_currency")
    rate_value = models.DecimalField(decimal_places=16, max_digits=20)

    def clean(self):
        super().clean()
        if self.base_currency == self.rate_currency and self.rate_value != Decimal(1):
            raise ValidationError(f"Comparison between equal currencies should be 1, not {self.rate_value}.")
