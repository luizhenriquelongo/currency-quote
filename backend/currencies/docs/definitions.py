CurrencySchema = {
    "properties": {
        "code": {"title": "Code", "type": "string"},
        "name": {"title": "Name", "type": "string"},
        "symbol": {"title": "Symbol", "type": "string"},
    },
    "required": ["name", "code", "symbol"],
    "title": "CurrencySchema",
    "type": "object",
}

CurrenciesSchema = {
    "properties": {
        "BRL": CurrencySchema,
        "EUR": CurrencySchema,
        "JPY": CurrencySchema,
        "USD": CurrencySchema,
    },
    "required": ["EUR", "USD", "BRL", "JPY"],
    "title": "CurrenciesSchema",
    "type": "object",
}

RatesSchema = {
    "properties": {
        "BRL": {"type": "number"},
        "EUR": {"type": "number"},
        "JPY": {"type": "number"},
        "USD": {"type": "number"},
    },
    "required": ["EUR", "USD", "BRL", "JPY"],
    "title": "RatesSchema",
    "type": "object",
}

ResponseObjectSchema = {
    "properties": {
        "base": {"title": "Base", "type": "string"},
        "date": {"title": "Date", "type": "string"},
        "rates": RatesSchema,
    },
    "required": ["date", "base", "rates"],
    "title": "ResponseObjectSchema",
    "type": "object",
}

Response200Schema = {
    "properties": {
        "results": {
            "default": [],
            "items": ResponseObjectSchema,
            "title": "Results",
            "type": "array",
        },
        "currencies": CurrenciesSchema,
    },
    "title": "Response",
    "type": "object",
}
