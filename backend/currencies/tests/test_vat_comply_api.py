from datetime import date

import pytest
import responses
from _decimal import Decimal

from currencies.schemas import CurrencySchema
from currencies.vat_comply_api import VATComplyAPI


@pytest.fixture
def vat_comply_api() -> VATComplyAPI:
    return VATComplyAPI()


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def mocked_currencies_endpoint_response() -> dict:
    return {
        "EUR": {"name": "Euro", "symbol": "€"},
        "USD": {"name": "US Dollar", "symbol": "$"},
        "JPY": {"name": "Japanese Yen", "symbol": "¥"},
        "BGN": {"name": "Bulgarian Lev", "symbol": "BGN"},
        "CZK": {"name": "Czech Koruna", "symbol": "CZK"},
        "DKK": {"name": "Danish Krone", "symbol": "DKK"},
        "GBP": {"name": "British Pound", "symbol": "£"},
        "HUF": {"name": "Hungarian Forint", "symbol": "HUF"},
        "PLN": {"name": "Polish Zloty", "symbol": "PLN"},
        "RON": {"name": "Romanian Leu", "symbol": "RON"},
        "SEK": {"name": "Swedish Krona", "symbol": "SEK"},
        "CHF": {"name": "Swiss Franc", "symbol": "CHF"},
        "ISK": {"name": "Icelandic Króna", "symbol": "ISK"},
        "NOK": {"name": "Norwegian Krone", "symbol": "NOK"},
        "HRK": {"name": "Croatian Kuna", "symbol": "HRK"},
        "RUB": {"name": "Russian Ruble", "symbol": "RUB"},
        "TRY": {"name": "Turkish Lira", "symbol": "TRY"},
        "AUD": {"name": "Australian Dollar", "symbol": "A$"},
        "BRL": {"name": "Brazilian Real", "symbol": "R$"},
        "CAD": {"name": "Canadian Dollar", "symbol": "CA$"},
        "CNY": {"name": "Chinese Yuan", "symbol": "CN¥"},
        "HKD": {"name": "Hong Kong Dollar", "symbol": "HK$"},
        "IDR": {"name": "Indonesian Rupiah", "symbol": "IDR"},
        "ILS": {"name": "Israeli New Shekel", "symbol": "₪"},
        "INR": {"name": "Indian Rupee", "symbol": "₹"},
        "KRW": {"name": "South Korean Won", "symbol": "₩"},
        "MXN": {"name": "Mexican Peso", "symbol": "MX$"},
        "MYR": {"name": "Malaysian Ringgit", "symbol": "MYR"},
        "NZD": {"name": "New Zealand Dollar", "symbol": "NZ$"},
        "PHP": {"name": "Philippine Piso", "symbol": "PHP"},
        "SGD": {"name": "Singapore Dollar", "symbol": "SGD"},
        "THB": {"name": "Thai Baht", "symbol": "THB"},
        "ZAR": {"name": "South African Rand", "symbol": "ZAR"},
    }


@pytest.fixture
def mocked_rates_endpoint_response() -> dict:
    return {
        "date": date.today().strftime("%Y-%m-%d"),
        "base": "USD",
        "rates": {
            "EUR": 0.9272137227630969,
            "USD": 1,
            "JPY": 108.57672693555864,
            "BGN": 1.813444598980065,
            "CZK": 25.534538711172928,
            "DKK": 6.925266573945294,
            "GBP": 0.8145572554473806,
            "HUF": 338.5720908669448,
            "PLN": 4.243393602225313,
            "RON": 4.479091330551692,
            "SEK": 10.154844691701436,
            "CHF": 0.9779323133982383,
            "ISK": 144.36717663421416,
            "NOK": 10.443022716736207,
            "HRK": 7.074640704682429,
            "RUB": 76.78025034770515,
            "TRY": 6.703384330088085,
            "AUD": 1.6693555864626797,
            "BRL": 5.275197032916087,
            "CAD": 1.4185442744552619,
            "CNY": 7.09095966620306,
            "HKD": 7.753824756606399,
            "IDR": 16614.44598980065,
            "ILS": 3.6408901251738524,
            "INR": 76.23180343069076,
            "KRW": 1235.8089939731108,
            "MXN": 24.614742698191932,
            "MYR": 4.358460825220213,
            "NZD": 1.7082058414464534,
            "PHP": 50.815948076031525,
            "SGD": 1.4361613351877607,
            "THB": 33.009735744089014,
            "ZAR": 18.789244320815946,
        },
    }


