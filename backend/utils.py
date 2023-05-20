from datetime import (
    datetime,
    timedelta,
)
from typing import List

import holidays


def isodate_to_datetime(isodate: str) -> datetime:
    date_format = "%Y-%m-%d"
    return datetime.strptime(isodate, date_format)


def is_business_day(date: datetime.date) -> bool:
    # Here we are using the same calendar as European Central Bank for consistency since the VATComplyAPI collects data
    # from the European Central Bank.
    holiday_dates = holidays.financial_holidays("ECB", observed=True)
    return date.weekday() not in holiday_dates.weekend and date not in holiday_dates


def get_dates_between(start_date: str, end_date: str) -> List[str]:
    dates = []

    start_dt = isodate_to_datetime(start_date).date()
    end_dt = isodate_to_datetime(end_date).date()

    current_dt = start_dt
    while current_dt <= end_dt:
        if is_business_day(current_dt):
            dates.append(current_dt.isoformat())
        current_dt += timedelta(days=1)

    return dates
