from proalgotrader_core.algo_session import AlgoSession as AlgoSession
from proalgotrader_core.api import Api as Api
from proalgotrader_core.brokers.base_broker import BaseBroker as BaseBroker
from proalgotrader_core.brokers.providers import providers as providers

class BrokerManager:
    @staticmethod
    def get_instance(api: Api, algo_session: AlgoSession) -> BaseBroker: ...
