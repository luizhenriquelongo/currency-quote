from drf_spectacular.utils import OpenApiExample

CurrenciesFlagOn = OpenApiExample(
    "Currencies Flag On",
    media_type="application/json",
    status_codes=[200],
    response_only=True,
    value={
        "results": [
            {
                "date": "2020-02-20",
                "base": "USD",
                "rates": {
                    "EUR": "0.9267840593141800",
                    "USD": "1.0000000000000000",
                    "BRL": "4.3874884151992600",
                    "JPY": "112.0111214087120000",
                },
            },
            {
                "date": "2020-02-21",
                "base": "USD",
                "rates": {
                    "EUR": "0.9258401999814830",
                    "USD": "1.0000000000000000",
                    "BRL": "4.4023701509119500",
                    "JPY": "111.9896305897600000",
                },
            },
            {
                "date": "2020-02-24",
                "base": "USD",
                "rates": {
                    "EUR": "0.9243852837862820",
                    "USD": "1.0000000000000000",
                    "BRL": "4.3884266962470000",
                    "JPY": "111.4069144019230000",
                },
            },
            {
                "date": "2020-02-25",
                "base": "USD",
                "rates": {
                    "EUR": "0.9225092250922510",
                    "USD": "1.0000000000000000",
                    "BRL": "4.3882841328413300",
                    "JPY": "110.6273062730630000",
                },
            },
            {
                "date": "2020-02-26",
                "base": "USD",
                "rates": {
                    "EUR": "0.9195402298850580",
                    "USD": "1.0000000000000000",
                    "BRL": "4.3899770114942500",
                    "JPY": "110.4643678160920000",
                },
            },
        ],
        "currencies": {
            "EUR": {"name": "Euro", "code": "EUR", "symbol": "€"},
            "USD": {"name": "US Dollar", "code": "USD", "symbol": "$"},
            "BRL": {"name": "Brazilian Real", "code": "BRL", "symbol": "R$"},
            "JPY": {"name": "Japanese Yen", "code": "JPY", "symbol": "¥"},
        },
    },
)

CurrenciesFlagOff = OpenApiExample(
    "Currencies Flag Off",
    media_type="application/json",
    status_codes=[200],
    response_only=True,
    value={
        "results": [
            {
                "date": "2020-02-20",
                "base": "USD",
                "rates": {
                    "EUR": "0.9267840593141800",
                    "USD": "1.0000000000000000",
                    "BRL": "4.3874884151992600",
                    "JPY": "112.0111214087120000",
                },
            },
            {
                "date": "2020-02-21",
                "base": "USD",
                "rates": {
                    "EUR": "0.9258401999814830",
                    "USD": "1.0000000000000000",
                    "BRL": "4.4023701509119500",
                    "JPY": "111.9896305897600000",
                },
            },
            {
                "date": "2020-02-24",
                "base": "USD",
                "rates": {
                    "EUR": "0.9243852837862820",
                    "USD": "1.0000000000000000",
                    "BRL": "4.3884266962470000",
                    "JPY": "111.4069144019230000",
                },
            },
            {
                "date": "2020-02-25",
                "base": "USD",
                "rates": {
                    "EUR": "0.9225092250922510",
                    "USD": "1.0000000000000000",
                    "BRL": "4.3882841328413300",
                    "JPY": "110.6273062730630000",
                },
            },
            {
                "date": "2020-02-26",
                "base": "USD",
                "rates": {
                    "EUR": "0.9195402298850580",
                    "USD": "1.0000000000000000",
                    "BRL": "4.3899770114942500",
                    "JPY": "110.4643678160920000",
                },
            },
        ]
    },
)
