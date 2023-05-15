from _decimal import Decimal

from pydantic import BaseModel


class CurrencySchema(BaseModel):
    name: str
    code: str
    symbol: str


class RatesSchema(BaseModel):
    EUR: Decimal
    USD: Decimal
    BRL: Decimal
    JPY: Decimal


class GetRatesAPIResponseSchema(BaseModel):
    date: str
    base: str
    rates: RatesSchema
