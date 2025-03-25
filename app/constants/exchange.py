from enum import Enum


class ExchangeType(Enum):
    BASIC = 1
    PRO = 2


class ExchangeCurrencyCode(Enum):
    VND = 'VND'
    CNY = 'CNY'