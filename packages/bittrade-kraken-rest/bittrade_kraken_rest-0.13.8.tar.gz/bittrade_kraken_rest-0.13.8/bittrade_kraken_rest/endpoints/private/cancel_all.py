from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result
import dataclasses

@dataclasses.dataclass
class CancelAllResult:
    count: int

def cancel_all_request():
    """
    Cancel all orders
    :return:
    """
    return prepare_private(url="/0/private/CancelAll")


def cancel_all_result():
    return send_and_map_to_result(CancelAllResult)
