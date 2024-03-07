from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.observable import send
from typing import Callable, TypedDict
from reactivex import compose, operators, Observable
from requests.models import PreparedRequest

GetWithdrawalAddressesResult = TypedDict("GetWithdrawalAddressesResult", {"key": str, "asset": str, "address": str, "verified": bool, "method": str})


def get_withdrawal_addresses_request(*, asset: str = "", key: str = ""):
    """
    Get withdrawal addresses
    :return:
    """
    data = {}
    if asset:
        data["asset"] = asset
    if key:
        data["key"] = key
    return prepare_private("/0/private/WithdrawAddresses", data=data)


def get_withdrawal_addresses_result() -> Callable[[Observable[PreparedRequest]], Observable[list[GetWithdrawalAddressesResult]]]:
    return compose(
        operators.flat_map(send),
        operators.map(lambda x: x.json()),
        operators.map(lambda x: x["result"]),
    )
