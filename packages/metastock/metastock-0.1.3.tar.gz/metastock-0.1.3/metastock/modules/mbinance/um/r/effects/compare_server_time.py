from reactivex import compose, operators as ops

from metastock.modules.core.util.r.action import Action
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.rx_common import of_type
from metastock.modules.mbinance.um.r.actions.get_time_diff import get_time_diff_action
from metastock.modules.mbinance.um.r.actions.save_time_diff import save_time_diff_action


class CompareServerTimeEffect(EffectBase):
    def effect(self, _):
        def __mapper(_: Action):
            return save_time_diff_action(0.5)

        return compose(of_type(get_time_diff_action), ops.map(__mapper))
