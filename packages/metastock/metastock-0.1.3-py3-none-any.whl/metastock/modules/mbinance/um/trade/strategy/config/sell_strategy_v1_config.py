from metastock.modules.mbinance.um.trade.strategy.config.strategy_config_base import (
    StrategyConfigBase,
)


class SellStrategyV1Config(StrategyConfigBase):
    def __init__(
        self,
        tp: float,
        sl: float,
        # __ Cấu hình của WT và Hull
        wt_diff_check: list,
        wt1_check: list,
        hull_diff_check: list,
        hull_check: list,
        # __ Flag check các loại điều kiện
        is_check_wt: bool = True,
        is_check_hull: bool = True,
        is_check_hull_condition_2: bool = False,
        # __ Check doc của base để hiểu phần giá min/max
        min_adj_price: float = 0,
        max_adj_price: float = 0.1,
        max_fixed_price: float | None = None,
    ):
        super().__init__(tp, sl, min_adj_price, max_adj_price, max_fixed_price)
        self._is_check_wt = is_check_wt
        self._is_check_hull = is_check_hull

        # ___________________ WT ___________________
        # ___ Điều kiện I của WT ___
        # Bắt buộc chênh lệch giữa 2 wt_diff phải lớn hơn phần tử đầu tiên, và giá trị hiện tại của nó phải nhỏ hơn phần
        # tử thứ 2 tức là tiến về ÂM(DOWNTREND)
        self._wt_diff_check = wt_diff_check
        # ___ Điều kiện II của WT ___
        # hệ số góc của WT1
        self._wt1_check = wt1_check

        # ___________________ Hull ___________________
        # ___ Điều kiện I của Hull ___
        # Hoặc là hull về dưới phần tử thứ nhất, hoặc là chỉ bằng n% so với đỉnh
        self._hull_diff_check = hull_diff_check

        # ___ Điều kiện II của Hull ___
        # Điều kiện để tính giá MAX, giảm sâu hơn giá này sẽ làm cho Hull đã xuống quá sâu, ko an toàn
        self._hull_check = hull_check
        self._is_check_hull_condition_2 = is_check_hull_condition_2

    def get_config_fields(self):
        return {
            "is_check_wt": self._is_check_wt,
            "is_check_hull": self._is_check_hull,
            "tp": self.tp,
            "sl": self.sl,
            "wt_diff_min": self._wt_diff_check[0],
            "wt_current_diff_max": self._wt_diff_check[1],
            "wt1_min": self._wt1_check[0],
            "hull_current_max_value": self._hull_diff_check[0],
            "hull_current_max_weight": self._hull_diff_check[1],
            "hull_current_max_deep": self._hull_check[0],
            "hull_current_max_deep_weight": self._hull_check[1],
            "hull_check_condition_2": self._is_check_hull_condition_2,
        }

    def is_check_hull(self) -> bool:
        return self._is_check_hull

    def is_check_hull_condition_2(self) -> bool:
        return self._is_check_hull_condition_2

    def get_wt_diff_min(self):
        """
        wt diff giữa 2 cây nến phải lớn hơn giá trị này
        :return:
        """
        return self._wt_diff_check[0]

    def get_current_wt_diff_max(self):
        """
        wt diff của cây nến hiện tại phải nhỏ hơn
        :return:
        """
        return self._wt_diff_check[1]

    def get_wt1_diff_min(self):
        """
        Giá trị wt1 giữa 2 cây nến tổi thiểu phải lớn hơn n đơn vị
        :return:
        """
        return self._wt1_check[0]

    def get_current_hull_max_value(self):
        """
        Giá trị hiện tại của hull phải nhỏ hơn
        :return:
        """
        return self._hull_diff_check[0]

    def get_hull_max_weight(self):
        """
        Giá trị hiện tại của hull so với đỉnh phải nhỏ hơn n%
        :return:
        """
        return self._hull_diff_check[1]

    def get_hull_max_deep(self):
        """
        Không mua khi hull đã xuống âm quá sâu
        :return:
        """
        return self._hull_check[0]

    def get_hull_deep_max_weight(self):
        """
        Trưởng hợp hull đã xuống âm thì so sánh nó với đỉnh xem có đi qua n% không

        :return:
        """
        return self._hull_diff_check[1]

    def __repr__(self):
        return (
            f"SellStrategyV1Config(\n"
            f"  Check WT: {self._is_check_wt}, Check Hull: {self._is_check_hull},\n"
            f"  Take Profit={self.tp},\n"
            f"  Stop Loss={self.sl},\n"
            f"  Wt_diff phải lớn hơn {self.get_wt_diff_min()} và hiện tại nhỏ hơn {self.get_current_wt_diff_max()},\n"
            f"  Diff của wt1(slope) là {self._wt1_check[0]}\n"
            f")"
        )
