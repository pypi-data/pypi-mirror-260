from metastock.modules.trade.strategy.filters.filter_abstract import FilterAbstract


class SpecificSymbolsFilter(FilterAbstract):
    name = 'specific_symbols_filter'

    def filter(self, symbol: str) -> bool:
        return True
