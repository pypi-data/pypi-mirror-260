import dataclasses
from enum import Enum
from typing import Callable, Literal, Optional, TypedDict

from reactivex import Observable
from requests import PreparedRequest

from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result
from .add_order import AddOrderRequest, OrderType, OrderSide, AddOrderResult, OrderDescr

@dataclasses.dataclass
class AddOrderBatchRequest:
    pair: str
    orders: list[AddOrderRequest]
    
    def as_dict(self):
        return {
            "pair": self.pair,
            "orders": [order.as_dict() for order in self.orders]
        }


def add_order_request(request: AddOrderBatchRequest):
    """
    Get open orders
    :return:
    """
    data = request.as_dict()
    return prepare_private(url="/0/private/AddOrderBatch", data=data)

AddOrderBatchResult = TypedDict("AddOrderBatchResult", {"orders": dict[str, AddOrderResult]})

def add_order_result() -> Callable[[Observable[PreparedRequest]], Observable[AddOrderBatchResult]]:
    return send_and_map_to_result(dict)  # type: ignore
