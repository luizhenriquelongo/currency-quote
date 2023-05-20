import datetime
from collections import defaultdict
from typing import List

from rest_framework import serializers

import utils
from currencies.models import (
    Currency,
    ExchangeRate,
)
from currencies.schemas import (
    GetRatesAPIResponseSchema,
)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class ExchangeRateListSerializer(serializers.ListSerializer):
    def to_schemas(self) -> List[GetRatesAPIResponseSchema]:
        response = defaultdict(lambda: {"rates": {}})
        for result in self.data:
            date = result["date"]
            base_currency_code = result["base_currency"]["code"]
            key = str(frozenset([date, base_currency_code]))

            response[key].update({"date": date, "base": result["base_currency"]["code"]})

            response[key]["rates"][result["currency"]["code"]] = result["rate"]

        return [GetRatesAPIResponseSchema.parse_obj(item) for item in response.values()]


class ExchangeRateSerializer(serializers.ModelSerializer):
    base_currency = CurrencySerializer()
    currency = CurrencySerializer()

    class Meta:
        model = ExchangeRate
        fields = "__all__"
        list_serializer_class = ExchangeRateListSerializer


class QueryParamsSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True, help_text="Start date of the exchange rates (YYYY-MM-DD)")
    end_date = serializers.DateField(required=True, help_text="End date of the exchange rates (YYYY-MM-DD)")
    currencies = serializers.BooleanField(
        default=False, required=False, help_text="A flag to return a description of each currency on response"
    )

    def validate(self, attrs):
        self.validate_fields(attrs)
        return attrs

    def validate_fields(self, attrs):
        start_dt = attrs.get("start_date")
        end_dt = attrs.get("end_date")

        if end_dt < start_dt:
            raise serializers.ValidationError(detail="'end_date' must be later than 'start_date'")

        self.validate_dates_range(start_dt, end_dt)

    def validate_dates_range(self, start_date: datetime.datetime.date, end_date: datetime.datetime.date):
        business_days = 0
        current_date = start_date
        while current_date <= end_date:
            if utils.is_business_day(current_date):
                business_days += 1
            current_date += datetime.timedelta(days=1)

        if business_days > 5:
            raise serializers.ValidationError(detail="The selected date range should not exceed 5 business days.")
