from metastock.modules.trade.strategy.filters.filter_abstract import FilterAbstract


class CapitalizationFilter(FilterAbstract):
    name = "capitalization_filter"

    def get_allowable_list(self) -> list[str]:
        pass
