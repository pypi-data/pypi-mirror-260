from _typeshed import Incomplete
from datetime import timedelta
from fyers_apiv3.FyersWebsocket.data_ws import FyersDataSocket as FyersDataSocket
from fyers_apiv3.fyersModel import FyersModel as FyersModel
from proalgotrader_core.algo_session import AlgoSession as AlgoSession
from proalgotrader_core.api import Api as Api
from proalgotrader_core.bar import Bar as Bar
from proalgotrader_core.broker_symbol import BrokerSymbol as BrokerSymbol
from proalgotrader_core.tick import Tick as Tick
from proalgotrader_core.token_managers.fyers_token_manager import FyersTokenManager as FyersTokenManager
from typing import Any, Dict, List

class DataManager:
    api: Incomplete
    algo_session: Incomplete
    token_manager: Incomplete
    ws_client: Incomplete
    http_client: Incomplete
    resolutions: Incomplete
    subscribers: Incomplete
    def __init__(self, api: Api, algo_session: AlgoSession) -> None: ...
    def initialize(self) -> None: ...
    def start_connection(self) -> None: ...
    def close_connection(self) -> None: ...
    def on_message(self, message: Dict[str, Any]) -> None: ...
    def subscribe(self, broker_symbol: BrokerSymbol) -> None: ...
    def fetch_quotes(self, broker_symbol: BrokerSymbol) -> Tick: ...
    def fetch_bars(self, broker_symbol: BrokerSymbol, timeframe: timedelta, fetch_from: int, fetch_to: int) -> List[Bar]: ...
