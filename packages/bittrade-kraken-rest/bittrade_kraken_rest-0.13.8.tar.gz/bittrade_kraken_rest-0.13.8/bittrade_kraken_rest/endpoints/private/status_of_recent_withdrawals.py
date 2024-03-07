from datetime import datetime
from decimal import Decimal
from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.observable import send
from typing import Callable, Literal, TypedDict
from reactivex import compose, operators, Observable
from requests.models import PreparedRequest

from bittrade_kraken_rest.connection.result import send_and_map_to_result

GetStatusOfRecentWithdrawalsResult = TypedDict("GetStatusOfRecentWithdrawalsResult", {"aclass": Literal["currency", "asset", "forex"], "asset": str, "refid": str, "txid": str, "info": str, "amount": str, "fee": str, "time": int, "status": Literal["Initial", "Pending", "Success", "Settled", "Failure"], "status-prop": Literal["return", "onhold"]})


def get_status_of_recent_withdrawals_request(*, asset: str, aclass: Literal["currency", "asset", "forex"] = "currency", method: str = "", start: datetime | None = None, end: datetime | None = None, cursor: str = "", limit: int = 25):
    """
    Get status of recent withdrawals
    :return:
    """
    data: dict[str, str | int] = {
        "asset": asset,
        "aclass": aclass,
        "limit": limit
    }
    if method:
        data["method"] = method
    if start:
        data["start"] = int(start.timestamp())
    if end:
        data["end"] = int(end.timestamp())
    if cursor:
        data["cursor"] = cursor
    return prepare_private("/0/private/WithdrawStatus", data=data)


def get_status_of_recent_withdrawals_result() -> Callable[[Observable[PreparedRequest]], Observable[list[GetStatusOfRecentWithdrawalsResult]]]:
    return compose(
        operators.flat_map(send),
        operators.map(lambda x: x.json()),
        operators.map(lambda x: x["result"]),
    )
