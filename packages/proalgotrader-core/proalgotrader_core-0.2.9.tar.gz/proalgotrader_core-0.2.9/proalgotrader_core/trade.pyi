from _typeshed import Incomplete
from proalgotrader_core.algorithm import Algorithm as Algorithm
from proalgotrader_core.broker_symbol import BrokerSymbol as BrokerSymbol
from proalgotrader_core.protocols.enums.position_type import PositionType as PositionType
from typing import Any, Dict

class Trade:
    id: Incomplete
    position_id: Incomplete
    market_type: Incomplete
    position_type: Incomplete
    order_type: Incomplete
    product_type: Incomplete
    quantities: Incomplete
    enter_price: Incomplete
    exit_price: Incomplete
    status: Incomplete
    tags: Incomplete
    created_at: Incomplete
    updated_at: Incomplete
    algorithm: Incomplete
    broker_symbol: Incomplete
    def __init__(self, position_info: Dict[str, Any], broker_symbol: BrokerSymbol, algorithm: Algorithm) -> None: ...
    @property
    def is_buy(self) -> bool: ...
    @property
    def is_sell(self) -> bool: ...
    @property
    def pnl(self) -> float: ...
    @property
    def pnl_percent(self) -> float: ...
    async def initialize(self) -> None: ...