class TestVATComplyAPI:
    def test_build_url_with_query_params(self, vat_comply_api: VATComplyAPI):
        url = vat_comply_api.build_url(path="/random_path", query_params={"arg1": "1", "arg2": "2"})
        assert url == f"{vat_comply_api.BASE_URL}/random_path?arg1=1&arg2=2"

    def test_build_url_without_query_params(self, vat_comply_api: VATComplyAPI):
        url = vat_comply_api.build_url(path="/random_path")
        assert url == f"{vat_comply_api.BASE_URL}/random_path"

    def test_build_url_without_path_slash(self, vat_comply_api: VATComplyAPI):
        url = vat_comply_api.build_url(path="random_path")
        assert url == f"{vat_comply_api.BASE_URL}/random_path"

    def test_get_currencies(self, vat_comply_api: VATComplyAPI, mocked_responses, mocked_currencies_endpoint_response):
        mocked_responses.get(
            f"{vat_comply_api.BASE_URL}/currencies",
            json=mocked_currencies_endpoint_response,
            status=200,
            content_type="application/json",
        )
        currencies = vat_comply_api.get_currencies()
        assert currencies == [
            CurrencySchema(name="Euro", code="EUR", symbol="€"),
            CurrencySchema(name="US Dollar", code="USD", symbol="$"),
            CurrencySchema(name="Japanese Yen", code="JPY", symbol="¥"),
            CurrencySchema(name="Bulgarian Lev", code="BGN", symbol="BGN"),
            CurrencySchema(name="Czech Koruna", code="CZK", symbol="CZK"),
            CurrencySchema(name="Danish Krone", code="DKK", symbol="DKK"),
            CurrencySchema(name="British Pound", code="GBP", symbol="£"),
            CurrencySchema(name="Hungarian Forint", code="HUF", symbol="HUF"),
            CurrencySchema(name="Polish Zloty", code="PLN", symbol="PLN"),
            CurrencySchema(name="Romanian Leu", code="RON", symbol="RON"),
            CurrencySchema(name="Swedish Krona", code="SEK", symbol="SEK"),
            CurrencySchema(name="Swiss Franc", code="CHF", symbol="CHF"),
            CurrencySchema(name="Icelandic Króna", code="ISK", symbol="ISK"),
            CurrencySchema(name="Norwegian Krone", code="NOK", symbol="NOK"),
            CurrencySchema(name="Croatian Kuna", code="HRK", symbol="HRK"),
            CurrencySchema(name="Russian Ruble", code="RUB", symbol="RUB"),
            CurrencySchema(name="Turkish Lira", code="TRY", symbol="TRY"),
            CurrencySchema(name="Australian Dollar", code="AUD", symbol="A$"),
            CurrencySchema(name="Brazilian Real", code="BRL", symbol="R$"),
            CurrencySchema(name="Canadian Dollar", code="CAD", symbol="CA$"),
            CurrencySchema(name="Chinese Yuan", code="CNY", symbol="CN¥"),
            CurrencySchema(name="Hong Kong Dollar", code="HKD", symbol="HK$"),
            CurrencySchema(name="Indonesian Rupiah", code="IDR", symbol="IDR"),
            CurrencySchema(name="Israeli New Shekel", code="ILS", symbol="₪"),
            CurrencySchema(name="Indian Rupee", code="INR", symbol="₹"),
            CurrencySchema(name="South Korean Won", code="KRW", symbol="₩"),
            CurrencySchema(name="Mexican Peso", code="MXN", symbol="MX$"),
            CurrencySchema(name="Malaysian Ringgit", code="MYR", symbol="MYR"),
            CurrencySchema(name="New Zealand Dollar", code="NZD", symbol="NZ$"),
            CurrencySchema(name="Philippine Piso", code="PHP", symbol="PHP"),
            CurrencySchema(name="Singapore Dollar", code="SGD", symbol="SGD"),
            CurrencySchema(name="Thai Baht", code="THB", symbol="THB"),
            CurrencySchema(name="South African Rand", code="ZAR", symbol="ZAR"),
        ]

    def test_get_currencies_with_500_api_return(self, vat_comply_api: VATComplyAPI, mocked_responses):
        mocked_responses.get(
            f"{vat_comply_api.BASE_URL}/currencies",
            status=500,
        )
        currencies = vat_comply_api.get_currencies()
        assert currencies is None

    def test_get_rates_with_default_params(
        self, vat_comply_api: VATComplyAPI, mocked_responses, mocked_rates_endpoint_response
    ):
        rate_date = date.today().strftime("%Y-%m-%d")
        mocked_rates_endpoint_response["date"] = rate_date
        mocked_responses.get(
            f"{vat_comply_api.BASE_URL}/rates?base=USD&date={rate_date}",
            match=(responses.matchers.query_param_matcher({"base": "USD", "date": rate_date}),),
            json=mocked_rates_endpoint_response,
            status=200,
            content_type="application/json",
        )

        response = vat_comply_api.get_rates()

        assert response.dict() == {
            "base": "USD",
            "date": rate_date,
            "rates": {
                "BRL": Decimal("5.275197032916087"),
                "EUR": Decimal("0.9272137227630969"),
                "JPY": Decimal("108.57672693555864"),
                "USD": Decimal("1"),
            },
        }

    def test_get_rates_with_brl_as_base(
        self, vat_comply_api: VATComplyAPI, mocked_responses, mocked_rates_endpoint_response
    ):
        base = "BRL"
        rate_date = date.today().strftime("%Y-%m-%d")

        mocked_rates_endpoint_response["base"] = base
        mocked_rates_endpoint_response["date"] = rate_date
        mocked_responses.get(
            f"{vat_comply_api.BASE_URL}/rates?base={base}&date={rate_date}",
            match=(responses.matchers.query_param_matcher({"base": base, "date": rate_date}),),
            json=mocked_rates_endpoint_response,
            status=200,
            content_type="application/json",
        )

        response = vat_comply_api.get_rates(base_currency=base)

        assert response.dict() == {
            "base": base,
            "date": rate_date,
            "rates": {
                "BRL": Decimal("5.275197032916087"),
                "EUR": Decimal("0.9272137227630969"),
                "JPY": Decimal("108.57672693555864"),
                "USD": Decimal("1"),
            },
        }

    def test_get_rates_with_different_date(
        self, vat_comply_api: VATComplyAPI, mocked_responses, mocked_rates_endpoint_response
    ):
        rate_date = "2020-02-20"

        mocked_rates_endpoint_response["date"] = rate_date
        mocked_responses.get(
            f"{vat_comply_api.BASE_URL}/rates?base=USD&date={rate_date}",
            match=(responses.matchers.query_param_matcher({"base": "USD", "date": rate_date}),),
            json=mocked_rates_endpoint_response,
            status=200,
            content_type="application/json",
        )

        response = vat_comply_api.get_rates(rates_date=rate_date)

        assert response.dict() == {
            "base": "USD",
            "date": rate_date,
            "rates": {
                "BRL": Decimal("5.275197032916087"),
                "EUR": Decimal("0.9272137227630969"),
                "JPY": Decimal("108.57672693555864"),
                "USD": Decimal("1"),
            },
        }

    def test_get_rates_with_400_api_return(self, vat_comply_api: VATComplyAPI, mocked_responses):
        rate_date = date.today().strftime("%Y-%m-%d")
        mocked_responses.get(
            f"{vat_comply_api.BASE_URL}/rates?base=USD&date={rate_date}",
            match=(responses.matchers.query_param_matcher({"base": "USD", "date": rate_date}),),
            status=400,
            content_type="application/json",
        )

        response = vat_comply_api.get_rates()
        assert response is None

    def test_get_rates_with_404_api_return(self, vat_comply_api: VATComplyAPI, mocked_responses):
        rate_date = date.today().strftime("%Y-%m-%d")
        mocked_responses.get(
            f"{vat_comply_api.BASE_URL}/rates?base=USD&date={rate_date}",
            match=(responses.matchers.query_param_matcher({"base": "USD", "date": rate_date}),),
            status=404,
            content_type="application/json",
        )

        response = vat_comply_api.get_rates()
        assert response is None

    def test_get_rates_with_500_api_return(self, vat_comply_api: VATComplyAPI, mocked_responses):
        rate_date = date.today().strftime("%Y-%m-%d")
        mocked_responses.get(
            f"{vat_comply_api.BASE_URL}/rates?base=USD&date={rate_date}",
            match=(responses.matchers.query_param_matcher({"base": "USD", "date": rate_date}),),
            status=500,
            content_type="application/json",
        )

        response = vat_comply_api.get_rates()
        assert response is None
