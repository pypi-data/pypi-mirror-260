from abc import ABC, abstractmethod


class StrategyConfigBase(ABC):
    def __init__(
        self,
        tp: float,
        sl: float,
        min_adj_price: float,
        max_adj_price: float,
        max_fixed_price: float | None,
    ):
        self.tp = tp
        self.sl = sl

        # ___________________ Tính giá min/max lúc vào lệnh ___________________
        # +/- thêm % dựa vào base để cho ra được min/max price khi vào lệnh
        # Lưu ý: Tại giá MIN thì đạt được profit cao nhất, MAX là nguy hiểm nhất
        # Đối với Long: min price là giá thấp nhất(theo số học), max price là giá cao nhất
        # Đói với Short: min price là giá cao nhất(theo số học), max price là giá thấp nhất
        self._min_adj_price = min_adj_price
        self._max_adj_price = max_adj_price

        # ___________________ Max Fixed Price ___________________
        #  Trong trường hợp combine chart 30m với chart 1m, chúng ta đã tính được giá làm cho
        # chart 30m thoả mãn, do đó sẽ lấy giá đó làm giá MAX(giá cao nhất cho phép vào lệnh)
        # Nó sẽ thay thế giá base(trước đó là dùng đỉnh wt) để tính
        self._max_fixed_price = max_fixed_price

    def get_tp(self):
        return self.tp

    def get_sl(self):
        return self.sl

    def get_max_adj_price(self):
        return self._max_adj_price

    def get_max_fixed_price(self):
        return self._max_fixed_price

    @abstractmethod
    def get_config_fields(self) -> dict:
        pass
