from pyrsistent import pmap

from metastock.modules.core.util.r.action import Action


def combine_reducer(combined_reducer: dict):
    def reduce(state, action: Action = None):
        if state is None:
            state = pmap()

        for key in combined_reducer.keys():
            slice_reducer = combined_reducer.get(key)
            last_state = state.get(key)
            new_state = slice_reducer(last_state, action)

            # only update if changed
            if last_state is not new_state:
                state = state.set(key, new_state)

        return state

    return reduce
