from datetime import datetime
from typing import Literal, TypedDict

from pydantic.dataclasses import dataclass
from reactivex import Observable

from bittrade_kraken_rest.connection.observable import send_public
from bittrade_kraken_rest.connection.result import map_to_result


class TickerResultEntry(TypedDict):
    a: tuple[str, str, str]
    b: tuple[str, str, str]
    c: tuple[str, str, str]
    v: tuple[str, str, str]
    p: tuple[str, str, str]
    t: tuple[str, str, str]
    l: tuple[str, str]
    h: tuple[str, str]
    o: tuple[str, str]

TickerResult = dict[str, TickerResultEntry]


def ticker_response(pair: str):
    params = {"pair": pair or None}
    return send_public(url="/0/public/Ticker", params=params)


def ticker(pair: str='') -> Observable[TickerResult]:
    return ticker_response(pair).pipe(map_to_result(dict))


__all__ = [
    "ticker_response",
    "ticker",
    "TickerResult",
    "TickerResultEntry",
]
