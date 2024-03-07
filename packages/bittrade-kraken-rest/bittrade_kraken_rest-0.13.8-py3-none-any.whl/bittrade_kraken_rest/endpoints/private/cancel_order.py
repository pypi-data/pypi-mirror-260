from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result
import dataclasses

@dataclasses.dataclass
class CancelOrderResult:
    count: int

def cancel_order_request(*, txid: str | int):
    """
    Cancel an order
    :return:
    """
    return prepare_private(url="/0/private/CancelOrder", data={"txid": txid})


def cancel_order_result():
    return send_and_map_to_result(CancelOrderResult)
