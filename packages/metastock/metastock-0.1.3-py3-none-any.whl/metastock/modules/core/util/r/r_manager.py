from typing import Any

from pyrsistent import PRecord
from reactivex.subject import BehaviorSubject

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.exit_event import exit_application
from metastock.modules.core.util.r.action import Action
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.schedule_one_thread import schedule_one_thread
from metastock.modules.mbinance.error.fatal_error import FatalError


class RManager:
    __state = None
    __subscriptions = list()

    def __init__(self, combined_reducer: Any, logger: AppLogger):
        self.__logger = logger
        self.__combined_reducer = combined_reducer
        self.__event_ob = BehaviorSubject[Action](None)

        self.__state = combined_reducer(self.__state)

    def get_state(self) -> PRecord:
        return self.__state

    def dispatch(self, action: Action):
        self.__state = self.__combined_reducer(self.__state, action)

        self.get_event_ob().on_next(action)

    def get_event_ob(self) -> BehaviorSubject[Action]:
        return self.__event_ob

    def effect(self, effect: EffectBase):
        effect_instance = effect

        def __on_next(action: Action):
            if isinstance(action, Action) and action.name != "EMPTY":
                self.dispatch(action)

        def __on_error(error: Any):
            self.__logger.info("hererer")
            self.__logger.exception(error)
            if isinstance(error, FatalError):
                self.__logger.error("will quit application due to fatal error")
                exit_application()

        if isinstance(effect_instance, EffectBase):
            return (
                self.get_event_ob()
                .pipe(schedule_one_thread(), effect_instance.effect(self))
                .subscribe(
                    on_next=__on_next,
                    on_error=__on_error,
                )
            )

    def effects(self, *effects: EffectBase):
        for effect in effects:
            self.__subscriptions.append(self.effect(effect))

    def stop(self):
        for subscription in self.__subscriptions:
            subscription.dispose()
