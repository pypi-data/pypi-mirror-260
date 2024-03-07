from typing import TypedDict
from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result

ExtendedBalance = TypedDict("ExtendedBalance", {"balance": str, "hold_trade": str})
GetExtendedBalanceResult = dict[str, ExtendedBalance]


def get_extended_balance_request():
    """
    Get extended balances
    :return:
    """
    return prepare_private(url="/0/private/BalanceEx")


def get_extended_balance_result():
    return send_and_map_to_result(GetExtendedBalanceResult)
