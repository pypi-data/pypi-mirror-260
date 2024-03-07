from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.observable import send
from typing import Callable, TypedDict
from reactivex import compose, operators, Observable
from requests.models import PreparedRequest

GetWithdrawalMethodsResult = TypedDict("GetWithdrawalMethodsResult", {"network": str, "asset": str, "minimum": str, "method": str})


def get_withdrawal_methods_request(*, asset: str = "", aclass: str = "", network: str = ""):
    """
    Get withdrawal methods
    :return:
    """
    data = {}
    if asset:
        data["asset"] = asset
    if network:
        data["network"] = network
    if aclass:
        data["aclass"] = aclass
    return prepare_private("/0/private/WithdrawMethods", data=data)


def get_withdrawal_methods_result() -> Callable[[Observable[PreparedRequest]], Observable[list[GetWithdrawalMethodsResult]]]:
    return compose(
        operators.flat_map(send),
        operators.map(lambda x: x.json()),
        operators.map(lambda x: x["result"]),
    )
