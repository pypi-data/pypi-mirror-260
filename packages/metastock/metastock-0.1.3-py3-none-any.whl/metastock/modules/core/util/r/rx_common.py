from reactivex import compose, operators as ops

from metastock.modules.core.util.r.action import match_action


def of_type(*actions):
    def compare(s):
        for action in actions:
            if match_action(s, action):
                return True
        return False

    return compose(ops.filter(compare))
