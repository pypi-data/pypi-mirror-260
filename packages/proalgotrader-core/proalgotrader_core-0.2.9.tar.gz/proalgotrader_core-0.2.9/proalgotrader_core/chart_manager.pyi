from _typeshed import Incomplete
from datetime import timedelta
from proalgotrader_core.broker_symbol import BrokerSymbol as BrokerSymbol
from proalgotrader_core.brokers.base_broker import BaseBroker as BaseBroker
from proalgotrader_core.chart import Chart as Chart
from typing import List

class ChartManager:
    broker_manager: Incomplete
    api: Incomplete
    algo_session: Incomplete
    def __init__(self, broker_manager: BaseBroker) -> None: ...
    @property
    def charts(self) -> List[Chart]: ...
    async def get_chart(self, broker_symbol: BrokerSymbol, timeframe: timedelta) -> Chart | None: ...
    async def register_chart(self, broker_symbol: BrokerSymbol, timeframe: timedelta) -> Chart: ...
