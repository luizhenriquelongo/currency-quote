from datetime import date
from typing import List
from urllib.parse import urlencode

import requests

from currencies.schemas import (
    CurrencySchema,
    GetRatesAPIResponseSchema,
)


class VATComplyAPI:
    BASE_URL: str = "https://api.vatcomply.com"

    def get_rates(
        self, base_currency: str = "USD", rates_date: str = date.today().strftime("%Y-%m-%d")
    ) -> GetRatesAPIResponseSchema | None:
        query_params = {"base": base_currency, "date": rates_date}
        url = self.build_url(path="/rates", query_params=query_params)
        raw_response = requests.get(url)

        try:
            raw_response.raise_for_status()

        except requests.HTTPError:
            return None

        return GetRatesAPIResponseSchema(**raw_response.json())

    def get_currencies(self) -> List[CurrencySchema] | None:
        url = self.build_url(path="/currencies")
        raw_response = requests.get(url)

        try:
            raw_response.raise_for_status()

        except requests.HTTPError:
            return None

        response = raw_response.json()

        return [CurrencySchema(name=value["name"], code=key, symbol=value["symbol"]) for key, value in response.items()]

    def build_url(self, path: str, query_params: dict | None = None) -> str:
        if path.startswith("/"):
            path = path[1:]

        url = f"{self.BASE_URL}/{path}"

        if query_params is None:
            return url

        encoded_params = urlencode(query_params)
        return url + f"?{encoded_params}"
