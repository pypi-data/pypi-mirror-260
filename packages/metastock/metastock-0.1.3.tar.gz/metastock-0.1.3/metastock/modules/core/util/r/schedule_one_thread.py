from reactivex import compose, operators as ops
from reactivex.scheduler import ThreadPoolScheduler


def schedule_one_thread():
    return compose(
        ops.observe_on(ThreadPoolScheduler(1)),
        # ops.subscribe_on(ThreadPoolScheduler(1))
    )


def schedule_subscribe_one_thread():
    return compose(ops.subscribe_on(ThreadPoolScheduler(1)))


def schedule_both(max_workers: int = 1):
    return compose(
        ops.observe_on(ThreadPoolScheduler(max_workers)),
        ops.subscribe_on(ThreadPoolScheduler(max_workers)),
    )


def schedule_threads(max_workers: int = None):
    return ops.observe_on(ThreadPoolScheduler(max_workers=max_workers))
