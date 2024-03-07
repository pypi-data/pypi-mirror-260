import dataclasses
from enum import Enum
from typing import Literal, Optional, TypedDict

from pydantic.dataclasses import dataclass

from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result
from bittrade_kraken_rest.models.order import Order

class OrderType(str, Enum):
    market = "market"
    limit = "limit"
    stop_loss = "stop-loss"
    take_profit = "take-profit"
    stop_loss_limit = "stop-loss-limit"
    take_profit_limit = "take-profit-limit"
    settle_position = "settle-position"


class OrderSide(str, Enum):
    buy = "buy"
    sell = "sell"

OrderDescr = TypedDict("OrderDescr", {"order": str})
AddOrderResult = TypedDict("AddOrderResult", {"descr": OrderDescr, "txid": list[str]})

@dataclasses.dataclass
class AddOrderRequest:
    ordertype: OrderType
    type: OrderSide
    price: str
    volume: str
    pair: str
    oflags: str = ""
    displayvol: str = ""
    price2: str = ""
    reqid: Optional[int] = None
    userref: str = "1"

    def as_dict(self):
        data = dataclasses.asdict(self)
        data["ordertype"] = data["ordertype"].value
        data["type"] = data["type"].value
        if not self.price2:
            del data["price2"]
        if not self.displayvol:
            del data["displayvol"]
        if not self.oflags:
            del data["oflags"]
        return {k: v for k, v in data.items() if v is not None}


def add_order_request(request: AddOrderRequest):
    """
    Get open orders
    :return:
    """
    data = request.as_dict()
    return prepare_private(url="/0/private/AddOrder", data=data)


def add_order_result():
    return send_and_map_to_result(AddOrderResult)
