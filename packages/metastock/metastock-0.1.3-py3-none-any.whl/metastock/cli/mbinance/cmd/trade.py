from dependency_injector.wiring import inject, Provide

from metastock.modules.core.util.exit_event import hold
from metastock.modules.mbinance.um.trade.one_billion import OneBillion


@inject
def trade_cmd(pair: str, um_app: OneBillion = Provide["mbinance.um.one_billion"]):
    um_app.start(pair=pair)

    hold()

    um_app.stop()
