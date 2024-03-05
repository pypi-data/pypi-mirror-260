from metastock.modules.trade.error import NotSupportConfigType
from metastock.modules.trade.strategy.signals.output_schema import SIGNAL_OUTPUT_SCHEMA_V1_NAME
from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract


class SimpleSqzMomSignal(SignalAbstract):
    name = 'simple_sqz_mom_signal'

    def support_output_versions(self) -> list[str]:
        return [SIGNAL_OUTPUT_SCHEMA_V1_NAME]

    def get_output(self, version = '@signal/output/v1'):
        if version == SIGNAL_OUTPUT_SCHEMA_V1_NAME:
            return self._get_output_v1()

        raise NotSupportConfigType(f"Not support get output for version {version}")

    def _get_output_v1(self):
        pass
