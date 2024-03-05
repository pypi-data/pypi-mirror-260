from metastock.modules.mbinance.um.trade.strategy.sell.msell_v1 import MSellV1Strategy
from metastock.modules.mbinance.um.value.trade_strategy_type import DecideInfo


class MSellCombine30m1m:
    def __init__(
        self,
        strategy_30m: MSellV1Strategy,
        strategy_1m: MSellV1Strategy,
    ):
        self._strategy_30m = strategy_30m
        self._strategy_1m = strategy_1m

    def run(self) -> DecideInfo:
        decide = self._strategy_30m.get_decide()

        # Check chart 30m
        if decide.open_pos != True:
            return decide

        # Nếu chart 30m cho điểm vào
        # Chỗ này mình có 2 lựa chọn,
        # ___ I.
        #  Chạy cho chart 1m với giá max là giá từ chart 30m, giá min vẫn từ đỉnh cũ
        # Nếu giá minx/max bị conflict -> ignore. Nhiệm vụ là tìm được giá giữa min/max thoả mãn strategy_config
        #
        # ___ II. Sẽ mua với giá từ chart 30m, bài toán là lúc nào thì mua. Đối với mỗi cây nến, tính giá min từ
        # chart 30m. Nếu giá min thoả mãn điều kiện thì sẽ đặt lệnh => cũng sẽ quay lại trường hợp I nhưng trường hợp I
        # còn lợi hơn do giá min lúc này là đỉnh wt
        return self._strategy_1m.get_decide()
